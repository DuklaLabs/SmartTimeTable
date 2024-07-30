import os
import json
from pathlib import Path
import time
import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import orjson

import globals

logging.basicConfig(level=logging.INFO)

OUTPUT_PATH = Path(__file__).parent

timetableData_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetableData')
Path(timetableData_dir).mkdir(parents=True, exist_ok=True)

# Global variables
teachers = {"teachers": []}
classes = {"classes": []}
rooms = {"rooms": []}
conf = {"hour_time": []}

network_time = 0
processing_time = 0
runs = 0

semaphore = asyncio.Semaphore(1000)

async def fetch(url, session):
    async with semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

async def get_links(url, session):
    try:
        html = await fetch(url, session)
        soup = BeautifulSoup(html, 'lxml')
        get_teachers(soup)
        get_classes(soup)
        get_rooms(soup)
        get_hours_time(soup, 'bk-hour-wrapper')
    except Exception as e:
        logging.error(f"Request error: {e}")

def get_teachers(soup):
    odkazy = soup.find('div', {'id': 'teacher_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        teachers["teachers"].append(get_OBJ(odkaz))
    # Manually add teachers that are not in the list (e.g. teachers that are not teaching this year or have left the school)
    teachers['teachers'].append({'Požárek Pavel': {'Permanent': 'none', 'Actual': 'none', 'Next': 'none'}})
    # Sort the teachers by name
    teachers["teachers"] = sorted(teachers["teachers"], key=lambda x: list(x.keys())[0])

def get_classes(soup):
    odkazy = soup.find('div', {'id': 'class_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        classes["classes"].append(get_OBJ(odkaz))

def get_rooms(soup):
    odkazy = soup.find('div', {'id': 'room_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        rooms["rooms"].append(get_OBJ(odkaz))

def get_hours_time(soup, parametr):
    div_blok = soup.find_all('div', {'class': parametr})
    for blok in div_blok:
        NUM = blok.find('div', class_='num').text.strip()
        OD = blok.find('span', class_='from').text.strip()
        DO = blok.find_all('span')[2].text.strip() if len(blok.find_all('span')) == 3 else ""
        result = {NUM: {"begin": OD, "end": DO}}
        conf["hour_time"].append(result)

def get_OBJ(link):
    tmp = link.text.strip()
    return {
        tmp: {
            "Permanent": link['href'].replace('Actual', 'Permanent').replace('/bakaweb/timetable/public/', ''),
            "Actual": link['href'].replace('/bakaweb/timetable/public/', ''),
            "Next": link['href'].replace('Actual', 'Next').replace('/bakaweb/timetable/public/', '')
        }
    }

async def fetch_timetable_data(name, url, typ, session, file):
    global network_time
    global processing_time
    start_time = time.time()
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'lxml')
    end_time = time.time()
    network_time += (end_time - start_time)

    start_time = time.time()
    lessons = get_lessons(soup)
    with open(f'{Path(file)}/{typ}.json', 'w', encoding='utf-8') as soubor:
        soubor.write(orjson.dumps(lessons).decode())
    end_time = time.time()
    processing_time += (end_time - start_time)

async def get_timeTables(url, Json_file):
    global runs
    Json_file_path = os.path.join(timetableData_dir, Json_file)
    with open(Json_file_path, 'rb') as file:
        data = orjson.loads(file.read())

    async with aiohttp.ClientSession() as session:
        tasks = []
        for obj in data[Json_file.replace('.json', '')]:
            name = next(iter(obj))
            urls = obj[name]
            slozka = os.path.join(timetableData_dir, f"{Json_file.replace('.json', '')}/{name}")
            Path(slozka).mkdir(parents=True, exist_ok=True)
            for typ in ["Permanent", "Actual", "Next"]:
                tasks.append(fetch_timetable_data(name, f"{url}{urls[typ]}", typ.lower(), session, Path(slozka)))
                runs += 1

        await asyncio.gather(*tasks)

def get_lessons(soup):
         
    days = soup.find_all('div', class_="bk-cell-wrapper")
    skip = False
    day_json = None
    for day in days:
        hours = soup.find_all('div', class_="bk-timetable-cell")
        day_json = orjson.loads(b'{}')
        nmbr = 0
        sp=0
        for hour in hours:
            sp = []
            check = hour.find_all('div', class_="day-item-hover multi")
            if check:
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            check = None
            check = hour.find_all('div', class_="day-item-hover")
            if check and len(check) == 1:  # Check if there is only one item in check
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            check = None
            check = hour.find_all('div', class_="day-item-hover multi pink")
            if check:
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            check = None
            check = hour.find_all('div', class_="day-item-hover  border-levy green h-100")
            if check:
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            check = None
            check = hour.find_all('div', class_="day-item-hover  pink ")
            if check:
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            check = None
            check = hour.find_all('div', class_="day-item-hover  pink hasAbsent")
            if check:
                for cell in check:
                    sp.append(get_data(cell, nmbr))
            
            check = None
            check = hour.find_all('div', class_="day-item-volno border-levy border-horni border-pravy")
            if check:
                for cell in check:
                    skip = True

            if sp:
                day_json[str(nmbr)] = sp        

        
            if skip:
                skip = False
                nmbr += 11
            else:
                nmbr += 1

            if day_json is None:
                day_json = orjson.loads(b'{}')
            
    return day_json



def get_data(cell, nmbr):
    if cell:
        js = cell.get('data-detail')
        detail_json = orjson.loads(js.encode('utf-8'))
        type_ = detail_json.get('type')
        group = room = lesson_ = subject = teacher = subject_text = teacher_text = change_info = theme = absencetext = has_absent = absent_info_text = removed_info = ""
        
        # Store the result of detail_json.get() in variables
        subjecttext = detail_json.get('subjecttext')
        teacher = detail_json.get('teacher')
        changeinfo = detail_json.get('changeinfo')
        theme = detail_json.get('theme')
        absencetext = detail_json.get('absencetext')
        hasAbsent = detail_json.get('hasAbsent')
        absentInfoText = detail_json.get('absentInfoText')

        if type_ == "absent":
            subject = detail_json.get('absentinfo')
            subject_text = detail_json.get('InfoAbsentName')
        elif type_ == "removed":
            removed_info = detail_json.get('removedinfo')
        elif type_ == "atom":
            group = detail_json.get('group')
            room = detail_json.get('room')
            lesson_ = subjecttext.split('|').pop(2).strip().split(' ')[0] if subjecttext else ""
            subject = cell.find('div', class_="middle zapsano")
            subject = subject.text if subject else cell.find('div', class_="middle").text
            teacher = cell.find('div', class_="bottom").find('span')
            teacher = teacher.text if teacher else ""
            subject_text = subjecttext.split('|').pop(0).strip() if subjecttext else ""
            teacher_text = teacher if teacher else ""
            change_info = changeinfo if changeinfo else ""
            theme = theme if theme else ""
            absencetext = "" if None else absencetext
            has_absent = "true" if hasAbsent else "false"
            absent_info_text = absentInfoText if absentInfoText else ""
        else:
            print("error"+ type_)
        # Vytvoření objektu s informacemi o hodině
        lesson = {
            "lesson": lesson_,
            "group": group,
            "room": room,
            "subject": subject,
            "subject_text": subject_text,
            "teacher": teacher,
            "teacher_text": teacher_text,
            "change_info": change_info,
            "theme": theme,
            "type": type_,
            "absencetext": absencetext,
            "has_absent": has_absent,
            "absent_info_text": absent_info_text,
            "removed_info": removed_info
        }
        return lesson

def add_teacher(teacher_name, teacher_info):
    teachers_file = os.path.join(timetableData_dir, 'teachers.json')
    with open(teachers_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data["teachers"].append({teacher_name: teacher_info})
    data["teachers"] = sorted(data["teachers"], key=lambda x: list(x.keys())[0])
    with open(teachers_file, 'w', encoding='utf-8') as file:
        json.dump(data, file)





async def get_timetable_data():
    print("Started fetching data...")
    script_start_time = time.time()

    url_s_parametrem = "https://bakalari.spssecb.cz/bakaweb/Timetable/Public/"
    soubor_nazev = "output.json"

    async with aiohttp.ClientSession() as session:
        await get_links(url_s_parametrem, session)
    
    with open(os.path.join(timetableData_dir, 'conf.json'), 'w', encoding='utf-8') as soubor:
        soubor.write(orjson.dumps(conf).decode())

    with open(os.path.join(timetableData_dir, 'teachers.json'), 'w', encoding='utf-8') as soubor:
        soubor.write(orjson.dumps(teachers).decode())

    print("Teachers data fetched successfully")

    with open(os.path.join(timetableData_dir, 'classes.json'), 'w', encoding='utf-8') as soubor:
        soubor.write(orjson.dumps(classes).decode())

    print("Classes data fetched successfully")

    with open(os.path.join(timetableData_dir, 'rooms.json'), 'w', encoding='utf-8') as soubor:
        soubor.write(orjson.dumps(rooms).decode())

    print("Rooms data fetched successfully")

    print("Started fetching timetable data...")

    await get_timeTables(url_s_parametrem, 'teachers.json')
    print("Teachers timetable data fetched successfully")
    await get_timeTables(url_s_parametrem, 'classes.json')
    print("Classes timetable data fetched successfully")
    await get_timeTables(url_s_parametrem, 'rooms.json')
    print("Rooms timetable data fetched successfully")

    globals.regenerate_timetable = True
    
    script_end_time = time.time()

    logging.info(f"Network time: {network_time:.2f} s  -async")
    logging.info(f"Processing time: {processing_time:.2f} s  -async")
    logging.info(f"Total runtime: {script_end_time - script_start_time:.2f} s")
    logging.info(f"Total runs: {runs}")


if __name__ == "__main__":
    asyncio.run(get_timetable_data())