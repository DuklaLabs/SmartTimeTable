from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import math

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





dragging_number = False
last_y_position_number = 0
buttons_enabled_number = True

dragging_d = False
last_y_position_d = 0
buttons_enabled_d = True

dragging_other = False
last_y_position_other = 0
buttons_enabled_other = True

def start_drag_number(event):
    global dragging_number, last_y_position_number, buttons_enabled_number
    dragging_number = True
    x, y = window.winfo_pointerxy()
    last_y_position_number = canvas.canvasy(y)
    global drag_start_position_number
    drag_start_position_number = event.y

def start_drag_d(event):
    global dragging_d, last_y_position_d, buttons_enabled_d
    dragging_d = True
    x, y = window.winfo_pointerxy()
    last_y_position_d = canvas.canvasy(y)
    global drag_start_position_d
    drag_start_position_d = event.y

def start_drag_other(event):
    global dragging_other, last_y_position_other, buttons_enabled_other
    dragging_other = True
    x, y = window.winfo_pointerxy()
    last_y_position_other = canvas.canvasy(y)
    global drag_start_position_other
    drag_start_position_other = event.y

def drag_number(event):
    global last_y_position_number, dragging_number, buttons_enabled_number
    if dragging_number:
        x, y = window.winfo_pointerxy()
        y_movement = canvas.canvasy(y) - last_y_position_number
        # Get the y position of the first button using the bbox method
        current_position = canvas.bbox(number_room_button_ids[0])[1]  # Extract only the Y coordinate
        print(current_position)
        # Limit the movement of the buttons
        if abs(y_movement) > 1:
            if current_position + y_movement <= 171 and current_position + y_movement >= 130 - (65 * (len(number_room_button_ids) - 6)):
                # Move the buttons
                for button_id in number_room_button_ids:
                    canvas.move(button_id, 0, y_movement)
                last_y_position_number = canvas.canvasy(y)
            elif current_position + math.copysign(1, y_movement) <= 171 and current_position + math.copysign(1, y_movement) >= 130 - (65 * (len(number_room_button_ids) - 6)):
                # Move the buttons by 1 pixel
                for button_id in number_room_button_ids:
                    canvas.move(button_id, 0, math.copysign(1, y_movement))
                last_y_position_number = canvas.canvasy(y)

        if abs(drag_start_position_number - current_position) > 20:
            # Disable the buttons
            buttons_enabled_number = False

def drag_d(event):
    global last_y_position_d, dragging_d, buttons_enabled_d
    if dragging_d:
        x, y = window.winfo_pointerxy()
        y_movement = canvas.canvasy(y) - last_y_position_d
        # Get the y position of the first button using the bbox method
        current_position = canvas.bbox(d_room_button_ids[0])[1]  # Extract only the Y coordinate
        # Limit the movement of the buttons
        if abs(y_movement) > 1:
            if current_position + y_movement <= 171 and current_position + y_movement >= 130 - (65 * (len(d_room_button_ids) - 6)):
                # Move the buttons
                for button_id in d_room_button_ids:
                    canvas.move(button_id, 0, y_movement)
                last_y_position_d = canvas.canvasy(y)
            elif current_position + math.copysign(1, y_movement) <= 171 and current_position + math.copysign(1, y_movement) >= 130 - (65 * (len(d_room_button_ids) - 6)):
                # Move the buttons by 1 pixel
                for button_id in d_room_button_ids:
                    canvas.move(button_id, 0, math.copysign(1, y_movement))
                last_y_position_d = canvas.canvasy(y)
        

        if abs(drag_start_position_d - current_position) > 20:
            # Disable the buttons
            buttons_enabled_d = False

def drag_other(event):
    global last_y_position_other, dragging_other, buttons_enabled_other
    if dragging_other:
        x, y = window.winfo_pointerxy()
        y_movement = canvas.canvasy(y) - last_y_position_other
        # Get the y position of the first button using the bbox method
        current_position = canvas.bbox(other_room_button_ids[0])[1]  # Extract only the Y coordinate
        # Limit the movement of the buttons
        if len(other_room_button_ids) > 8:
            if abs(y_movement) > 1:
                if current_position + y_movement <= 171 and current_position + y_movement >= 130 - (65 * (len(other_room_button_ids) - 6)):
                    # Move the buttons
                    for button_id in other_room_button_ids:
                        canvas.move(button_id, 0, y_movement)
                    last_y_position_other = canvas.canvasy(y)
                elif current_position + math.copysign(1, y_movement) <= 171 and current_position + math.copysign(1, y_movement) >= 130 - (65 * (len(other_room_button_ids) - 6)):
                    # Move the buttons by 1 pixel
                    for button_id in other_room_button_ids:
                        canvas.move(button_id, 0, math.copysign(1, y_movement))
                    last_y_position_other = canvas.canvasy(y)

        if abs(drag_start_position_other - current_position) > 20:
            # Disable the buttons
            buttons_enabled_other = False

def stop_drag_number(event):
    global dragging_number, buttons_enabled_number
    dragging_number = False

    # Enable the buttons after 200ms by setting the buttons_enabled variable to True
    window.after(200, lambda: enable_buttons_number())

def stop_drag_d(event):
    global dragging_d, buttons_enabled_d
    dragging_d = False

    # Enable the buttons after 200ms by setting the buttons_enabled variable to True
    window.after(200, lambda: enable_buttons_d())

def stop_drag_other(event):
    global dragging_other, buttons_enabled_other
    dragging_other = False

    # Enable the buttons after 200ms by setting the buttons_enabled variable to True
    window.after(200, lambda: enable_buttons_other())


def enable_buttons_number():
    global buttons_enabled_number
    buttons_enabled_number = True

def enable_buttons_d():
    global buttons_enabled_d
    buttons_enabled_d = True

def enable_buttons_other():
    global buttons_enabled_other
    buttons_enabled_other = True









def update_globals(room_name):
    global buttons_enabled_number, buttons_enabled_d, buttons_enabled_other
    if buttons_enabled_number or buttons_enabled_d or buttons_enabled_other:

        # Load the data from the JSON file
        with open('build\\globals.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update the values
        data['timetable_data'] = room_name
        data['timetable_type'] = 'Room'
        data['regenerate_timetable'] = True

        # Write the data back to the JSON file
        with open('build\\globals.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

        print(data)
        print(data['regenerate_timetable'])
        window.destroy()







# Load room data from JSON file
with open('build\\timetableData\\rooms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Separate the rooms into three groups: rooms with only number, rooms starting with the letter D, the rest
rooms = {
    'number': [],
    'D': [],
    'other': []
}

for room in data['rooms']:
    room_name = list(room.keys())[0]
    if room_name[0].isdigit():
        rooms['number'].append(room)
    elif room_name[0] == 'D':
        rooms['D'].append(room)
    else:
        rooms['other'].append(room)

# Sort the number rooms by their number, the D rooms by the number after the D, the other rooms alphabetically
rooms['number'] = sorted(rooms['number'], key=lambda x: int(list(x.keys())[0]))
rooms['D'] = sorted(rooms['D'], key=lambda x: int(list(x.keys())[0][1:]))
rooms['other'] = sorted(rooms['other'], key=lambda x: list(x.keys())[0])

# Create a list of room buttons and their IDs
number_room_buttons = []
number_room_button_ids = []
d_room_buttons = []
d_room_button_ids = []
other_room_buttons = []
other_room_button_ids = []

button_image = PhotoImage(file=relative_to_assets("RoomButton.png"))

# Iterate over rooms and create buttons for each room
for room in rooms['number']:
    room_name = list(room.keys())[0]
    button = Button(image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                    text=room_name, font=("Kanit Light", 20), compound="center",
                    command=lambda room_name=room_name: update_globals(room_name),
                    activebackground="#2F2F2F", activeforeground="#2F2F2F",
                    background="#2F2F2F", foreground="#2F2F2F")
    button.bind("<Button-1>", start_drag_number)
    button.bind("<B1-Motion>", drag_number)
    button.bind("<ButtonRelease-1>", stop_drag_number)
    number_room_buttons.append(button)
    button_id = canvas.create_window(512.0 - 200, 130.0 + 65 * len(number_room_buttons), window=button)
    number_room_button_ids.append(button_id)

for room in rooms['D']:
    room_name = list(room.keys())[0]
    button = Button(image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                    text=room_name, font=("Kanit Light", 20), compound="center",
                    command=lambda room_name=room_name: update_globals(room_name),
                    activebackground="#2F2F2F", activeforeground="#2F2F2F",
                    background="#2F2F2F", foreground="#2F2F2F")
    button.bind("<Button-1>", start_drag_d)
    button.bind("<B1-Motion>", drag_d)
    button.bind("<ButtonRelease-1>", stop_drag_d)
    d_room_buttons.append(button)
    button_id = canvas.create_window(512.0, 130.0 + 65 * len(d_room_buttons), window=button)
    d_room_button_ids.append(button_id)

for room in rooms['other']:
    room_name = list(room.keys())[0]
    button = Button(image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                    text=room_name, font=("Kanit Light", 20), compound="center",
                    command=lambda room_name=room_name: update_globals(room_name),
                    activebackground="#2F2F2F", activeforeground="#2F2F2F",
                    background="#2F2F2F", foreground="#2F2F2F")
    button.bind("<Button-1>", start_drag_other)
    button.bind("<B1-Motion>", drag_other)
    button.bind("<ButtonRelease-1>", stop_drag_other)
    other_room_buttons.append(button)
    button_id = canvas.create_window(512 + 200, 130.0 + 65 * len(other_room_buttons), window=button)
    other_room_button_ids.append(button_id)


room_buttons = number_room_button_ids + d_room_button_ids + other_room_button_ids









# Create a separate canvas for the text and rectangle
text_canvas = Canvas(
    window,
    bg="#2F2F2F",
    height=80,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
text_canvas.place(x=0, y=0)

# Create the rectangle and text on the separate canvas
rect = text_canvas.create_rectangle(
    312.0,
    110.0,
    712.0,
    110.0 + 58 * 65 + 45.0,
    fill="#2F2F2F",
    outline=""
)

text = text_canvas.create_text(
    512.0,
    45.0,
    anchor="center",
    text="Učebny",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)


def start_drag(event):
    start_drag_number(event)
    start_drag_d(event)
    start_drag_other(event)

def drag(event):
    drag_number(event)
    drag_d(event)
    drag_other(event)

def stop_drag(event):
    stop_drag_number(event)
    stop_drag_d(event)
    stop_drag_other(event)

# Bind all of the drag events to the window
window.bind("<Button-1>", start_drag)
window.bind("<B1-Motion>", drag)
window.bind("<ButtonRelease-1>", stop_drag)



window.resizable(False, False)
window.mainloop()
