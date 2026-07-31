# main.py

import skimage
# from matplotlib import pyplot as plt # Plus nécessaire
from extraction import selectionner_images
# from trie import detect_layout_from_image # Plus nécessaire ici
import os
os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Program Files\Python313\tcl\tk8.6"

def main():
    print("--- Programme Principal ---")
    
    # La fonction sélectionne et lance l'interface
    # L'analyse se fait maintenant directement DANS l'interface
    selectionner_images() 
    
    # Le programme se termine lorsque l'utilisateur ferme la fenêtre.
    print("Fermeture du programme.")

if __name__ == "__main__":
    main()