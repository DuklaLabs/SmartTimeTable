import os
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import requests_cache
import lxml
import orjson

logging.basicConfig(level=logging.DEBUG)

OUTPUT_PATH = Path(__file__).parent

timetableData_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timetableData')
Path(timetableData_dir).mkdir(parents=True, exist_ok=True)

#Vytvoření globálních proměnných
#seznam učitelů jako pole teachres v json formátu
teachers = {
    "teachers": [ ]}
classes = {
    "classes": [ ]}
rooms = {
    "rooms": [ ]}

time_table = []

conf = {
    "hour_time" : []}

network_time = 0
processing_time = 0
runs = 0

session = requests_cache.CachedSession('bakalari_cache', expire_after=100000)

def get_links(url, soubor_nazev):
    try:
        # Získejte obsah stránky pomocí knihovny requests
        response = session.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'lxml')
        with open(soubor_nazev, 'w', encoding='utf-8') as soubor:
            soubor.write(response.text)
        
        get_teachers(soup)
        get_classes(soup)
        get_rooms(soup)
        get_hours_time(soup, 'bk-hour-wrapper')
    except requests.exceptions.RequestException as e:
        print(f"Chyba při požadavku: {e}")
        
def get_teachers(soup):
    odkazy = soup.find('div', {'id': 'teacher_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        
        teachers["teachers"].append(get_OBJ(odkaz))    
        
#funkce kro nalezení tříd
def get_classes(soup):
    odkazy = soup.find('div', {'id': 'class_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        #pridání objektu json s klíčem classes a hodnotou odkazu
        classes["classes"].append(get_OBJ(odkaz))

#funkce pro nalezení místností
def get_rooms(soup):
    odkazy = soup.find('div', {'id': 'room_canvas'}).find('div', class_='bk-canvas-body').find_all('a')
    for odkaz in odkazy:
        #pridání objektu json s klíčem classes a hodnotou odkazu
        rooms["rooms"].append(get_OBJ(odkaz))
        
def get_hours_time(soup, parametr):
    div_blok = soup.find_all('div', {'class': parametr})

    for blok in div_blok:
        NUM = blok.find('div', class_='num').text.strip()

        # Získání hodnoty z třídy "from"
        OD = blok.find('span', class_='from').text.strip()

        # Získání hodnoty ze všech elementů <span>
        spany = blok.find_all('span')
        if len(spany) == 3:
            DO = spany[2].text.strip()
        
        result = {
            NUM : {   "begin" : OD,
                      "end" : DO}}
        
        conf["hour_time"].append(result)
    
        
def get_lessons(soup):
         
    days = soup.find_all('div', class_="bk-cell-wrapper")
    skip = False
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
            
    return day_json
def check_cell(hour, class_):
    check = hour.find_all('div', class_="day-item-hover multi")
    if check:
        sp =[]
        for cell in check:
            sp.append(get_data(cell, nmbr))
        return sp
            
    
    
def get_data(cell, nmbr):
    if cell:
        js = cell.get('data-detail')
        detail_json = orjson.loads(js.encode('utf-8'))
        type_ = detail_json.get('type')
        group = room = lesson_ = subject = teacher = subject_text = teacher_text = change_info = theme = absencetext = has_absent = absent_info_text = removed_info = ""
        if type_ == "absent":
            subject = detail_json.get('absentinfo')
            subject_text = detail_json.get('InfoAbsentName')
        elif type_ == "removed":
            removed_info = detail_json.get('removedinfo')
        elif type_ == "atom":
            group = detail_json.get('group')
            room = detail_json.get('room')
            lesson_ = detail_json.get('subjecttext').split('|').pop(2).strip().split(' ')[0]
            subject = cell.find('div', class_="middle zapsano")
            subject = subject.text if subject else cell.find('div', class_="middle").text
            teacher = cell.find('div', class_="bottom").find('span')
            teacher = teacher.text if teacher else ""
            subject_text = detail_json.get('subjecttext').split('|').pop(0).strip() if 'subjecttext' in detail_json else ""
            teacher_text = detail_json.get('teacher') if 'teacher' in detail_json else ""
            change_info = detail_json.get('changeinfo') if 'changeinfo' in detail_json else ""
            theme = detail_json.get('theme') if 'theme' in detail_json else ""
            absencetext = detail_json.get("absencetext") if 'absencetext' in detail_json else ""
            has_absent = detail_json.get("hasAbsent") if 'hasAbsent' in detail_json else ""
            absent_info_text = detail_json.get("absentInfoText") if 'absentInfoText' in detail_json else ""
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
            "absencetext": "" if None else absencetext,
            "has_absent": "true" if has_absent else "false",
            "absent_info_text": absent_info_text,
            "removed_info": removed_info
        }
        return lesson
  

def get_timeTables(url, Json_file):
    global runs
    Json_file_path = os.path.join(timetableData_dir, Json_file)
    with open(Json_file_path, 'rb') as file:
        data = orjson.loads(file.read())
    with ThreadPoolExecutor(max_workers=30) as executor:
        for obj in data[Json_file.replace('.json','')]:
            name = next(iter(obj))
            print(name)
            permanent_url = obj[name]['Permanent']
            actual_url = obj[name]['Actual']
            next_url = obj[name]['Next']
            slozka = os.path.join(timetableData_dir, f"{Json_file.replace('.json','')}/{name}")
            Path(slozka).mkdir(parents=True, exist_ok=True)
            executor.submit(get_table, 'permanent', f'{url}{permanent_url}', Path(slozka))
            executor.submit(get_table, 'actual', f'{url}{actual_url}', Path(slozka))
            executor.submit(get_table, 'next', f'{url}{next_url}', Path(slozka))
            runs += 3
        

def get_table(typ, url, file):
    
    global network_time
    global processing_time
    start_time = time.time()
    response = session.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'lxml')
    end_time = time.time() 
    #print("network_time")
    #print(end_time-start_time)
    network_time += int((end_time - start_time)*1000) 
    
    start_time = time.time()
    lessons = get_lessons(soup)
    with open(f'{Path(file)}/{typ}.json', 'w', encoding='utf-8') as soubor:
        soubor.write(str(lessons).replace('\'','"').replace('None','""'))
        
    end_time = time.time()
    #print("process_time")
    #print(end_time-start_time)
    processing_time += int((end_time - start_time)*1000) 

def get_OBJ(link):
    tmp = link.text
    result = {
            tmp.replace('\n', '') : {   "Permanent" : link['href'].replace('Actual','Permanent').replace('/bakaweb/timetable/public/','') ,
                                        "Actual" : link['href'].replace('/bakaweb/timetable/public/',''),
                                        "Next" : link['href'].replace('Actual','Next').replace('/bakaweb/timetable/public/','')}}
    return result





script_start_time = time.time()

# Nastavte název souboru, kam chcete uložit odpověď
nazev_souboru = 'odpoved.html'

# Zde můžete nahradit '<>' vaším konkrétním parametrem
url_s_parametrem = "https://bakalari.spssecb.cz/bakaweb/Timetable/Public/"
slozka_scriptu = os.path.dirname(os.path.abspath(__file__))
cesta_k_souboru = os.path.join(slozka_scriptu, 'timetableData', nazev_souboru)

# Kontrola zda je url validní a dostupná
response = requests.get(url_s_parametrem)
response.raise_for_status()




get_links(url_s_parametrem, cesta_k_souboru)

# Serialize teachers dictionary
with open(os.path.join(timetableData_dir, 'teachers.json'), 'wb') as file:
    file.write(orjson.dumps(teachers))

# Serialize classes dictionary
with open(os.path.join(timetableData_dir, 'classes.json'), 'wb') as file:
    file.write(orjson.dumps(classes))

# Serialize rooms dictionary
with open(os.path.join(timetableData_dir, 'rooms.json'), 'wb') as file:
    file.write(orjson.dumps(rooms))

# Serialize conf dictionary
with open(os.path.join(timetableData_dir, 'conf.json'), 'wb') as file:
    file.write(orjson.dumps(conf))

    
get_timeTables(url_s_parametrem, 'teachers.json')
get_timeTables(url_s_parametrem, 'classes.json')
get_timeTables(url_s_parametrem, 'rooms.json')

script_end_time = time.time()

print (f"total Network time: {network_time}")
print (f"total Procesing time: {processing_time}")
print (f"Network time per run: {network_time/runs}")
print (f"Processing time per run: {processing_time/runs}")
print (f"Total runs: {runs}")
print (f"Total Execution time per run: {(script_end_time-script_start_time)/runs}") 
print (f"Total Execution time: {script_end_time-script_start_time}")




time.sleep(2)
# Nastavení globální proměnné fetch_data na False po 2 sekundách
with open(OUTPUT_PATH / 'globals.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    data['fetch_data'] = False
    with open(OUTPUT_PATH /'globals.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    


