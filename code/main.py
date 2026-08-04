# main.py
import threading
from tkinter import Image, PhotoImage, Label

import customtkinter as ctk

import os


os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Program Files\Python313\tcl\tk8.6"
print("hello")


importTemp =None

def main():

    loadingScreen = ctk.CTk()
    loadingScreen.title("KeyboardLayoutIdentificator")
    loadingScreen.geometry("1000x700")
    loadingScreen.resizable(False, False)\

    photo = PhotoImage(file="./asset/keyboardLayoutDetectorLogo.png")
    lbl = Label(loadingScreen, image=photo)
    lbl.place(relx=0.5, rely=0.4, anchor="center")

    ctk.CTkLabel(loadingScreen, text="Loading Keyboard Layout Identificator...", font=("Roboto", 18)).place(relx=0.5, rely=0.75, anchor="center")
    bar = ctk.CTkProgressBar(loadingScreen, mode="indeterminate", width=500)
    bar.place(relx=0.5, rely=0.8, anchor="center")
    bar.start()

    def load():
        global importTemp
        from extraction import selectionner_images as f
        importTemp = f
        loadingScreen.after(0, kill_clean)

    def kill_clean():
        bar.stop()
        loadingScreen.quit()



    threading.Thread(target=load, daemon=True).start()
    loadingScreen.mainloop()
    loadingScreen.destroy()

    importTemp()


if __name__ == "__main__":
    main()