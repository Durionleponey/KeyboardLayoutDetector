


### Keyboard Layout Detector (AZERTY / QWERTY)

Ce projet détecte automatiquement le layout de clavier (AZERTY ou QWERTY) à partir d’images de clavier en utilisant OpenCV & EasyOCR.

### 1. Fonctionnalités

- Upscale automatique de l’image pour améliorer l’OCR.


**Visualisation complète** :

- image originale,
- images pré‑traitées avec bounding boxes,
- résumé du layout détecté + confiance.

### 2. Installation
**2.1. Cloner le dépôt**

```
bash
git clone <URL_REPO>
cd <VOTRE_REPO>
```

**2.2. Créer un environnement virtuel (recommandé)**
```
bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# ou
.\.venv\Scripts\activate       # Windows
```

**2.3. Installer les dépendances**
```
bash
pip install -r requirements.txt
```



**3. Structure principale du code**

```
project/
│── detect_layout.py       # pipeline principal de détection
│── utils.py               # prétraitements, corrections OCR, dessin bounding boxes
│── extraction.py          # interface CustomTkinter (sélecteur d’images)
│── data/                  # photos de claviers à analyser
│── requirements.txt
│── README.md

```


### 4. Utilisation
Lancer 
`python main.py`

Fonctionnalités de l’interface :
- aperçu des images (scrollable + zoom)
- sélection multiple
- analyse batch
- affichage clair des résultats


