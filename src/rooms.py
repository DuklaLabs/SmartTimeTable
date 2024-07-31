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
    window.title("SmartTimeTable V2.1 by DuklaLabs - Classes")
    window.attributes("-fullscreen", True)
    window.config(cursor="none")
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





    # Implement dragging for the button lists
    dragging = False
    last_y_position = 0
    buttons_enabled = True

    def start_drag(event):
        nonlocal dragging, last_y_position, buttons_enabled
        dragging = True
        x, y = window.winfo_pointerxy()
        last_y_position = canvas.canvasy(y)
        drag_start_position = event.y

    def drag(event):
        nonlocal last_y_position, dragging, buttons_enabled
        if dragging:
            x, y = window.winfo_pointerxy()
            y_movement = canvas.canvasy(y) - last_y_position
            number_current_position = canvas.bbox(number_room_button_ids[0])[1]  # Extract only the Y coordinate
            d_current_position = canvas.bbox(d_room_button_ids[0])[1]  # Extract only the Y coordinate

            if 500 - 50 * len(number_room_buttons) <= number_current_position + y_movement <= 120:
                for button_id in number_room_button_ids:
                    canvas.move(button_id, 0, y_movement)
                last_y_position = canvas.canvasy(y)

            if y_movement > 30 or y_movement < -30:
                buttons_enabled = False

            if 500 - 50 * len(d_room_buttons) <= d_current_position + y_movement <= 120:
                for button_id in d_room_button_ids:
                    canvas.move(button_id, 0, y_movement)
                last_y_position = canvas.canvasy(y)

    def stop_drag(event):
        nonlocal dragging, buttons_enabled
        dragging = False
        window.after(200, lambda: enable_buttons())

    def enable_buttons():
        nonlocal buttons_enabled
        buttons_enabled = True

    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind("<ButtonRelease-1>", stop_drag)




    def update_globals(room_name):
        nonlocal buttons_enabled
        if buttons_enabled:

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
    d_room_buttons = []
    number_room_button_ids = []
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
        button.bind("<Button-1>", start_drag)
        button.bind("<B1-Motion>", drag)
        button.bind("<ButtonRelease-1>", stop_drag)
        button_id = canvas.create_window(412-70, 120 + 50 * len(number_room_buttons), window=button)
        number_room_buttons.append(button)
        number_room_button_ids.append(button_id)

    for room in rooms["D"]:
        room_name = list(room.keys())[0]
        button = Button(window, image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                        text=room_name, font=("Kanit Light", 20), compound="center",
                        command=lambda room_name=room_name: update_globals(room_name),
                        activebackground="#2F2F2F", activeforeground="#2F2F2F",
                        background="#2F2F2F", foreground="#2F2F2F")
        button.bind("<Button-1>", start_drag)
        button.bind("<B1-Motion>", drag)
        button.bind("<ButtonRelease-1>", stop_drag)
        button_id = canvas.create_window(612+70, 120 + 50 * len(d_room_buttons), window=button)
        d_room_buttons.append(button)
        d_room_button_ids.append(button_id)

    


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

    window.mainloop()



if __name__ == "__main__":
    root = Tk()
    open_rooms_menu(root)
    root.mainloop()

