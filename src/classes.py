from pathlib import Path
import json
from tkinter import Toplevel, Canvas, Button, PhotoImage, Tk
import globals

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "classes"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_classes_menu(master):
    # Create a secondary window
    window = Toplevel(master)
    window.geometry("1024x600")
    window.configure(bg="#FFFFFF")
    window.title("SmartTimeTable V0.4 by DuklaLabs - Classes")
    window.config(cursor="none")
    window.attributes("-fullscreen", True)
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
        nonlocal dragging, last_y_position
        dragging = True
        last_y_position = event.y

    def drag(event):
        nonlocal last_y_position
        if dragging:
            delta_y = event.y - last_y_position
            canvas.move("all", 0, delta_y)
            last_y_position = event.y

    def stop_drag(event):
        nonlocal dragging
        dragging = False

    def enable_buttons():
        nonlocal buttons_enabled
        buttons_enabled = True

    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind("<ButtonRelease-1>", stop_drag)

    # Create buttons for each class and assign a function to each
    def update_globals(class_name):
        nonlocal buttons_enabled
        if buttons_enabled:
            globals.timetable_data = class_name
            globals.timetable_type = "Class"
            globals.regenerate_timetable = True

            print("Class selected: " + globals.timetable_data)

            if window.winfo_exists():
                window.destroy()

    # Create the button list as a grid
    with open(OUTPUT_PATH / "timetableData" / "classes.json", "r", encoding="utf-8") as f:
        class_data = json.load(f)

    button_image = PhotoImage(file=relative_to_assets("ClassButton.png"))
    class_buttons_ = []

    # Extract class names
    class_names = [list(class_dict.keys())[0] for class_dict in class_data["classes"]]

    num_cols = 4

    num_rows = len(class_names) // num_cols + 1

    # Initialize the class_buttons list
    class_buttons = [[None] * num_cols for _ in range(num_rows)]

    # Iterate over class names
    for i, class_name in enumerate(class_names):
        class_buttons_.append(Button(window, image=button_image, text=class_name, font=("Kanit Light", 23), compound="center", borderwidth=0, highlightthickness=0, command=lambda class_name=class_name: update_globals(class_name), relief="flat"))
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


if __name__ == "__main__":
    root = Tk()
    open_classes_menu(root)



