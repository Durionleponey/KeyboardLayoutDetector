import warnings
from utils import *

warnings.filterwarnings('ignore')


def ocr_keyboard_layout_multi_files(reader, files_to_analyze):

    results = []

    number_of_image_to_load = len(files_to_analyze)
    for i,path in enumerate(files_to_analyze):
        temp = loading_screen(ocr_keyboard_layout,path=path,reader=reader,number_of_image_to_load=number_of_image_to_load,current_image_number=i+1)
        #print(f"--->{temp}")
        results.append(temp)
    return results


def ocr_keyboard_layout(file_to_analyze, reader):

    def raw_keybord_reader(img):

        return reader.readtext(
            img,
            allowlist='AZQW',
            detail=1,
            text_threshold=0.4,
            low_text=0.3,
            link_threshold=0.9,
            width_ths=0.0,
            ycenter_ths=0.0
        )


    def scan_raw_to_data(full_result):

        dic_char = {}
        for bbox, text, conf in full_result:

            if len(text) > 1 or conf < 0.8:
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

        return dic_char



    def data_to_verdict(dic_char):

        isQwerty = 0

        def a_before_b(a, b, tol=30):
            (ax, ay), (bx, by) = a[0], b[0]
            if abs(ay - by) > tol:
                return ay < by
            return ax < bx

        done = set()

        scoreDic = {
            "a": {"q": 2, "w": 3},
            "z": {"q": 2, "w": 3},
        }

        for key in dic_char:
            for compaKey in dic_char:
                if (key,compaKey) not in done and key in scoreDic and compaKey in scoreDic[key]:

                    done.add((key,compaKey))

                    value = scoreDic[key][compaKey]

                    test = a_before_b(dic_char[key], dic_char[compaKey])

                    if test > 0:
                        isQwerty-= value
                    else:
                        isQwerty+= value

        return isQwerty

    plotoupas = 1
    plotoupas = 0

    plotoupas2 = 1
    plotoupas2 = 0



    #print(f"path--->{file_to_analyze}")

    img = cv2.imread(file_to_analyze)

    h, w = img.shape[:2]
    img = img[:, :w // 3]
    img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)



    full_result = raw_keybord_reader(gray)
    dic_char = scan_raw_to_data(full_result)
    isQwerty = data_to_verdict(dic_char)

    #print(tol)
    if plotoupas:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        for i in dic_char:
            key = dic_char[i]
            plt.text(key[0][0], key[0][1] - 8, i.upper(), color='lime', fontsize=14, ha='center')
        plt.show()

    #print(isQwerty)


    if isQwerty == 0:
        rotation = [0,90,180,270]

        for i in rotation:
            img = cv2.imread(file_to_analyze)

            # img = img[:, :w // 3]
            img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

            if i ==0:
                pass
            if i == 90:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            if i == 180:
                img =cv2.rotate(img, cv2.ROTATE_180)
            if i == 270:
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.bitwise_not(gray)

            full_result = raw_keybord_reader(gray)
            dic_char = scan_raw_to_data(full_result)
            isQwertyTemp = data_to_verdict(dic_char)

            #print(f"angle value :{i} confiance valye {isQwertyTemp}")


            if abs(isQwerty) < abs(isQwertyTemp):
                isQwerty = isQwertyTemp

            if abs(isQwerty) == 10:
                break



            if plotoupas2:
                image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                plt.imshow(image2)
                for i in dic_char:
                    key = dic_char[i]
                    plt.text(key[0][0], key[0][1] - 8, i.upper(), color='lime', fontsize=14, ha='center')
                plt.show()
                plt.close()





        #print(f'{isQwerty=}')

        if isQwerty==0:
            return "ERROR"

        if isQwerty > 0:
            return ("QWERTY")
        else:
            return ("AZERTY")






    if isQwerty > 0:
        return("QWERTY")
    else:
        return("AZERTY")



