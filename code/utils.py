import threading

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import PhotoImage, Label
import customtkinter as ctk




def loading_screen(load):

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

    def load2():
        load()
        loadingScreen.after(0, loadingScreen.quit)


    threading.Thread(target=load2, daemon=True).start()
    loadingScreen.mainloop()
    loadingScreen.destroy()