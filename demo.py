import cv2
import os
import shutil


def capture_image_from_cam_into_temp():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("test")
    while True and (cv2.getWindowProperty("test", 0) >= 0):
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir("temp"):
                os.mkdir("temp", mode=0o777)  # make sure the directory exists
            # img_name = "./temp/opencv_frame_{}.png".format(img_counter)
            img_name = "./temp/test_img.png"
            print("imwrite=", cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))

    cam.release()

    cv2.destroyAllWindows()

    return True


# capture_image_from_cam_into_temp()
