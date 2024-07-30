from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Toplevel, Tk
import textwrap
import json
import globals

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "credits"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

def show_timetable_info(master):
    
    # Create a secondary window
    window = Toplevel(master)
    window.geometry("1024x600")
    window.configure(bg="#FFFFFF")
    window.title("SmartTimeTable V0.4 - Credits")
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

    button_image_1 = PhotoImage(file=relative_to_assets("Exit.png"))
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: window.destroy(),
        relief="flat"
    )
    button_1.place(x=930.0, y=25.0, width=60.0, height=60.0)

    timetable_type = globals.timetable_type.lower()
    timetable_data = globals.timetable_data

    if timetable_type == "class":
        with open(OUTPUT_PATH / "timetableData" / "info" / "classesInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["classes"]
            timetable_info = next((class_info for class_info in timetable_info_list if timetable_data in class_info), None)

    elif timetable_type == "teacher":
        with open(OUTPUT_PATH / "timetableData" / "info" / "teachersInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["teachers"]
            timetable_info = next((teacher_info for teacher_info in timetable_info_list if timetable_data in teacher_info), None)

    elif timetable_type == "room":
        with open(OUTPUT_PATH / "timetableData" / "info" / "roomsInfo.json", "r", encoding="utf-8") as file:
            timetable_info_list = json.load(file)["rooms"]
            timetable_info = next((room_info for room_info in timetable_info_list if timetable_data in room_info), None)

    if timetable_info is not None:
        timetable_name = timetable_info[timetable_data].get("name", "Default Name")
    else:
        timetable_name = "Unknown Timetable"

    canvas.create_text(
        512.0,
        60.0,
        anchor="center",
        text=timetable_name,
        fill="#D24B49",
        font=("Kanit Regular", 50 * -1)
    )

    info_text = timetable_info[timetable_data].get("info", "No info available") if timetable_info else "No info available"
    wrapped_text = textwrap.fill(info_text, width=60)
    lines = wrapped_text.split("\n")
    y = 150

    for line in lines:
        canvas.create_text(512, y, anchor="n", text=line, fill="#FFFFFF", font=("Kanit", 32 * -1))
        y += 35

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    root = Tk()
    show_timetable_info(root)