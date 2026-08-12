
from typing import List, Tuple, Dict, Any
import warnings

import matplotlib.pyplot as plt

from utils import *

warnings.filterwarnings('ignore')

def ocr_keyboard_layout(reader, files_to_analyze):


    print(files_to_analyze)

    img = cv2.imread(files_to_analyze[0])



    all_detected = []  # List of lists of (char, confidence) for each method
    all_full_detections = []  # List of full OCR results with bounding boxes for each method

    # Define allowed characters for keyboard detection

    h, w = img.shape[:2]
    img = img[:, :w // 3]
    img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)


    full_result = reader.readtext(
        gray,
        allowlist='AZQW',
        detail=1,
        text_threshold=0.4,
        low_text=0.3,
        link_threshold=0.9,
        width_ths=0.0,
        ycenter_ths=0.0,
    )




    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image)

    dic_char = {}


    for bbox, text, conf in full_result:

        if len(text) > 1 or conf < 0.2:
            continue

        text = text.lower()
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        cx, cy = sum(xs) / 4, sum(ys) /4

        if text not in dic_char:
            dic_char[text] = [[cx,cy],conf]
            continue
        if dic_char[text][1] < conf:
            dic_char[text] = [[cx, cy], conf]

    print(dic_char)


    azerty = 0
    qwerty = 0

    for i in dic_char:
        key = dic_char[i]
        plt.text(key[0][0], key[0][1] - 8, i.upper(), color='lime', fontsize=14, ha='center')
    plt.show()


    def a_before_b(a, b, tol):
        (ax, ay), (bx, by) = a[0], b[0]
        if abs(ay - by) > tol:
            return ay < by
        return ax < bx

    def a_upper_b(a, b, tol):
        (ax, ay), (bx, by) = a[0], b[0]
        return ay < by

    #print(f'is a before z --->{a_before_b(dic_char["a"],dic_char["z"],)}')
    #print(f'is q before x --->{a_before_b(dic_char["q"],dic_char["x"])}')


    total = azerty + qwerty
    print(azerty,qwerty,total)





    return 0
