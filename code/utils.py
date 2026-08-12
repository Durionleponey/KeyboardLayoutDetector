import threading

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import PhotoImage, Label
import customtkinter as ctk


def upscale_image(img, scale=2, interpolation=cv2.INTER_CUBIC):
    """
    Upscales an image by a given factor safely.

    Parameters:
        img (numpy.ndarray): Input image.
        scale (float): Upscaling factor.
        interpolation (int): Interpolation method.

    Returns:
        numpy.ndarray: Upscaled image.
    """
    height, width = img.shape[:2]




    # Compute new size
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Ensure we don't exceed OpenCV's limit
    SHRT_MAX = 30000
    new_width = min(new_width, SHRT_MAX - 1)
    new_height = min(new_height, SHRT_MAX - 1)

    new_size = (new_width, new_height)

    upscaled = cv2.resize(img, new_size, interpolation=interpolation)
    return upscaled





def display_results(original_img):
    plt.figure(figsize=(18, 6))
    # Original Image
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis('off')

    plt.show()

def draw_boxes_on_image(img, detections):
    """Dessine les bounding boxes sur une copie de l'image."""
    if len(img.shape) == 2:
        img_display = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        img_display = img.copy()

    for bbox, text, score in detections:
        # Convertir bbox en points entiers
        pts = np.array(bbox, dtype=np.int32)

        # Dessiner le polygone (bounding box)
        cv2.polylines(img_display, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Ajouter le texte au-dessus de la box
        cv2.putText(
            img_display,
            f"{text}",
            (int(bbox[0][0]), int(bbox[0][1]) - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

    return img_display



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