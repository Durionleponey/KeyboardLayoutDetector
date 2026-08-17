import threading

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import PhotoImage, Label
import customtkinter as ctk




def loading_screen(load,path=None,reader=None):

    loadingScreen = ctk.CTk()
    loadingScreen.title("KeyboardLayoutIdentificator")
    loadingScreen.geometry("1000x700")
    loadingScreen.resizable(False, False)\

    #photo = PhotoImage(file="./asset/keyboardLayoutDetectorLogo.png")
    #lbl = Label(loadingScreen, image=photo)
    #lbl.place(relx=0.5, rely=0.4, anchor="center")

    ctk.CTkLabel(loadingScreen, text="Loading Keyboard Layout Identificator...", font=("Roboto", 18)).place(relx=0.5, rely=0.75, anchor="center")
    bar = ctk.CTkProgressBar(loadingScreen, mode="indeterminate", width=500)
    bar.place(relx=0.5, rely=0.8, anchor="center")
    bar.start()

    print("hello")



    temp = None

    def load2():
        nonlocal temp
        if path:
            temp = load(path,reader)
        else:
            temp =load()
        loadingScreen.after(0, loadingScreen.quit)


    threading.Thread(target=load2, daemon=True).start()
    loadingScreen.mainloop()
    loadingScreen.destroy()
    return temp