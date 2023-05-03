from Camera_init import *
import mediapipe as mp
import pandas as pd
import numpy as np

import random
from camera_inp import dc


# Global Variable
def detect_init():
    global arr, point, distance, distList_max, distList_min, finger_coordinate
    arr = []
    point = (400, 300)
    distance = 0
    distList_max = [0, 0, 0, 0, 0]
    distList_min = [0, 0, 0, 0, 0]
    finger_coordinate = [0, 0, 0]


global lst
lst = [0, 0]

# Define the frame width and height
h = 480  # y co-ordinate
w = int(1.3333 * h)  # x co-ordinate
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Image Processing
pTime = 0
cTime = 0
Hand_data = []
index_data = []

# Now 650, 866 frame shape
var = False


def hand_detected():
    global var
    return var


def compare_dist():
    global lst, arr, finger_coordinate
    handd = finger_coordinate
    x, y, z = handd[0], handd[1], handd[2]
    print(x, y, z, __name__)
    print(arr.shape, __name__)

    if x < arr.shape[0] and y < arr.shape[1]:  # Hand should be in screen region
        depth = arr[x][y]
        if abs(z - depth) < 100:
            print('Hand Detected close to screen')
            lst[0] = x
            lst[1] = y
            return True
        return False
    return False


def pixel_coordinate():
    return lst


# Functions
def centroid(lmlist):
    cen_x = int((lmlist[5][1] + lmlist[9][1] + lmlist[13][1] + lmlist[17][1] + lmlist[0][1]) / 5)
    cen_y = int((lmlist[5][2] + lmlist[9][2] + lmlist[13][2] + lmlist[17][2] + lmlist[0][2]) / 5)
    xx, yy = cen_x, cen_y
    return xx, yy


def L_BwFing(pt1, pt2):
    return ((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2) ** 0.5


def pointing_finger(lmList):
    global point, distList_max, distList_min
    xx, yy = centroid(lmList)

    # Finger condition
    for id in [1, 5, 9, 13, 17]:
        if distList_min[id // 4] < L_BwFing(lmList[id], lmList[id + 2]):
            distList_min[id // 4] = L_BwFing(lmList[id], lmList[id + 2])

    finger_pointing = []
    for id in [1, 5, 9, 13, 17]:
        # distList_max[i//4] >= L_BwFing(lmList[i],lmList[i+3])
        if L_BwFing(lmList[id], lmList[id + 3]) > distList_min[id // 4]:
            finger_pointing.append(id)

    if len(finger_pointing) != 0 and len(finger_pointing) < 3:
        random_num = random.choice(finger_pointing)
        xx = lmList[random_num + 3][1]
        yy = lmList[random_num + 3][2]

    # xx = lmList[8][1]
    # yy = lmList[8][2]
    if xx > w:
        xx = w - 1
    if yy > h:
        yy = h - 1
    point = (xx, yy)
    print(xx, yy)


# Initialize Intel Camera Realsense
# dc = DepthCamera()
# 480, 640 frame shape

# Create Object for Hand

def main():
    global finger_coordinate, arr, var, w, h, Hand_data
    arr = pd.read_csv('mydata.csv')

    ret, depth_frame, depth_img, color_frame = dc.get_frame()
    # depth_img will give use depth distance other t1o are used for obtaining depth and color fram
    depth_img = cv2.resize(depth_img, (w, h))
    depth_frame = cv2.resize(depth_frame, (w, h))
    color_frame = cv2.resize(color_frame, (w, h))
    # color_frame = cv2.flip(color_frame, 1)
    # depth_frame = cv2.flip(depth_frame, 1)

    # Hand detection package from OpenCV
    imgRGB = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)  # Because mpHands module uses RGB
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        var = True
        for handLms in results.multi_hand_landmarks:
            lmList = []
            # Draw hand landmarks
            mpDraw.draw_landmarks(color_frame, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                h, w, c = color_frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if cx > w:
                    cx = w
                if cy > h:
                    cy = h
                # print(id, cx, cy)

            # Collect data
            if len(Hand_data) == 0:
                Hand_data = lmList
            else:
                Hand_data = np.vstack((Hand_data, lmList))

        # Find finger which is open
        print("Hand Img no.  = ", len(Hand_data) // 21)
        pointing_finger(lmList)
        print(point)

        cv2.circle(color_frame, (point[0], point[1]), 10, (0, 0, 255), cv2.FILLED)

        # Show distance for a specific point
        distance = depth_img[point[1], point[0]]  # 1st y point, then x-point
        print(distance, type(distance), "Line176")

        Strng = "{}mm".format(distance)
        cv2.putText(color_frame, Strng, point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 180), 2)
        cv2.imshow('color_frame', color_frame)
        cv2.imshow('depth_frame', depth_frame)

        # Detect finger in range
        arr = np.array(arr)
        finger_coordinate = [point[0], point[1], distance]
        detection = compare_dist()

        key = cv2.waitKey(1)

    # cv2.destroyWindow('color_frame')
    # cv2.destroyWindow('depth_frame')
