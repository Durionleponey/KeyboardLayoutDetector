import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog as fd
from ocr import ocr_keyboard_layout_multi_files
import random


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self,reader):
        super().__init__()
        self.title("Sélecteur d'Images et Analyse de Clavier")
        self.geometry("1000x700") # Un peu plus large pour bien voir
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.reader = reader
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.join(current_dir, "..", "data")
        
        self.checkboxes = []      # (widget_checkbox, chemin_fichier, index_ligne)
        self.result_labels = []   # LISTE SÉPARÉE pour ne supprimer QUE les résultats

        self.title_label = ctk.CTkLabel(self, text="SÉLECTION DES CLAVIERS", font=("Roboto", 24, "bold"), text_color="#3B8ED0")
        self.title_label.grid(row=0, column=0, padx=20, columnspan=2, pady=(20, 10), sticky="ew")

        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Cliquez sur une image pour agrandir")
        self.scroll_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        self.scroll_frame.grid_columnconfigure(0, weight=0)
        self.scroll_frame.grid_columnconfigure(1, weight=0)
        self.scroll_frame.grid_columnconfigure(2, weight=1)

        self.status_label = ctk.CTkLabel(self, text="Sélectionnez des images et cliquez sur VALIDER.", font=("Roboto", 14), text_color="#F8A707")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(0, 5), sticky="ew")


        self.btn_openfile = ctk.CTkButton(self, text="OUVRIR UN AUTRE FICHIER", font=("Roboto", 14, "bold"), height=50, fg_color="#9D6526", hover_color="#C26526", command=self.open_image_from_dir)
        self.btn_openfile.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.ctk_export_txt = ctk.CTkCheckBox(self, text="EXPORTER LES RESULTATS EN .TXT", font=("Roboto", 14))
        self.ctk_export_txt.grid(row=3, column=1, padx=20, pady=(0, 20))

        self.btn_openfile2 = ctk.CTkButton(self, text="DESELECTIONNER TOUT", font=("Roboto", 14, "bold"), height=50, fg_color="#9D6526", hover_color="#C26526", command=self.deselect_all_checkbox)
        self.btn_openfile2.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.btn_selectAll2 = ctk.CTkButton(self, text="SELECTIONNER TOUT", font=("Roboto", 14, "bold"), height=50, fg_color="#9D6526", hover_color="#C26526", command=self.select_all_checkbox)
        self.btn_selectAll2.grid(row=4, column=1, padx=20, pady=(0, 20), sticky="ew")

        self.btn_validate = ctk.CTkButton(self, text="VALIDER", font=("Roboto", 14, "bold"), height=50, fg_color="#2CC985", hover_color="#229A65", command=self.submit, state="disabled")
        self.btn_validate.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        self.grid_columnconfigure((0, 1), weight=1)


        self.load_images()

    def select_all_checkbox(self):

        for i in self.checkboxes:
            i[0].select()

        if len(self.checkboxes):
            self.btn_validate.configure(state="normal")

    def deselect_all_checkbox(self):

        for i in self.checkboxes:
            i[0].set(0)

        if len(self.checkboxes):
            self.btn_validate.configure(state="disabled")

    def enable_disable_validate_button(self):
        flag = 0
        for chk in self.checkboxes:
            if chk[0].get() == 1:
                flag = 1
                break
        self.btn_validate.configure(state="normal" if flag else "disabled")




    def load_images(self):
        if not os.path.exists(self.folder_path):
            print(f"ERREUR: Le dossier data est introuvable ici : {self.folder_path}")
            return
        
        extensions = (".png", ".jpg", ".jpeg", ".webp")
        files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(extensions)]

        for i, filename in enumerate(files):#enumate give index and elemnent
            file_path = os.path.join(self.folder_path, filename)
            self.load_image_in_interface(file_path)



        #Robin fast debug
        #self.select_all_checkbox()
        #self.submit()


    def load_image_in_interface(self, file_path):
        try:
            pil_img = Image.open(file_path)
            preview_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 75))

            img_label = ctk.CTkLabel(self.scroll_frame, text="", image=preview_image, cursor="hand2")
            img_label.grid(row=len(self.checkboxes) + 1, column=0, padx=10, pady=5)
            img_label.bind("<Button-1>", command=lambda event, p=file_path: self.open_full_image(p))

            chk = ctk.CTkCheckBox(self.scroll_frame, text=file_path, font=("Roboto", 14), command=self.enable_disable_validate_button)
            chk.grid(row=len(self.checkboxes) + 1, column=1, padx=10, pady=5, sticky="w")

            self.checkboxes.append((chk, file_path, len(self.checkboxes) + 1))

        except Exception as e:
            print(f"Erreur chargement {file_path}: {e}")



    def open_full_image(self, path):
        top = ctk.CTkToplevel(self)
        top.title("Zoom")
        top.geometry("800x800")
        top.attributes("-topmost", True)
        top.zoom = 1

        def apply_zoom(delta):
            MAX_ZOOM = 4
            MIN_ZOOM = 0.2

            if MIN_ZOOM < delta + top.zoom < MAX_ZOOM:

                top.zoom += delta
                full_image.configure(size=(int(base_size[0] * top.zoom),int(base_size[1] * top.zoom)))

            top.btn_dezoom.configure(state="normal" if top.zoom + delta > MIN_ZOOM else "disabled")
            top.btn_zoom.configure(state="normal" if top.zoom + delta < MAX_ZOOM else "disabled")
        try:

            pil_img = Image.open(path)
            w, h = pil_img.size
            ratio = min(800 / w, 600 / h)
            base_size = (w * ratio, h * ratio)  # float, jamais modifié
            full_image = ctk.CTkImage(pil_img, size=(int(base_size[0]), int(base_size[1])))
            ctk.CTkLabel(top, text="", image=full_image).pack(expand=True, fill="both")
            top.btn_zoom = ctk.CTkButton(top, text="Zommer", font=("Roboto", 14, "bold"), height=50, fg_color="#2CC985", hover_color="#229A65", command=lambda : apply_zoom(0.2))
            top.btn_dezoom = ctk.CTkButton(top, text="Dezommer", font=("Roboto", 14, "bold"), height=50, fg_color="#2CC985", hover_color="#229A65", command=lambda : apply_zoom(-0.2))
            top.btn_zoom.place(relx=0.5, rely=0.85, anchor="center")
            top.btn_dezoom.place(relx=0.5, rely=0.95, anchor="center")
            top.bind("<MouseWheel>", lambda e: apply_zoom(0.1 if e.delta > 0 else -0.1))
        except Exception as e:
            ctk.CTkLabel(top, text=f"Erreur: {e}").pack()

    def open_image_from_dir(self):


        file_path = fd.askopenfilename()
        self.load_image_in_interface(file_path)

    def set_ui_state(self, state):
        for w in (self.btn_validate, self.btn_openfile,self.btn_openfile2, self.btn_selectAll2,self.ctk_export_txt):
            w.configure(state=state)
        for chk, _, _ in self.checkboxes:
            chk.configure(state=state)

        if state == "normal":
            self.resizable(True, True)
            self.overrideredirect(False)
        else:
            self.resizable(False, False)
            self.overrideredirect(True)



    def submit(self):
        self.set_ui_state("disabled")
        self.update()
        global f
        for label in self.result_labels:
            #print(self.result_labels)
            label.destroy()
        self.result_labels = []

        files_to_analyze = []
        for chk, file_path, row_index in self.checkboxes:
            if chk.get() == 1:
                files_to_analyze.append(file_path)
        
        if not files_to_analyze:
            self.status_label.configure(text="Aucune image sélectionnée.", text_color="#FF0000")
            return
            
        self.status_label.configure(text=f"Analyse en cours de {len(files_to_analyze)} image(s)...", text_color="#F8A707")
        self.update_idletasks()

        try:
            finalResult = ocr_keyboard_layout_multi_files(self.reader,files_to_analyze)
        except:
            for _ in range(5):
                print("ERRROORR")

        count = 0

        f = None

        if self.ctk_export_txt.get() == 1:
            try:
                self.ctk_export_txt.configure(state="disabled")
                f = open("keyboardLayoutDetector" + str(random.random())[2:] + "resultats.txt", "w", encoding="utf-8")
            except Exception as e:
                print(e)

        try:
            for chk, file_path, row_index in self.checkboxes:
                if chk.get() == 1:
                    if self.ctk_export_txt.get() == 1:
                        f.write(f"{file_path} : {finalResult[count]}\n")

                    res_lbl = ctk.CTkLabel(self.scroll_frame,
                                         text=f"➜ {finalResult[count]}",
                                         font=("Roboto", 14, "bold"),
                                         wraplength=400,
                                         justify="left")

                    res_lbl.grid(row=row_index, column=2, padx=10, pady=5, sticky="w")

                    self.result_labels.append(res_lbl)
                    count += 1

            self.status_label.configure(text=f"✅ Terminé ! ({count} résultats)", text_color="#2CC985")
            self.ctk_export_txt.configure(state="normal")

        except Exception as e:
            print(e)


        if f is not None:
            f.close()
        self.set_ui_state("normal")
        self.update()


def selectionner_images(reader):
    app = App(reader)
    app.mainloop()

if __name__ == "__main__":
    selectionner_images()