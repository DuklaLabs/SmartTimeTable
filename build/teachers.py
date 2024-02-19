from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar, VERTICAL, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\teachers")


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

canvas_buttons = Canvas(window, bg="#2F2F2F", highlightthickness=0)
canvas_buttons.place(x=0, y=100, width=1024, height=500)  # Adjust the position and size as needed
frame_buttons = Frame(canvas_buttons, bg="#2F2F2F")
canvas_buttons.create_window((0, 0), window=frame_buttons, anchor="nw")


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

teacher_buttons = []
button_image = PhotoImage(file=relative_to_assets("TeacherButton.png"))

for i in range(58):
    button = Button(frame_buttons, image=button_image, borderwidth=0, bd=0, highlightthickness=0, relief="flat",
                    text="Aaaaaaaa Bbbbbbbbb", font=("Kanit Light", 20), compound="center",
                    command=lambda i=i: print(f"Button {i+1} clicked"), 
                    activebackground="#2F2F2F", activeforeground="#2F2F2F",
                    background="#2F2F2F", foreground="#2F2F2F")
    button.pack(pady=9, anchor='center')

frame_buttons.update()
canvas_buttons.configure(scrollregion=canvas_buttons.bbox("all"))

dragging = False
last_y_position = 0
y_movement = 0

def start_drag(event):
    global dragging, last_y_position
    dragging = True
    last_y_position = event.y

def on_touch_drag(event):
    global dragging, last_y_position, y_movement
    if dragging:
        y_movement += event.y - last_y_position
        if abs(y_movement) > 5:  # Only move when y_movement is larger than 5 pixels
            frame_buttons.place(x=canvas_buttons.winfo_width() // 2, y=(frame_buttons.winfo_y() + y_movement), anchor="n")
            y_movement = 0
        last_y_position = event.y

def stop_drag(event):
    global dragging
    dragging = False

frame_buttons.bind("<Button-1>", start_drag)
frame_buttons.bind("<B1-Motion>", on_touch_drag)
frame_buttons.bind("<ButtonRelease-1>", stop_drag)

def bind_drag_events(widget):
    widget.bind("<Button-1>", start_drag)
    widget.bind("<B1-Motion>", on_touch_drag)
    widget.bind("<ButtonRelease-1>", stop_drag)

# Bind drag events to all buttons in frame_buttons
for button in frame_buttons.winfo_children():
    bind_drag_events(button)

canvas_buttons.create_window((canvas_buttons.winfo_width() // 2, 0), window=frame_buttons, anchor="n")

canvas_buttons.create_window((canvas_buttons.winfo_width() // 2, 0), window=frame_buttons, anchor="n")



text = canvas.create_text(
    512.0,
    45.0,
    anchor="center",
    text="Učitelé",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)

# Place a rectangle behind the text with the same color as the canvas
rect = canvas.create_rectangle(
    312.0,
    110.0,
    712.0,
    110.0 + 58 * 65 + 45.0,
    fill="#2F2F2F",
    outline=""
)

# Place the rectangle in front of everything then do the same for the text
canvas.tag_raise("rect")
canvas.tag_raise("text")

window.resizable(False, False)
window.mainloop()
