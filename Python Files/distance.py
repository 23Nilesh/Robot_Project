from typing import List, Any

from Camera_init import *
from camera_inp import dc
import numpy as np
import pandas as pd

# dc = DepthCamera()
# point = [[500, 300], [600, 300], [500, 400], [600, 400]]
global avgg, arr
avgg: list[7] = []
var = False


def dist_status():
    global var
    return var


def chk(d_data):  # Chk if any value left without updating
    global avgg

    fill = sum(avgg) / len(avgg)
    n = d_data.shape[0]
    m = d_data.shape[1]
    count = 0
    for i in range(n):
        for j in range(m):
            if d_data[i][j] < 10:  # If found replace with avg of avg distances of n divided regions
                d_data[i][j] = int(fill)
                count += 1
    print('No. of values not updates are =', count)


def fill_data(region):
    n = region.shape[0]
    m = region.shape[1]
    lest = []
    for i in range(n):
        for j in range(m):
            if region[i][j] > 10:  # 10mm, Relasene measures in mm up to 5m
                lest.append(region[i][j])

    if len(lest) == 0:
        return 0
    global avgg
    avg = int(sum(lest) / len(lest))
    avgg.append(avg)
    for i in range(n):
        for j in range(m):
            if region[i][j] < 10:
                region[i][j] = avg


# def update_data(h_data, division):
#     n = division
#     h, w = h_data.shape[0], h_data.shape[1]
#     division_size_x = w//n
#     division_size_y = h//n
#
#     for x in range(0, w, division_size_x):
#         for y in range(0, h, division_size_y):
#             region = h_data[x:x+division_size_x, y:y+division_size_y]
#             fill_data(region)

def update_data(h_data):
    h, w = h_data.shape[0], h_data.shape[1]
    division_size_x = 10
    division_size_y = 10

    for x in range(0, w, division_size_x):
        for y in range(0, h, division_size_y):
            region = h_data[x:x + division_size_x, y:y + division_size_y]
            fill_data(region)


def take_dist(point):
    global var
    var = False
    x = point[1][0] - point[0][0] + 1
    y = point[2][1] - point[0][1] + 1
    print('Value of x, y', x, y)
    global arr
    arr = np.ones((x, y))
    columns = [str(i) for i in range(1, x + 1)]
    print(columns)
    # print(len(columns), columns)
    for ij in range(1):
        # Show distance for a specific point
        for i in range(0, x, 10):  # range([start], [stop], [step])
            # print(i)
            for j in range(0, y, 10):
                # print(j)
                ret, depth_frame, depth_img, color_frame = dc.get_frame()
                if not ret:
                    print("Return value is ", ret)
                    break

                # 1st y point, then x-point in distance
                distance = depth_img[point[0][1] + j, point[0][0] + i]
                arr[i][j] = distance
                # print('distance is ', distance)

                # Display on screen
                cv2.circle(color_frame, (point[0][0] + i, point[0][1] + j), 4, (0, 0, 255), thickness=2)
                cv2.imshow("depth_frame", depth_frame)
                cv2.imshow("color_frame", color_frame)
                key = cv2.waitKey(1)
                if key == 110:
                    break

        key = cv2.waitKey(1)
        if key == 110:
            break

        # arr = np.array(arr)
        print(arr.shape, type(arr.shape), arr.shape[0], arr.shape[1])
        update_data(arr)  # divide region
        print('Array shape ', arr.shape)
        chk(arr)

        df = pd.DataFrame(arr, columns)
        df.to_csv('mydata.csv', index=False, float_format='%.0f')

        var = True

    cv2.destroyWindow('color_frame')
    cv2.destroyWindow('depth_frame')

# take_dist([[500, 300], [600, 300], [500, 400], [600, 400]])
