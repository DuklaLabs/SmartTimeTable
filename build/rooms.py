from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Majrich\Documents\Code\SmartTimeTable\build\assets\rooms")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x600")
window.configure(bg="#FFFFFF")
window.title("SmartTimeTable V0.4 by DuklaLabs - Rooms")
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


numberedRoomButtons = []
otherRoomButtons = []
button_image = PhotoImage(file=relative_to_assets("RoomButton.png"))

for i in range(30):
    numberedRoomButtons.append(Button(image=button_image, borderwidth=0, highlightthickness=0, command=lambda i=i: print(f"button_{i} clicked"), relief="flat"))
    numberedRoomButtons[i].place(x=317.0, y=100.0 + (i * 65), width=140.0, height=45.0)

for i in range(20):
    otherRoomButtons.append(Button(image=button_image, borderwidth=0, highlightthickness=0, command=lambda i=i: print(f"button_{i} clicked"), relief="flat"))
    otherRoomButtons[i].place(x=567.0, y=100.0 + (i * 65), width=140.0, height=45.0)


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


canvas.create_text(
    512.0,
    45.0,
    anchor="center",
    text="Učebny",
    fill="#D24B49",
    font=("Kanit Regular", 50 * -1)
)
window.resizable(False, False)
window.mainloop()
