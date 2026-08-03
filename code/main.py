# main.py

import skimage
# from matplotlib import pyplot as plt # Plus nécessaire
from extraction import selectionner_images
# from trie import detect_layout_from_image # Plus nécessaire ici
import os
os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Program Files\Python313\tcl\tk8.6"

def main():
    print("heello!")

    selectionner_images() 


if __name__ == "__main__":
    main()