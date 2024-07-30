#!/usr/bin/env python3

import os
from pathlib import Path
from subprocess import Popen
import sys
from time import strftime
from tkinter import Tk, Canvas, Button, PhotoImage, Label
import datetime
import json
from PIL import Image, ImageTk
import asyncio

import globals
from teachers import open_teachers_menu
from classes import open_classes_menu
from rooms import open_rooms_menu
from timetableInfo import show_timetable_info
from credits import show_credits
from getTimetableData import get_timetable_data


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "timetable"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

default_timetable_type = globals.timetable_type
default_timetable_data = globals.timetable_data
default_timetable_time_period = globals.timetable_time_period


root = Tk()

root.geometry("1024x600")
root.configure(bg="#FFFFFF")
root.title("SmartTimeTable V0.4 by DuklaLabs")
root.attributes("-fullscreen", True)
#root.config(cursor="none")

timetable_inactivity = 0

canvas = Canvas(
    root,
    bg="#2F2F2F",
    height=600,
    width=1024,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


image_image_1 = PhotoImage(
    file=relative_to_assets("Timetable.png"))
image_1 = canvas.create_image(
    901.0,
    300.0,
    image=image_image_1
)









dragging = False
last_x_position = 0

def start_drag(event):
    global timetable_inactivity
    timetable_inactivity = 0
    global dragging, last_x_position
    overlapping = canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
    if image_1 in overlapping:
        dragging = True
        last_x_position = event.x


def drag(event):
    global dragging, last_x_position
    if dragging:
        x_movement = event.x - last_x_position
        current_position = canvas.coords(image_1)
        if 197 <= current_position[0] + x_movement <= 901:
            # Move image_1
            canvas.move(image_1, x_movement, 0)
            # Move main_texts
            for row in main_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
            # Move bottom_texts
            for row in bottom_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
            # Move top_texts
            for row in top_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
        last_x_position = event.x


def stop_drag(event):
    global dragging
    dragging = False

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", stop_drag)









image_image_2 = PhotoImage(
    file=relative_to_assets("WeekdaysBackground.png"))
image_2 = canvas.create_image(
    37.0,
    300.0,
    image=image_image_2
)






# If the window is not touched for more than 30 seconds, than change the timetable time type to a default one from the globals.py file
def check_timetable_inactivity():
    global timetable_inactivity
    if timetable_inactivity >= 30:
        print("Timetable inactive for too long, changing to default")

        globals.timetable_type = default_timetable_type
        globals.timetable_data = default_timetable_data
        globals.timetable_time_period = "Permanent"
            
        change_timetable_time_period()
        timetable_inactivity = 0

# Increase the timetable_inactivity variable every second
def increase_timetable_inactivity():
    global timetable_inactivity
    timetable_inactivity += 1
    check_timetable_inactivity()
    root.after(1000, increase_timetable_inactivity)









main_ = []
top_ = []
bottom_ = []

main_texts = [[None] * 5 for _ in range(11)]
bottom_texts = [[None] * 5 for _ in range(11)]
top_texts = [[None] * 5 for _ in range(11)]

position_offset = 901

def generate_timetable():
    # Destroy the previous timetable
    destroy_timetable()

    # Update the timetable name
    update_timetable_name()

    # Define the mapping from timetable_type to folder name
    type_to_folder = {"teacher": "teachers", "class": "classes", "room": "rooms"}


    # Construct the file path
    timetable_type = globals.timetable_type.lower()
    timetable_data = globals.timetable_data
    timetable_period = globals.timetable_time_period.lower()

    file_path = OUTPUT_PATH / "timetableData" / type_to_folder[timetable_type] / timetable_data / f"{timetable_period}.json"
    print(file_path)

    # Load the JSON file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            timetable_data = json.load(file)
    except FileNotFoundError:
        print("File not found, retrying")
        global timetable_inactivity
        timetable_inactivity = 10000
        check_timetable_inactivity()
        return

    # Define the mapping from timetable_type to text fields
    type_to_text_fields = {
        "teacher": {"main": "subject", "top": "room", "bottom": "group"},
        "class": {"main": "subject", "top": "room", "bottom": "teacher"},
        "room": {"main": "subject", "top": "teacher", "bottom": "group"},
    }

    text_fields = type_to_text_fields[timetable_type]

    # Get the current position of the timetable
    current_position = canvas.coords(image_1)[0]

    # Use the data from the JSON file to create the timetable
    for j in range(5):
        for i in range(11):
            try:
                if (timetable_type == "class"):
                    lesson = timetable_data.get(str(j*11 + i), [{}])  # Get the lesson for all groups
                    # If the lesson is empty, skip it
                    if lesson == [{}]:
                        continue
                    # Loop through all groups and create the lesson by combining the the bottom and top text of each group
                    # Use the main text of the first group
                    main_text = lesson[0].get(text_fields["main"], "").replace(" celá", "")
                    bottom_text = ", ".join([group.get(text_fields["bottom"], "").replace(" celá", "") for group in lesson if group.get(text_fields["bottom"], "").replace(" celá", "")])
                    top_text = ", ".join([group.get(text_fields["top"], "").replace(" celá", "") for group in lesson if group.get(text_fields["top"], "").replace(" celá", "")])
                else:
                    lesson = timetable_data.get(str(j*11 + i), [{}])[0]  # Get the lesson for one group
                    # If the lesson is empty, skip it
                    if lesson == "":
                        continue
                    main_text = lesson.get(text_fields["main"], "").replace(" celá", "")
                    bottom_text = lesson.get(text_fields["bottom"], "").replace(" celá", "")
                    top_text = lesson.get(text_fields["top"], "").replace(" celá", "")
                # If there is no top or bottom text then center the main text
                if top_text == "" and bottom_text == "":
                    main_text_center_offset = 30
                    main_size = 28
                else:
                    main_text_center_offset = 0
                    main_size = 28

                if (len(main_text) < 5 and len(top_text) >= 10):
                    main_size = 22
                    top_text_center_offset = -5
                    main_text_center_offset = -5
                else:
                    main_size = 28
                    top_text_center_offset = 0
                main_.append(canvas.create_text(current_position - position_offset + main_text_center_offset + 116 + i * 150, 190 + j * 75, anchor="center", text=main_text, fill="#D3D3D3", font=("Inter Light", main_size * -1)))
                main_texts[i][j] = main_[-1]

                if len(bottom_text) <= 4:
                    bottom_size = 20
                else:
                    # Dynamic font size so the text fits in the box
                    bottom_size = 20 - (len(bottom_text) - 5)
                bottom_.append(canvas.create_text(current_position - position_offset + 184 + i * 150, 200 + j * 75, anchor="center", text=bottom_text, fill="#D3D3D3", font=("Inter", bottom_size * -1)))
                bottom_texts[i][j] = bottom_[-1]

                if len(top_text) <= 4:
                    top_size = 20
                else:
                    # Dynamic font size so the text fits in the box
                    top_size = 16 - (len(top_text) - 11)
                top_.append(canvas.create_text((current_position - position_offset + 184 + i * 150) + top_text_center_offset, 175 + j * 75, anchor="center", text=top_text, fill="#D3D3D3", font=("Inter Light", top_size * -1)))
                top_texts[i][j] = top_[-1]
            except Exception as e:
                print(f"Error creating ¨lesson: {e}")

    global weekdays_texts

    canvas.tag_raise(image_2)
    for i in range(5):
        # Raise all weekdays if they exist
        if weekdays_texts[i] is not None:
            canvas.tag_raise(weekdays_texts[i])
    # Raise all dates
    for row in dates:
        for date in row:
            if date is not None:
                canvas.tag_raise(date)

    globals.regenerate_timetable = False

    # Set the timetable inactivity to 0
    timetable_inactivity = 0





def destroy_timetable():
    for row in main_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)
    for row in bottom_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)
    for row in top_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)


timetable_name_text = canvas.create_text(80, 10, anchor="nw", text="", fill="#D3D3D3", font=("Inter", 50 * -1))


def update_timetable_name():
    timetable_type = globals.timetable_type.lower()
    timetable_data = globals.timetable_data

    # Open the corresponding timetable info file depending on the timetable type
    if timetable_type == "class":
        with open(OUTPUT_PATH / "timetableData" / "info" / "classesInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["classes"]
            timetable_info = next((class_info for class_info in timetable_info_list if timetable_data in class_info), None)

    elif timetable_type == "teacher":
        with open(OUTPUT_PATH / "timetableData" / "info" / "teachersInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["teachers"]
            timetable_info = next((teacher_info for teacher_info in timetable_info_list if timetable_data in teacher_info), None)

    elif timetable_type == "room":
        with open(OUTPUT_PATH / "timetableData" / "info" / "roomsInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["rooms"]
            timetable_info = next((room_info for room_info in timetable_info_list if timetable_data in room_info), None)

    # Create the title by getting the name from the corresponding timetable info file
    if timetable_info is not None:
        timetable_name = timetable_info[timetable_data].get("name", "Default Name")
    else:
        timetable_name = "Unknown Timetable"

    # Add 2 spaces in front of the name to move it to the right
    timetable_name = "  " + timetable_name

    canvas.itemconfigure(timetable_name_text, text=timetable_name)




#Create the clock
def clock():
    #Get the current time and date and format it to 12:00   31.12.2024
    string = strftime("%H:%M   %d.%m.%Y")
    lbl.configure(text=string)
    lbl.after(1000, clock)


lbl = Label(root, font=("Inter", 28), background = "#303030", foreground = "#B6B6B6")

lbl.place(x=770, y=40, anchor="center")
clock()



import json

# Create the dates matrix
dates = [[None] * 5 for _ in range(1)]
weekdays_texts = [None for _ in range(5)]

def change_timetable_time_period():

    # Update the values
    if globals.timetable_time_period == "Actual":
        globals.timetable_time_period = "Next"
        timetable_time_period_label.config(text="Příští", bg="#D9D9D9", fg="#000000", font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()
        start_date = datetime.date.today()
        # Calculate the offset to the next Monday
        offset = (7 - start_date.weekday()) % 7
        for j in range(5):
            date = start_date + datetime.timedelta(days=j + offset)
            dates[0][j] = canvas.create_text(39, 205 + j * 75, anchor="center", text=date.strftime("%d.%m."), fill="#D3D3D3", font=("Inter Light", 20 * -1))

    elif globals.timetable_time_period == "Next":
        globals.timetable_time_period = "Permanent"
        timetable_time_period_label.config(text="Stálý", bg="#D9D9D9", fg="#000000", font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()

    elif globals.timetable_time_period == "Permanent":
        globals.timetable_time_period = "Actual"
        timetable_time_period_label.config(text="Aktuální", bg="#D9D9D9", fg="#000000", font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()
        start_date = datetime.date.today()
        # Calculate the offset to this week"s Monday
        offset = ((7 - start_date.weekday()) % 7) - 7
        for j in range(5):
            date = start_date + datetime.timedelta(days=j + offset)
            dates[0][j] = canvas.create_text(39, 205 + j * 75, anchor="center", text=date.strftime("%d.%m."), fill="#D3D3D3", font=("Inter Light", 20 * -1))

    weekdays = ["Po", "Út", "St", "Čt", "Pá"]
    for j in range(5):
        if weekdays_texts[j] is not None:
            canvas.delete(weekdays_texts[j])
            weekdays_texts[j] = None
            root.update()
        
    if globals.timetable_time_period == "Permanent":
        weekdays_y = 185
        weekdays_text_size = 32
    else:
        weekdays_y = 175
        weekdays_text_size = 27
    for i in range(5):
        weekdays_texts[i] = canvas.create_text(39, weekdays_y + i * 75, anchor="center", text=weekdays[i], fill="#D3D3D3", font=("Inter", weekdays_text_size * -1))

    globals.regenerate_timetable = True

    # Update the root
    root.update()




def destroy_dates():
    # delete the dates if they exist
    for j in range(5):
        if dates[0][j] is not None:
            canvas.delete(dates[0][j])
            dates[0][j] = None







def rotate_image(image, angle):
    rotated_image = image.rotate(angle)
    return ImageTk.PhotoImage(rotated_image)

def update_image():
    global angle, photo_image, canvas, loading
    angle = (angle - 3) % 360  # Update the angle
    photo_image = rotate_image(image, angle)  # Rotate the image
    canvas.itemconfig(loading, image=photo_image)  # Update the image on the canvas
    canvas.tag_raise(loading)  # Place the loading image on top of everything else
    root.after(10, update_image)  # Call this function again after 100 ms

# Function to run the async function and handle completion
def run_get_timetable_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_timetable_data())
    print("Timetable data fetching completed")
    button_6.place(x=964.0, y=14.0, width=50.0, height=50.0)
    generate_timetable()



image = Image.open(relative_to_assets("Loading.png"))
photo_image = ImageTk.PhotoImage(image)
# Place the loading image in the middle of the refresh button
loading = canvas.create_image(987, 40, image=photo_image)
canvas.tag_raise(loading)
# Update the image
angle = 0
update_image()


def fetch_data():

    # Create a big "Mimo provoz!" text centered in the middle of the screen
    # global big_text
    # big_text = canvas.create_text(512, 300, anchor="center", text="Mimo provoz!", fill="#0000FF", font=("Inter", 100 * -1))

    # Hide the refresh button
    button_6.place_forget()

    # Start the async function to fetch the data
    run_get_timetable_data()

    # Delete the big text after 1second
    # root.after(2000, lambda: canvas.delete(big_text))









button_image_1 = PhotoImage(
    file=relative_to_assets("CreditsButton.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_credits(root),
    relief="flat"
)
button_1.place(
    x=955.0,
    y=530.0,
    width=65.0,
    height=65.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("InfoButton.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_timetable_info(root),
    relief="flat"
)
button_2.place(
    x=16.0,
    y=11.0,
    width=45.0,
    height=55.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("ClassesButton.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_classes_menu(root),
    relief="flat"
)
button_3.place(
    x=452.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("TeachersButton.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_teachers_menu(root),
    relief="flat"
)
button_4.place(
    x=272.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("RoomsButton.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_rooms_menu(root),
    relief="flat"
)
button_7.place(
    x=632.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("TimetableTypeButton.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: change_timetable_time_period(),
    relief="flat",
    activeforeground="#000000",
    activebackground="#D9D9D9"
)
button_5.place(
    x=43.0,
    y=540.0,
    width=150.0,
    height=45.0
)

timetable_time_period_label = Label(text="Aktuální", bg="#D9D9D9", fg="#000000", font=("Kanit", 30 * -1), anchor="center")
timetable_time_period_label.place(
    x=43.0 + 75.0,
    y=540.0 + 22.5,
    anchor="center"
)
timetable_time_period_label.bind("<Button-1>", lambda e: button_5.invoke())


button_image_6 = PhotoImage(
    file=relative_to_assets("RefreshButton.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: fetch_data(),
    relief="flat"
)
button_6.place(
    x=964.0,
    y=14.0,
    width=50.0,
    height=50.0
)
# Raise the loading image to be on top of the button
canvas.tag_raise(loading)

root.resizable(False, False)

change_timetable_time_period()
generate_timetable()

def check_and_regenerate():
    if globals.regenerate_timetable:
        print("Regenerating")
        generate_timetable()
        # refresh the window
        root.update()

    root.after(250, check_and_regenerate)

# Start checking
check_and_regenerate()




increase_timetable_inactivity()


canvas.tag_raise(loading)

canvas.tag_raise(image_2)
for i in range(5):
    canvas.tag_raise(weekdays_texts[i])
# Raise all dates
for row in dates:
    for date in row:
        if date is not None:
            canvas.tag_raise(date)

root.mainloop()
