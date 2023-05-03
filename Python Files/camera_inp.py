from Camera_init import *
import os
import shutil
import cv2

# Define the frame width and height - (640, 480) or (866, 650)
h = 480  # y co-ordinate
w = int(1.3334 * h)  # x co-ordinate


# *********************************************** Get Images *******************************************************
def get_img(n):
    list_ = ["red", "blue", "green"]
    num = 0
    while num == 0:
        ret, depth_frame, depth_img, color_frame = dc.get_frame()
        color_frame = cv2.resize(color_frame, (w, h))
        # cv2.imshow("color_frame", color_frame)
        # cv2.imshow("depth_frame", depth_frame)
        cv2.waitKey(1) & 0xFF
        # if key_pressed == ord('q'):
        #     break

        cv2.imwrite('images/' + list_[n] + '.jpg', color_frame)
        print("image saved!")
        num += 1

    # dc.release()
    # cv2.destroyAllWindows()


# Create the images directory if it does not exist
if os.path.exists('images'):
    shutil.rmtree('images')
os.makedirs('images')

dc = DepthCamera()
