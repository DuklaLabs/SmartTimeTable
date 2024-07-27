# A menu for selecting a teacher
# The menu is made up of buttons, each representing a teacher organized in a list that can be scrolled through by dragging

from pathlib import Path
import json
from tkinter import Toplevel, Canvas, Button, PhotoImage, Tk
import globals
from playVideo import play_video

def open_teachers_menu(master):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "teachers"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Create a secondary window
    window = Toplevel(master)
    window.geometry("1024x600")
    window.configure(bg="#FFFFFF")
    window.title("SmartTimeTable V0.4 by DuklaLabs - Teachers")
    window.attributes("-fullscreen", True)
    # window.config(cursor="none")
    window.lift()

    # Create a canvas for the secondary window
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

    # Create a button to exit the secondary window
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





    # Implement dragging for the button list
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
            current_position = canvas.bbox(teacher_buttons[0])[1]  # Extract only the Y coordinate

            if -3200 <= current_position + y_movement <= 120:
                for button in teacher_buttons:
                    canvas.move(button, 0, y_movement)
                last_y_position = canvas.canvasy(y)

            if y_movement > 30 or y_movement < -30:
                buttons_enabled = False

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





    # Create buttons for each teacher and assign a function to each
    def update_globals(teacher_name):
        nonlocal buttons_enabled     
        if buttons_enabled:
            if teacher_name == "Požárek Pavel":
                play_video("Pozi.mp4")
                window.after(12000, lambda: window.destroy())
                return

            globals.timetable_data = teacher_name
            globals.timetable_type = "Teacher"
            globals.regenerate_timetable = True

            print("Teacher selected: " + globals.timetable_data)

            if window.winfo_exists():
                window.destroy()





    with open(OUTPUT_PATH / "timetableData" / "teachers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    teacher_buttons = []
    button_image = PhotoImage(file=relative_to_assets("TeacherButton.png"))

    for teacher in data["teachers"]:
        teacher_name = list(teacher.keys())[0]

        button = Button(window, image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                        text=teacher_name, font=("Kanit Light", 20), compound="center",
                        command=lambda teacher_name=teacher_name: update_globals(teacher_name),
                        activebackground="#2F2F2F", activeforeground="#2F2F2F",
                        background="#2F2F2F", foreground="#2F2F2F")

        button.bind("<Button-1>", start_drag)
        button.bind("<B1-Motion>", drag)
        button.bind("<ButtonRelease-1>", stop_drag)

        button_id = canvas.create_window(512.0, 130.0 + 65 * len(teacher_buttons), window=button)
        teacher_buttons.append(button_id)

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
        text="Učitelé",
        fill="#D24B49",
        font=("Kanit Regular", 50 * -1)
    )

    window.bind("<Button-1>", start_drag)
    window.bind("<B1-Motion>", drag)
    window.bind("<ButtonRelease-1>", stop_drag)

    window.resizable(False, False)
    window.mainloop()