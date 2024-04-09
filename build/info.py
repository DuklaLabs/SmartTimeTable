from pathlib import Path
from subprocess import Popen
import sys
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image,ImageTk
import json


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\credits")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()


window.geometry("1024x600")
window.configure(bg = "#FFFFFF")
window.title("SmartTimeTable V0.4 - Credits")
window.attributes("-fullscreen", True)
window.config(cursor = "none")

canvas = Canvas(
    window,
    bg = "#2F2F2F",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

button_image_1 = PhotoImage(
    file=relative_to_assets("Exit.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),
    relief="flat"
)
button_1.place(
    x=930.0,
    y=25.0,
    width=60.0,
    height=60.0
)



# Load the currently selected timetable from the globals.json file
with open('build\\globals.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    timetable_type = data['timetable_type'].lower()
    timetable_data = data['timetable_data']

# Open the corresponding timetable info file depending on the timetable type
if timetable_type == "class":
    with open(f"build\\timetableData\\info\\classesInfo.json", "r", encoding='utf-8') as file:
        timetable_info_list = json.load(file)['classes']
        timetable_info = next((class_info for class_info in timetable_info_list if timetable_data in class_info), None)

elif timetable_type == "teacher":
    with open(f"build\\timetableData\\info\\teachersInfo.json", "r", encoding='utf-8') as file:
        timetable_info_list = json.load(file)['teachers']
        timetable_info = next((teacher_info for teacher_info in timetable_info_list if timetable_data in teacher_info), None)

elif timetable_type == "room":
    with open(f"build\\timetableData\\info\\roomsInfo.json", "r", encoding='utf-8') as file:
        timetable_info_list = json.load(file)['rooms']
        timetable_info = next((room_info for room_info in timetable_info_list if timetable_data in room_info), None)

# Create the title by getting the name from the corresponding timetable info file
if timetable_info is not None:
    timetable_name = timetable_info[timetable_data].get('name', 'Default Name')
else:
    timetable_name = 'Unknown Timetable'
canvas.create_text(
    512.0,
    60.0,
    anchor="center",
    text=timetable_name,
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)

import textwrap

info_text = ""
if timetable_info is not None:
    # Create the info text by getting the info from the corresponding timetable info file
    info_text = timetable_info[timetable_data].get('info', 'No info available')
else:
    info_text = 'No info available'

# Wrap the text if it's too long
wrapped_text = textwrap.fill(info_text, width=60)

# Split the wrapped text into lines
lines = wrapped_text.split('\n')

# Calculate the initial y coordinate
y = 150

# Create each line as a separate text item on the canvas
for line in lines:
    canvas.create_text(512, y, anchor="n", text=line, fill="#FFFFFF", font=("Kanit", 32 * -1))
    y += 35  # Move the y coordinate down for the next line






window.resizable(False, False)
window.mainloop()
