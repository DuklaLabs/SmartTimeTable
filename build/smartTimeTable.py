import os
from pathlib import Path
from subprocess import Popen
import sys
import time
from time import strftime

from tkinter import Tk, Canvas, Button, PhotoImage, Label
import datetime


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\timetable")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

global timetable_name  # The name of the timetable as a text
global timetable_type  # The type of the timetable (e.g. "Class", "Teacher", "Room")
global timetable_data  # The data of the timetable (e.g. "1.S", "Novák Jan", "46")
global timetable_time_period    # The time period of the timetable (e.g. "Actual", "Next week", "Previous week")


window = Tk()

window.geometry("1024x600")
window.configure(bg="#FFFFFF")
window.title("SmartTimeTable V0.4 by DuklaLabs")
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


image_image_1 = PhotoImage(
    file=relative_to_assets("Timetable.png"))
image_1 = canvas.create_image(
    901.0,
    300.0,
    image=image_image_1
)


dragging = False
last_x_position = 0


def start_drag(event):
    global dragging, last_x_position
    overlapping = canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
    if image_1 in overlapping:
        dragging = True
        last_x_position = event.x


def drag(event):
    global dragging, last_x_position
    if dragging:
        x_movement = event.x - last_x_position
        current_position = canvas.coords(image_1)
        if 197 <= current_position[0] + x_movement <= 901:
            # Move image_1
            canvas.move(image_1, x_movement, 0)
            # Move main_texts
            for row in main_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
            # Move bottom_texts
            for row in bottom_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
            # Move top_texts
            for row in top_texts:
                for text in row:
                    if text is not None:
                        canvas.move(text, x_movement, 0)
        last_x_position = event.x


def stop_drag(event):
    global dragging
    dragging = False

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", stop_drag)



image_image_2 = PhotoImage(
    file=relative_to_assets("WeekdaysBackground.png"))
image_2 = canvas.create_image(
    37.0,
    300.0,
    image=image_image_2
)


image_image_3 = PhotoImage(
    file=relative_to_assets("Weekdays.png"))
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




timetable_name_text = canvas.create_text(17, 10, anchor="nw", text="", fill="#D3D3D3", font=("Inter", 50 * -1))

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



# Create the dates matrix
dates = [[None] * 5 for _ in range(1)]

start_date = datetime.date.today()
for j in range(5):
    date = start_date + datetime.timedelta(days=j)
    dates[0][j] = canvas.create_text(39, 205 + j * 75, anchor="center", text=date.strftime("%d.%m."), fill="#D3D3D3", font=("Inter Light", 20 * -1))




button_image_1 = PhotoImage(
    file=relative_to_assets("CreditsButton.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Popen([sys.executable, str(OUTPUT_PATH / "credits.py")]),
    relief="flat"
)
button_1.place(
    x=955.0,
    y=530.0,
    width=65.0,
    height=65.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("InfoButton.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=16.0,
    y=11.0,
    width=45.0,
    height=55.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("ClassesButton.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Popen([sys.executable, str(OUTPUT_PATH / "classes.py")]),
    relief="flat"
)
button_3.place(
    x=452.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("TeachersButton.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Popen([sys.executable, str(OUTPUT_PATH / "teachers.py")]),
    relief="flat"
)
button_4.place(
    x=272.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("RoomsButton.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Popen([sys.executable, str(OUTPUT_PATH / "rooms.py")]),
    relief="flat"
)
button_7.place(
    x=632.0,
    y=540.0,
    width=150.0,
    height=45.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("TimetableTypeButton.png"))
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
    width=150.0,
    height=45.0
)



button_image_6 = PhotoImage(
    file=relative_to_assets("RefreshButton.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: window.destroy(),
    relief="flat"
)
button_6.place(
    x=964.0,
    y=14.0,
    width=50.0,
    height=50.0
)

window.resizable(False, False)


canvas.tag_raise(image_2)
canvas.tag_raise(image_3)
#raise all dates
# Raise all dates
for row in dates:
    for date in row:
        if date is not None:
            canvas.tag_raise(date)


change_timetable_name("IT Laboratoř 46")
window.mainloop()
