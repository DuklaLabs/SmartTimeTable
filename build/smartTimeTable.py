import os
from pathlib import Path
from subprocess import Popen
import sys
import time
from time import strftime
from tkinter import Tk, Canvas, Button, PhotoImage, Label
import datetime
import json
import asyncio
from PIL import Image, ImageTk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets\\timetable")

with open(OUTPUT_PATH / "config.json", 'r', encoding='utf-8') as f:
    config = json.load(f)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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




main_ = []
top_ = []
bottom_ = []

main_texts = [[None] * 5 for _ in range(11)]
bottom_texts = [[None] * 5 for _ in range(11)]
top_texts = [[None] * 5 for _ in range(11)]

position_offset = 901


def generate_timetable():
    # Destroy the previous timetable
    destroy_timetable()

    # Define the mapping from timetable_type to folder name
    type_to_folder = {"teacher": "teachers", "class": "classes", "room": "rooms"}

    # Load the data from the JSON file
    with open('build\\globals.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Construct the file path
    timetable_type = data['timetable_type'].lower()
    timetable_data = data['timetable_data']
    timetable_period = data['timetable_time_period'].lower()

    file_path = f"build\\timetableData\\{type_to_folder[timetable_type]}\\{timetable_data}\\{timetable_period}.json"
    print(file_path)

    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        timetable_data = json.load(file)

    # Define the mapping from timetable_type to text fields
    type_to_text_fields = {
        "teacher": {"main": "subject", "top": "room", "bottom": "group"},
        "class": {"main": "subject", "top": "room", "bottom": "teacher"},
        "room": {"main": "subject", "top": "teacher", "bottom": "group"},
    }

    text_fields = type_to_text_fields[timetable_type]

    # Get the current position of the timetable
    current_position = canvas.coords(image_1)[0]

    # Use the data from the JSON file to create the timetable
    for j in range(5):
        for i in range(11):
            lesson = timetable_data.get(str(j*11 + i), [{}])[0]  # Get the lesson
            main_text = lesson.get(text_fields["main"], "").replace(" celá", "")
            bottom_text = lesson.get(text_fields["bottom"], "").replace(" celá", "")
            top_text = lesson.get(text_fields["top"], "").replace(" celá", "")
            main_.append(canvas.create_text(current_position - position_offset + 120 + i * 150, 190 + j * 75, anchor="center", text=main_text, fill="#D3D3D3", font=("Inter Light", 30 * -1)))
            main_texts[i][j] = main_[-1]
            if len(bottom_text) <= 4:
                bottom_size = 20
            else:
                bottom_size = 17
            bottom_.append(canvas.create_text(current_position - position_offset + 183 + i * 150, 200 + j * 75, anchor="center", text=bottom_text, fill="#D3D3D3", font=("Inter", bottom_size * -1)))
            bottom_texts[i][j] = bottom_[-1]
            top_.append(canvas.create_text(current_position - position_offset + 183 + i * 150, 175 + j * 75, anchor="center", text=top_text, fill="#D3D3D3", font=("Inter Light", 20 * -1)))
            top_texts[i][j] = top_[-1]

    canvas.tag_raise(image_2)
    canvas.tag_raise(image_3)
    # Raise all dates
    for row in dates:
        for date in row:
            if date is not None:
                canvas.tag_raise(date)

    #set the regenarate timetable variable in globals.json to false
    data['regenerate_timetable'] = False
    with open('build\\globals.json', 'w') as f:
        json.dump(data, f)





def destroy_timetable():
    for row in main_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)
    for row in bottom_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)
    for row in top_texts:
        for text in row:
            if text is not None:
                canvas.delete(text)


timetable_name_text = canvas.create_text(80, 10, anchor="nw", text="", fill="#D3D3D3", font=("Inter", 50 * -1))

def change_timetable_name(new_text):
    global timetable_name
    timetable_name = new_text
    canvas.itemconfigure(timetable_name_text, text=new_text)




#Create the clock
def clock():
    #Get the current time and date and format it to 12:00   31.12.2024
    string = strftime('%H:%M   %d.%m.%Y')
    lbl.configure(text=string)
    lbl.after(1000, clock)


lbl = Label(window, font=('Inter', 28), background = '#303030', foreground = '#B6B6B6')

lbl.place(x=770, y=40, anchor="center")
clock()



import json

# Create the dates matrix
dates = [[None] * 5 for _ in range(1)]

def change_timetable_time_period():
    # Load the data from the JSON file
    with open('build\\globals.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update the values
    if data['timetable_time_period'] == "Actual":
        data['timetable_time_period'] = "Next"
        timetable_time_period_label.config(text="Příští", bg="#D9D9D9", fg='#000000', font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()
        start_date = datetime.date.today()
        # Calculate the offset to the next Monday
        offset = (7 - start_date.weekday()) % 7
        for j in range(5):
            date = start_date + datetime.timedelta(days=j + offset)
            dates[0][j] = canvas.create_text(39, 205 + j * 75, anchor="center", text=date.strftime("%d.%m."), fill="#D3D3D3", font=("Inter Light", 20 * -1))

    elif data['timetable_time_period'] == "Next":
        data['timetable_time_period'] = "Permanent"
        timetable_time_period_label.config(text="Stálý", bg="#D9D9D9", fg='#000000', font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()

    elif data['timetable_time_period'] == "Permanent":
        data['timetable_time_period'] = "Actual"
        timetable_time_period_label.config(text="Aktuální", bg="#D9D9D9", fg='#000000', font=("Kanit", 30 * -1), anchor="center")
        destroy_dates()
        start_date = datetime.date.today()
        # Calculate the offset to this week's Monday
        offset = ((7 - start_date.weekday()) % 7) - 7
        for j in range(5):
            date = start_date + datetime.timedelta(days=j + offset)
            dates[0][j] = canvas.create_text(39, 205 + j * 75, anchor="center", text=date.strftime("%d.%m."), fill="#D3D3D3", font=("Inter Light", 20 * -1))

    data['regenerate_timetable'] = True

    # Write the data back to the JSON file
    with open('build\\globals.json', 'w', encoding= 'utf-8') as f:
        json.dump(data, f)




def destroy_dates():
    # delete the dates if they exist
    for j in range(5):
        if dates[0][j] is not None:
            canvas.delete(dates[0][j])
            dates[0][j] = None
            window.update()



def rotate_image(image, angle):
    rotated_image = image.rotate(angle)
    return ImageTk.PhotoImage(rotated_image)

def update_image():
    global angle, photo_image, canvas, loading
    angle = (angle - 3) % 360  # Update the angle
    photo_image = rotate_image(image, angle)  # Rotate the image
    canvas.itemconfig(loading, image=photo_image)  # Update the image on the canvas
    window.after(10, update_image)  # Call this function again after 100 ms


image = Image.open(relative_to_assets("Loading.png"))
photo_image = ImageTk.PhotoImage(image)
loading = canvas.create_image(512, 300, image=photo_image)
angle = 0
# Hide the loading image
canvas.itemconfig(loading, state="hidden")




def fetch_data():
    # Load the data from the JSON file
    with open('build\\globals.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['fetch_data'] = True

    # Write the data back to the JSON file
    with open('build\\globals.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    # Show the Loading image in the middle of the screen an make it spin until fetch_data is set to False by another script
    global image, photo_image, canvas, loading, angle

    # Load the image using PIL
    image = Image.open(relative_to_assets("Loading.png"))

    # Resize the image to 30% of its original size
    width, height = image.size
    image = image.resize((int(width * 0.4), int(height * 0.4)))

    # Flip the image vertically
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Create a PhotoImage object from the PIL image
    photo_image = ImageTk.PhotoImage(image)

    # Add the image to the canvas
    loading = canvas.create_image(512, 300, image=photo_image)

    # Place the loading image on top of everything else
    canvas.tag_raise(loading)

    # Initialize the angle
    angle = 0

    # Start the rotation
    update_image()

    # Start the getTimeTableData.py script
    Popen([sys.executable, str(OUTPUT_PATH / "getTimeTableData.py")])

    # Wait until the fetch_data is set to False
    check_fetch_data()

def check_fetch_data():
    with open('build\\globals.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data['fetch_data']:
        # If fetch_data is still True, check again after 1 second
        window.after(1000, check_fetch_data)
    else:
        # If fetch_data is False, hide the loading image and regenerate the timetable
        canvas.itemconfig(loading, state="hidden")
        generate_timetable()
    


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
    command=lambda: change_timetable_time_period(),
    relief="flat",
    activeforeground='#000000',
    activebackground="#D9D9D9"
)
button_5.place(
    x=43.0,
    y=540.0,
    width=150.0,
    height=45.0
)

timetable_time_period_label = Label(text="Aktuální", bg="#D9D9D9", fg='#000000', font=("Kanit", 30 * -1), anchor="center")
timetable_time_period_label.place(
    x=43.0 + 75.0,
    y=540.0 + 22.5,
    anchor="center"
)
timetable_time_period_label.bind("<Button-1>", lambda e: button_5.invoke())


button_image_6 = PhotoImage(
    file=relative_to_assets("RefreshButton.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: fetch_data(),
    relief="flat"
)
button_6.place(
    x=964.0,
    y=14.0,
    width=50.0,
    height=50.0
)

window.resizable(False, False)

# Set the timetable time period to Actual by writing permanent to the globals.json file an then calling the change_timetable_time_period function
with open('build\\globals.json', 'r') as f:
    data = json.load(f)
    data['timetable_time_period'] = "Permanent"
    with open('build\\globals.json', 'w') as f:
        json.dump(data, f)
change_timetable_time_period()

generate_timetable()

def check_and_regenerate():
    with open('build\\globals.json', 'r') as f:
        data = json.load(f)
        #print(data)
        #print(data['regenerate_timetable'])
    if data['regenerate_timetable'] == True:
        # Your code here
        print("Regenerating")
        generate_timetable()
        # refresh the window
        window.update()

    window.after(250, check_and_regenerate)

# Start checking
check_and_regenerate()


change_timetable_name(config["timetableName"])

canvas.tag_raise(image_2)
canvas.tag_raise(image_3)
#raise all dates
# Raise all dates
for row in dates:
    for date in row:
        if date is not None:
            canvas.tag_raise(date)

window.mainloop()
