from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar, VERTICAL, Frame
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "teachers"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x600")
window.configure(bg="#FFFFFF")
window.title("SmartTimeTable V0.4 by DuklaLabs - Teachers")
window.attributes("-fullscreen", True)
#window.config(cursor="none")


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



dragging = False
last_y_position = 0
buttons_enabled = True

def start_drag(event):
    global dragging, last_y_position, buttons_enabled
    dragging = True
    x, y = window.winfo_pointerxy()
    last_y_position = canvas.canvasy(y)
    global drag_start_position
    drag_start_position = event.y

def drag(event):
    global last_y_position, dragging, buttons_enabled
    if dragging:
        x, y = window.winfo_pointerxy()
        y_movement = canvas.canvasy(y) - last_y_position
        # Get the y position of the first button using the bbox method
        current_position = canvas.bbox(teacher_buttons[0])[1]  # Extract only the Y coordinate

        if -3200 <= current_position + y_movement <= 120:
            # Move the buttons
            for button in teacher_buttons:
                canvas.move(button, 0, y_movement)
            last_y_position = canvas.canvasy(y)

        if abs(drag_start_position - current_position) > 20:
            # Disable the buttons
            buttons_enabled = False


def stop_drag(event):
    global dragging, buttons_enabled
    dragging = False

    # Enable the buttons after 200ms by setting the buttons_enabled variable to True
    window.after(200, lambda: enable_buttons())

def enable_buttons():
    global buttons_enabled
    buttons_enabled = True

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", stop_drag)




def update_globals(teacher_name):
    global buttons_enabled
    print(buttons_enabled)
    if buttons_enabled:

        # Load the data from the JSON file
        with open(OUTPUT_PATH / "globals.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Update the values
        data["timetable_data"] = teacher_name
        data["timetable_type"] = "Teacher"
        data["regenerate_timetable"] = True

        # Write the data back to the JSON file
        with open(OUTPUT_PATH / "globals.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

        print(data)
        print(data["regenerate_timetable"])
        window.destroy()



# Load teacher data from JSON file
with open(OUTPUT_PATH / "timetableData" / "info" / "teachersInfo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

teacher_buttons = []
teacher_buuton_ids = []
button_image = PhotoImage(file=relative_to_assets("TeacherButton.png"))

# Iterate over teacher data
for teacher in data["teachers"]:
    # Get teacher name
    teacher_name = list(teacher.keys())[0]

    # Create button for teacher
    button = Button(image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                    text=teacher_name, font=("Kanit Light", 20), compound="center",
                    command=lambda teacher_name=teacher_name: update_globals(teacher_name),
                    activebackground="#2F2F2F", activeforeground="#2F2F2F",
                    background="#2F2F2F", foreground="#2F2F2F")

    # Bind the drag events to the button
    button.bind("<Button-1>", start_drag)
    button.bind("<B1-Motion>", drag)
    button.bind("<ButtonRelease-1>", stop_drag)

    # Add the button to the canvas and get its ID
    button_id = canvas.create_window(512.0, 130.0 + 65 * len(teacher_buttons), window=button)


    # Add button ID to list
    teacher_buttons.append(button_id)









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
    text="Učitelé",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)


# Bind the drag events to the window instead of the canvas
window.bind("<Button-1>", start_drag)
window.bind("<B1-Motion>", drag)
window.bind("<ButtonRelease-1>", stop_drag)


window.resizable(False, False)
window.mainloop()
