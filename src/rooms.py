from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel
import json
import globals

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "rooms"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path



def open_rooms_menu(master):

    # Create a secondary window
    window = Toplevel(master)
    window.geometry("1024x600")
    window.configure(bg="#FFFFFF")
    window.title("SmartTimeTable V0.4 by DuklaLabs - Classes")
    window.attributes("-fullscreen", True)
    window.lift()

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
        window,
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


    def update_globals(room_name):
        nonlocal buttons_enabled_number, buttons_enabled_d
        if buttons_enabled_number or buttons_enabled_d:

            # Load the data from the JSON file
            with open(OUTPUT_PATH / "globals.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update the values
            globals.timetable_data = room_name
            globals.timetable_type = "Room"
            globals.regenerate_timetable = True

            print("Room selected: " + globals.timetable_data)
            window.destroy()


    # Load room data from JSON file
    with open(OUTPUT_PATH / "timetableData" / "rooms.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Separate the rooms into two groups: number rooms and D rooms
    rooms = {
        "number": [],
        "D": []
    }

    for room in data["rooms"]:
        room_name = list(room.keys())[0]
        if room_name[0].isdigit():
            rooms["number"].append(room)
        elif room_name[0] == "D":
            rooms["D"].append(room)


    # Sort the number rooms by their number, the D rooms by the number after the D, the other rooms alphabetically
    rooms["number"] = sorted(rooms["number"], key=lambda x: int(list(x.keys())[0]))
    rooms["D"] = sorted(rooms["D"], key=lambda x: int(list(x.keys())[0][1:]))

    # Create a list of room buttons and their IDs
    number_room_buttons = []
    number_room_button_ids = []
    d_room_buttons = []
    d_room_button_ids = []

    button_image = PhotoImage(file=relative_to_assets("RoomButton.png"))

    # Iterate over rooms and create buttons for each room
    for room in rooms["number"]:
        room_name = list(room.keys())[0]
        button = Button(window, image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                        text=room_name, font=("Kanit Light", 20), compound="center",
                        command=lambda room_name=room_name: update_globals(room_name),
                        activebackground="#2F2F2F", activeforeground="#2F2F2F",
                        background="#2F2F2F", foreground="#2F2F2F")
        number_room_buttons.append(button)
        number_room_button_ids.append(button.place(x=312-70, y=100 + 50 * len(number_room_buttons)))

    for room in rooms["D"]:
        room_name = list(room.keys())[0]
        button = Button(window, image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                        text=room_name, font=("Kanit Light", 20), compound="center",
                        command=lambda room_name=room_name: update_globals(room_name),
                        activebackground="#2F2F2F", activeforeground="#2F2F2F",
                        background="#2F2F2F", foreground="#2F2F2F")
        d_room_buttons.append(button)
        d_room_button_ids.append(button.place(x=712-70, y=100 + 50 * len(d_room_buttons)))

    
    # Make the two list separately scrollable

    dragging_number = False
    last_y_position_number = 0
    buttons_enabled_number = True

    dragging_d = False
    last_y_position_d = 0
    buttons_enabled_d = True

    def start_drag_number(event):
        nonlocal dragging_number, last_y_position_number
        dragging_number = True
        last_y_position_number = event.y

    def drag_number(event):
        nonlocal last_y_position_number
        if dragging_number:
            delta_y = event.y - last_y_position_number
            canvas.move("all", 0, delta_y)
            last_y_position_number = event.y

    def stop_drag_number(event):
        nonlocal dragging_number
        dragging_number = False


    def start_drag_d(event):
        nonlocal dragging_d, last_y_position_d
        dragging_d = True
        last_y_position_d = event.y

    def drag_d(event):
        nonlocal last_y_position_d
        if dragging_d:
            delta_y = event.y - last_y_position_d
            canvas.move("all", 0, delta_y)
            last_y_position_d = event.y
    
    def stop_drag_d(event):
        nonlocal dragging_d
        dragging_d = False

    def enable_buttons_number():
        nonlocal buttons_enabled_number
        buttons_enabled_number = True

    def enable_buttons_d():
        nonlocal buttons_enabled_d
        buttons_enabled_d = True

    canvas.bind("<Button-1>", start_drag_number)
    canvas.bind("<B1-Motion>", drag_number)
    canvas.bind("<ButtonRelease-1>", stop_drag_number)

    canvas.bind("<Button-1>", start_drag_d)
    canvas.bind("<B1-Motion>", drag_d)
    canvas.bind("<ButtonRelease-1>", stop_drag_d)





    window.mainloop()



