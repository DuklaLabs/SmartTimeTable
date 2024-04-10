from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "classes"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x600")
window.configure(bg="#FFFFFF")
window.title("SmartTimeTable V0.4 by DuklaLabs - Classes")
window.attributes("-fullscreen", True)
window.config(cursor="none")


canvas = Canvas(
    window,
    bg="#2F2F2F",
    height=600,
    width=1024,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


button_image_1 = PhotoImage(
    file=relative_to_assets("ExitButton.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),
    relief="flat"
)
button_1.place(
    x=935.0,
    y=30.0,
    width=60.0,
    height=60.0
)

import json

def update_globals(class_name):
    # Load the data from the JSON file
    with open(OUTPUT_PATH / "globals.json", "r") as f:
        data = json.load(f)

    # Update the values
    data["timetable_data"] = class_name
    data["timetable_type"] = "Class"
    data["regenerate_timetable"] = True

    # Write the data back to the JSON file
    with open(OUTPUT_PATH / "globals.json", "w") as f:
        json.dump(data, f)
    window.destroy()

# Load class data from JSON file
with open(OUTPUT_PATH / "timetableData" / "classes.json", "r", encoding="utf-8") as f:
    class_data = json.load(f)

button_image = PhotoImage(file=relative_to_assets("ClassButton.png"))
class_buttons_ = []

# Extract class names
class_names = [list(class_dict.keys())[0] for class_dict in class_data["classes"]]

# Set the number of rows and columns for the buttons
num_rows = 4
num_cols = 4

# Initialize the class_buttons list
class_buttons = [[None] * num_cols for _ in range(num_rows)]

# Iterate over class names
for i, class_name in enumerate(class_names):
    class_buttons_.append(Button(image=button_image, text=class_name, font=("Kanit Light", 23), compound="center", borderwidth=0, highlightthickness=0, command=lambda class_name=class_name: update_globals(class_name), relief="flat"))
    class_buttons[i // num_cols][i % num_cols] = class_buttons_[-1]
    class_buttons[i // num_cols][i % num_cols].place(x=144.0 + (i % num_cols) * 195, y=117.0 + (i // num_cols) * 100, width=150.0, height=65.0)

canvas.create_text(
    512.0,
    45.0,
    anchor="center",
    text="Třídy",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)
window.resizable(False, False)
window.mainloop()
