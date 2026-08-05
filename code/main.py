# main.py
import threading
from tkinter import Image, PhotoImage, Label

from utils import loading_screen

import customtkinter as ctk

import os


os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Program Files\Python313\tcl\tk8.6"
print("hello")


importTemp =None

def main():

    def load():
        global importTemp
        from extraction import selectionner_images as f
        importTemp = f

    loading_screen(load)

    importTemp()


if __name__ == "__main__":
    main()