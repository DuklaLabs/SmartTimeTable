# credits.py

from pathlib import Path
from subprocess import Popen
import sys
from tkinter import Tk, Canvas, Toplevel, Text, Button, PhotoImage
from PIL import Image,ImageTk

from playVideo import play_video

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "credits"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def show_credits(master):

    window = Toplevel(master)
    window.geometry("1024x600")
    window.configure(bg = "#FFFFFF")
    window.title("SmartTimeTable V2.1 - Credits")
    window.attributes("-fullscreen", True)
    window.config(cursor = "none")

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

    button_image_1 = PhotoImage(
        file=relative_to_assets("Exit.png"))
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: window.destroy(),
        relief="flat"
    )
    button_1.place(
        x=930.0,
        y=25.0,
        width=60.0,
        height=60.0
    )



    #Create a 600 wide block of text that is aligned in the center
    text = Text(window, wrap="word", width=600, height=600, bg="#2F2F2F", fg="#FFFFFF", font=("Kanit Regular", 16))

    #center the heading in the window
    canvas.create_text(
        512.0,
        50.0,
        anchor="center",
        text="SmartTimeTable V2.1 by DuklaLabs",
        fill="#D24B49",
        font=("Kanit Regular", 40 * -1)
    )

    canvas.create_text(512, 120, anchor="center", text="Projekt chytrého rozvrhu sponzorován vedením školy", fill="#FFFFFF", font=("Kanit", 26 * -1))

    canvas.create_text(512, 200, anchor="center", text="Poháněn je RasperyPi zero 2 W", fill="#FFFFFF", font=("Kanit", 28 * -1))
    canvas.create_text(512, 240, anchor="center", text="Zobrazen je na 10.1“ TFT LCD display", fill="#FFFFFF", font=("Kanit", 28 * -1))
    figma_text = canvas.create_text(512, 280, anchor="center", text="Grafické rozhraní je vytvořeno softwarem Figma", fill="#FFFFFF", font=("Kanit", 28 * -1))
    canvas.create_text(512, 320, anchor="center", text="S použitím knihovny TKinter designer pro import GUI", fill="#FFFFFF", font=("Kanit", 28 * -1))

    canvas.create_text(512, 400, anchor="center", text="Pro více info se obraťte na DuklaLabs CEO – Jan Petrášek", fill="#FFFFFF", font=("Kanit", 28 * -1))

    canvas.create_text(512, 450, anchor="center", text="WORK IN PROGRESS", fill="#FF0000", font=("Kanit", 28 * -1))

    #if the DuklaLabs logo get clicked three time in 10 seconds, change the "Figma" text to "Ligma"
    def change_figma_text(new_text):
        canvas.itemconfigure(figma_text, text=new_text)





    button_image_5 = PhotoImage(
        file=relative_to_assets("Video.png"))
    button_5 = Button(
        window,
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [play_video("SpinningFish.mp4"), window.after(1, window.lift)],
        relief="flat"
    )
    button_5.place(
        x=923,
        y=180,
        width=70.0,
        height=70.0
    )






    image_image_1 = PhotoImage(
        file=relative_to_assets("SchoolLogo.png"))
    image_1 = canvas.create_image(
        231.0,
        530.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("GithubQRCode.png"))
    image_2 = canvas.create_image(
        939,
        514.0,
        image=image_image_2
    )

    click_count = 0

    def increase_click_count():
        window.after(3000, reset_click_count)
        nonlocal click_count
        click_count += 1
        if click_count == 3:
            change_figma_text("Grafické rozhraní je vytvořeno softwarem Ligma")

    def reset_click_count():
        nonlocal click_count
        click_count = 0
        change_figma_text("Grafické rozhraní je vytvořeno softwarem Figma")

    button_image_2 = PhotoImage(
        file=relative_to_assets("DuklaLabsLogo.png"))
    button_2 = Button(
        window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=increase_click_count,
        relief="flat"
    )
    button_2.place(
        x=452.0,
        y=485.0,
        width=90.0,
        height=90.0
    )

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    root = Tk()
    show_credits(root)
    root.destroy()