from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

import globals

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\classes")


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

button_image = PhotoImage(file=relative_to_assets("ClassButton.png"))
class_buttons_ = []
class_buttons = [[None] * 4 for _ in range(4)]

for i in range(4):
    for j in range(4):
        class_buttons_.append(Button(image=button_image, borderwidth=0, highlightthickness=0, command=lambda i=i, j=j: globals.timetable_data.set(f"button_{i*4+j+1}"), relief="flat"))
        class_buttons[i][j] = class_buttons_[-1]
        class_buttons[i][j].place(x=144.0 + j * 195, y=117.0 + i * 100, width=150.0, height=65.0)



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
