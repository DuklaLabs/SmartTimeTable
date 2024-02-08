import os
from pathlib import Path
from subprocess import Popen
import sys
import time
from time import strftime

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x600")
window.configure(bg = "#FFFFFF")
window.title("SmartTimeTable V0.4")
window.attributes("-fullscreen", True)


canvas = Canvas(
    window,
    bg = "#2F2F2F",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1024.0,
    600.0,
    fill="#2F2F2F",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    901.0,
    300.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    37.0,
    300.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    38.0,
    323.0,
    image=image_image_3
)







# Create the timetable texts
main_ = []
top_ = []
bottom_ = []

main_texts = [[None] * 5 for _ in range(11)]
bottom_texts = [[None] * 5 for _ in range(11)]
top_texts = [[None] * 5 for _ in range(11)]

for i in range(11):
    for j in range(5):
        main_.append(canvas.create_text(116 + i * 150, 190 + j * 75, anchor="center", text="XXc", fill="#D3D3D3", font=("Inter Light", 30 * -1)))
        main_texts[i][j] = main_[-1]

for i in range(11):
    for j in range(5):
        bottom_.append(canvas.create_text(183 + i * 150, 197 + j * 75, anchor="center", text="Xx", fill="#D3D3D3", font=("Inter Light", 23 * -1)))
        bottom_texts[i][j] = bottom_[-1]

for i in range(11):
    for j in range(5):
        top_.append(canvas.create_text(183 + i * 150, 172 + j * 75, anchor="center", text="0.XX P0", fill="#D3D3D3", font=("Inter Light", 18 * -1)))
        top_texts[i][j] = top_[-1]

timetable_name_text = canvas.create_text(15, 10, anchor="nw", text="", fill="#D3D3D3", font=("Inter", 50 * -1))

def change_timetable_name(new_text):
    global timetable_name
    timetable_name = new_text
    canvas.itemconfigure(timetable_name_text, text=new_text)







#Create the clock
def time():
    #Get the current time and date and format it to 12:00   31.12.2024
    string = strftime('%H:%M   %d.%m.%Y')
    lbl.configure(text=string)
    lbl.after(1000, time)
 

lbl = Label(window, font=('Inter', 28), background = '#303030', foreground = '#B6B6B6')

lbl.place(x=770, y=40, anchor="center")
time()



#Create the dates
for i in range(5):
    canvas.create_text(40, 205 + i * 75, anchor="center", text="00.00.", fill="#D3D3D3", font=("Inter Light", 20 * -1))








image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    986.0,
    562.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    987.0,
    563.0,
    image=image_image_5
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=887.0,
    y=535.0,
    width=45.0,
    height=55.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=632.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=452.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=272.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=43.0,
    y=540.0,
    width=80.0,
    height=20.0
)



button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    #open the credits window when clicked using the Popen function
    command = lambda: Popen([sys.executable, str(OUTPUT_PATH / "credits.py")]),
    relief="flat"
)
button_6.place(
    x=964.0,
    y=14.0,
    width=50.0,
    height=50.0
)

window.resizable(False, False)



change_timetable_name("IT Laboratoř 46")
window.mainloop()
