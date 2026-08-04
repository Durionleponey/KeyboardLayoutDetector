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
    loadingScreen.title = "KeyboardLayoutIdentificator"
    loadingScreen.geometry("1000x700")
    loadingScreen.resizable(False, False)\


    photo = PhotoImage(file="./asset/keyboardLayoutDetectorLogo.png")
    lbl = Label(loadingScreen, image=photo)
    lbl.pack()



    ctk.CTkLabel(loadingScreen, text="Loading Keyboard Layout Identificator...", font=("Roboto", 14)).pack(pady=(30, 10))
    bar = ctk.CTkProgressBar(loadingScreen, mode="indeterminate", width=500)
    bar.pack()
    bar.start()

    def load():
        global importTemp
        from extraction import selectionner_images as f
        importTemp = f
        loadingScreen.after(0, loadingScreen.destroy)

    threading.Thread(target=load, daemon=True).start()
    loadingScreen.mainloop()

    importTemp()


if __name__ == "__main__":
    main()