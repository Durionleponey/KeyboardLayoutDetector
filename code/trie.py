import warnings
from utils import *

warnings.filterwarnings('ignore')


def ocr_keyboard_layout_multi_files(reader, files_to_analyze):

    results = []
    for path in files_to_analyze:
        results.append(ocr_keyboard_layout(reader,path))

    return results


def ocr_keyboard_layout(reader, file_to_analyze):

    plotoupas = 1
    plotoupas = 0


    #print(file_to_analyze)

    img = cv2.imread(file_to_analyze)

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

    tol = 30

    #print(tol)




    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if plotoupas:
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

    #print(dic_char)


    isQwerty = 0


    if plotoupas:
        for i in dic_char:
            key = dic_char[i]
            plt.text(key[0][0], key[0][1] - 8, i.upper(), color='lime', fontsize=14, ha='center')
        plt.show()




    def a_before_b(a, b, tol):
        (ax, ay), (bx, by) = a[0], b[0]
        if abs(ay - by) > tol:
            return ay < by
        return ax < bx


    scoreDic = {
        "a": {"q": 2, "w": 3},
        "z": {"q": 2, "w": 3},
    }


    done = set()


    for key in dic_char:
        for compaKey in dic_char:
            if (key,compaKey) not in done and key in scoreDic and compaKey in scoreDic[key]:

                done.add((key,compaKey))

                value = scoreDic[key][compaKey]

                test = a_before_b(dic_char[key], dic_char[compaKey], tol)

                if test > 0:
                    isQwerty-= value
                else:
                    isQwerty+= value





    #print(isQwerty)


    if isQwerty == 0:
        return("ERROR")

    if isQwerty > 0:
        return("QWERTY")
    else:
        return("AZERTY")



