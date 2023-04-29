from Camera_init import *
import os
import shutil
import cv2
import glob
import numpy as np


# Define the frame width and height
h = 480  # y co-ordinate
w = int(1.3334*h)  # x co-ordinate
# 480, 640
# Now 650, 866 frame shape

# *********************************************** Get Images *******************************************************
def get_img():
    # Create the images directory if it does not exist
    if os.path.exists('images'):
        shutil.rmtree('images')

    os.makedirs('images')
    dc = DepthCamera()
    num = 0
    while True:
        ret, depth_frame, depth_img, color_frame = dc.get_frame()
        # depth_img will give use depth distance other t1o are used for obtaining depth and color frame
        color_frame = cv2.resize(color_frame, (w, h))
        if not ret:
            print("return value is", ret)
            continue

        cv2.imshow("color_frame", color_frame)
        key_pressed = cv2.waitKey(5) & 0xFF
        if key_pressed == ord('q'):
            break
        elif key_pressed == ord('s'):  # wait for 's' key to save and exit
            cv2.imwrite('images/img' + str(num) + '.png', color_frame)
            print("image saved!")
            num += 1

    dc.release()
    cv2.destroyAllWindows()


get_img()


