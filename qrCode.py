import qrcode
import validators
import cv2
import numpy as np
from pyzbar.pyzbar import decode


def createQRcode(value):
    img = qrcode.make(value)
    # if not validators.url(value):
    #     filename = value + ".jpg"
    # else:
    #     filename = "link.jpg"
    filename = "qr.jpg"
    img.save(filename)


createQRcode(
    "https://www.youtube.com/watch?v=-GmJLI122ZM&ab_channel=codebasicscodebasics"
)


def detectLiveFeed():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("Result")
    cap.set(3, 640)
    cap.set(4, 480)
    response_list = set()
    while True and (cv2.getWindowProperty("Result", 0) >= 0):

        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode("utf-8")
            print(myData)
            response_list.add(myData)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(
                img,
                myData,
                (pts2[0], pts2[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 255),
                2,
            )

        cv2.imshow("Result", img)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()
    return response_list


def detectFromImage(path):
    img = cv2.imread(path)
    if len(decode(img)) < 1:
        return False
    barcode = decode(img)[0]
    myData = barcode.data.decode("utf-8")
    # print(myData)
    # print(barcode)
    return myData


img_path = "Hello.jpg"
print(detectFromImage(img_path))
# print(detectLiveFeed())
