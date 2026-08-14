# main.py


from utils import loading_screen
import os



os.environ["TCL_LIBRARY"] = r"C:\Program Files\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"]  = r"C:\Program Files\Python313\tcl\tk8.6"
#print("hello")


importTemp =None
reader =None


def main():



    def load():

        global importTemp
        from extraction import selectionner_images as f
        importTemp = f
        global reader
        import easyocr
        reader = easyocr.Reader(['en', 'fr'], gpu=True)

    loading_screen(load)

    importTemp(reader)


if __name__ == "__main__":
    main()