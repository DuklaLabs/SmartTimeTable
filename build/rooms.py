from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\rooms")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1024x600")
window.configure(bg="#FFFFFF")
window.title("SmartTimeTable V0.4 by DuklaLabs - Rooms")
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



def update_globals(class_name):
    # Load the data from the JSON file
    with open('build\\globals.json', 'r') as f:
        data = json.load(f)

    # Update the values
    data['timetable_data'] = class_name
    data['timetable_type'] = 'Room'
    data['regenerate_timetable'] = True

    print(data)

    # Write the data back to the JSON file
    with open('build\\globals.json', 'w') as f:
        json.dump(data, f)
    window.destroy()

# Load room data from JSON file
with open('build\\timetableData\\rooms.json', 'r', encoding='utf-8') as f:
    room_data = json.load(f)

# Extract room names
room_names = [list(room_dict.keys())[0] for room_dict in room_data['rooms']]

room_buttons = []
button_image = PhotoImage(file=relative_to_assets("RoomButton.png"))

# Generate buttons for each room
for i, room_name in enumerate(room_names):
    room_buttons.append(Button(image=button_image, borderwidth=0, highlightthickness=0,
                                text=room_name, fg="black", font=("Kanit Light", 20),
                                compound='center',
                                command=lambda room_name=room_name: update_globals(room_name), relief="flat"))
    room_buttons[i].place(x=317.0, y=100.0 + (i * 65), width=140.0, height=45.0)

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

canvas.create_text(
    512.0,
    45.0,
    anchor="center",
    text="Učebny",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)
window.resizable(False, False)
window.mainloop()