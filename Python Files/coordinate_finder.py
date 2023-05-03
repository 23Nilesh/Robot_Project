import cv2
import numpy as np

import math



def refining(img):
    kernel = np.array([[1,1,1], [1,1,1], [1,1,1]])
    sharpened = cv2.filter2D(img, -1, kernel)
    sharpened2 = cv2.filter2D(sharpened, -1, kernel)
    return sharpened2


def garbage_remove(img):
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 5000  # adjust this value to control maximum area of white region
    small_contours = [cnt for cnt in contours if cv2.contourArea(cnt) < max_area]

    # Create a mask image to represent the small white regions
    mask_ = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask_, small_contours, -1, 255, -1)

    # Invert the mask image to represent the black regions
    mask_inv = cv2.bitwise_not(mask_)

    # Apply the mask to the input image to change small white regions to black
    result = cv2.bitwise_and(img, img, mask=mask_inv)
    return result
def red_img(img1):
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    # lower red
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    # upper red
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img1, img1, mask=mask)

    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    res2 = cv2.bitwise_and(img1, img1, mask=mask2)

    img3 = res + res2
    avg_mask = mask2 + mask
    clean_img=garbage_remove(avg_mask)
    refined=refining(clean_img)
    return refined

def blue_img(img1):
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)



    # # Upper blue
    # lower_blue2 = np.array([150,50,50])
    # upper_blue2 = np.array([255,180,180])

    # Lower blue
    # lower_blue = np.array([100, 50, 50])  # Lower bound for blue hue, saturation and value
    # upper_blue = np.array([130, 275, 255])

    lower_blue = np.array([78, 158, 124])
    upper_blue = np.array([138, 255, 255])
    # rgb(37, 150, 190)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(img1, img1, mask=mask)

    # mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    # res2 = cv2.bitwise_and(img1, img1, mask=mask2)

    # img3 = res + res2
    # avg_mask = mask2 + mask
    clean_img = garbage_remove(mask)
    refined = refining(clean_img)
    return refined


def green_img(img1):
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    # Upper green
    lower_green2 = np.array([70,50,50])
    upper_green2 = np.array([90,255,255])

    # Lower green
    lower_green = np.array([50,50,50])
    upper_green = np.array([70,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(img1, img1, mask=mask)

    mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    res2 = cv2.bitwise_and(img1, img1, mask=mask2)

    img3 = res + res2
    avg_mask = mask2 + mask
    clean_img = garbage_remove(avg_mask)
    refined = refining(clean_img)
    return refined



def screen_finder(img):
    dim = img.shape
    height=dim[0]
    width=dim[1]

    coordinates_up = []
    coordinates_down = []


    for i in range(height - 1):
        for j in range(width - 1):
            condi1 = np.logical_and(img[i + 1, j] == 255, img[i, j] == 0)
            condi2 = np.logical_and(img[i, j] == 255, img[i + 1, j] == 0)
            if (condi1):
                coordinates_up.append([i + 1, j])
            if (condi2):
                coordinates_down.append([i, j])
    print(coordinates_up)
    print(coordinates_down)
    coordinates_up = Sort(coordinates_up)
    coordinates_down = Sort(coordinates_down)
    return [coordinates_up[0],coordinates_up[-1],coordinates_down[0],coordinates_down[-1]]

def screen_finder2(img):
    font = cv2.FONT_HERSHEY_COMPLEX

    _, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    # Detecting contours in image.
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # List to store the coordinates of the vertices
    # List to store the coordinates
    coord_list = []

    # Going through every contour found in the image.
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

        # draws boundary of contours.
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)

        # Used to flatten the array containing
        # the coordinates of the vertices.
        n = approx.ravel()
        i = 0

        while i < len(n):
            x = n[i]
            y = n[i + 1]

            # Add the coordinates to the list
            coord_list.append((x, y))

            # String containing the coordinates.
            string = str(x) + " " + str(y)

            if i == 0:
                # text on topmost coordinate.
                cv2.putText(img, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))
            else:
                # text on remaining coordinates.
                cv2.putText(img, string, (x, y), font, 0.5, (255, 255, 255))

            i += 2

    # Print the list of coordinates
    # print(coord_list)
    coord_list=sort1(coord_list)
    return coord_list


def sort1(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo

    if(l==4):

        if (sub_li[0][0] > sub_li[1][0]):
            tempo = sub_li[0]
            sub_li[0] = sub_li[1]
            sub_li[1] = tempo
        if (sub_li[2][0] > sub_li[3][0]):

            tempo = sub_li[2]
            sub_li[2] = sub_li[3]
            sub_li[3] = tempo
    return sub_li

def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li



def parts3_(list):
    print(list)
    x1=int((list[0][0]+list[1][0])/3)
    y1=int((list[0][1]+list[1][1])/3)
    x2 = int((list[0][0] + list[1][0]) *2/ 3)
    y2 = int((list[0][1] + list[1][1]) *2/ 3)
    ret_list=[[x1,y1],[x2,y2]]
    return ret_list


def trisect_points(point):
    # Calculate the distance between the two points
    distance = ((point[1][1] - point[0][1])**2 + (point[1][0] - point[0][0])**2)**0.5

    # Calculate the trisect points
    trisect_distance = distance / 3
    theta = math.atan2(point[1][1] - point[0][1], point[1][0] - point[0][0])
    trisect1_x = int(point[0][0] + trisect_distance * math.cos(theta))
    trisect1_y = int(point[0][1] + trisect_distance * math.sin(theta))
    trisect2_x = int(point[0][0] + 2 * trisect_distance * math.cos(theta))
    trisect2_y = int(point[0][1] + 2 * trisect_distance * math.sin(theta))

    return [[trisect1_x, trisect1_y], [trisect2_x, trisect2_y]]


def bisect(list):
    x1=int((list[0][0]+list[1][0])/2)
    y1=int((list[0][1]+list[1][1])/2)

    ret_list=[x1,y1]
    return ret_list


def intersection_point(line1_point1, line1_point2, line2_point1, line2_point2):
    # Line 1 equation: y = mx + b
    m1 = (line1_point2[1] - line1_point1[1]) / (line1_point2[0] - line1_point1[0])
    b1 = line1_point1[1] - m1 * line1_point1[0]

    # Line 2 equation: y = mx + b
    m2 = (line2_point2[1] - line2_point1[1]) / (line2_point2[0] - line2_point1[0])
    b2 = line2_point1[1] - m2 * line2_point1[0]

    # Find the intersection point
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = m1 * x_intersect + b1

    return [x_intersect, y_intersect]
def read_images():
    img = cv2.imread('images/red.jpg')
    red = red_img(img)
    # cv2.imshow("red", red)
    coordinates_game1 = screen_finder2(red)
    print("red", coordinates_game1)

    img2 = cv2.imread('images/blue.jpg')
    # cv2.imshow("bluer", img2)

    blue = red_img(img2)
    # cv2.imshow("blue", blue)
    coordinates_game2 = screen_finder2(blue)
    print("Blue", coordinates_game2)

    img3 = cv2.imread('images/green.jpg')
    green = green_img(img3)
    # cv2.imshow("green", green)
    coordinates_game3 = screen_finder2(green)
    print("green", coordinates_game3)

    coordinates_game = [[0, 0], [0, 0], [0, 0], [0, 0]]
    templist = [[0, 0], [0, 0], [0, 0], [0, 0]]
    count = 0
    if (len(coordinates_game1) == 4):
        count = 1
        for i in range(4):
            fi = int((coordinates_game[i][0] + coordinates_game1[i][0]) / count)
            sec = int((coordinates_game[i][1] + coordinates_game1[i][1]) / count)
            templist[i] = [fi, sec]
        coordinates_game = templist

    if (len(coordinates_game2) == 4):
        count = count + 1
        for i in range(4):
            fi = int((coordinates_game[i][0] + coordinates_game2[i][0]) / count)
            sec = int((coordinates_game[i][1] + coordinates_game2[i][1]) / count)
            templist[i] = [fi, sec]
        coordinates_game = templist

    if (len(coordinates_game3) == 4):
        count = count + 1
        for i in range(4):
            fi = int((coordinates_game[i][0] + coordinates_game3[i][0]) / count)
            sec = int((coordinates_game[i][1] + coordinates_game3[i][1]) / count)
            templist[i] = [fi, sec]
        coordinates_game = templist
    print(coordinates_game)
    # for i in range(4):
    #     for j in range(2):
    #         coordinates_game[i][j]=coordinates_game[i][j]*2
    # print(coordinates_game,"updated")

    trisect_up=trisect_points([coordinates_game[0],coordinates_game[1]])
    bisectleft=bisect([coordinates_game[0],coordinates_game[2]])
    bisectright=bisect([coordinates_game[1],coordinates_game[3]])
    trisect_mid=trisect_points([bisectleft,bisectright])
    trisect_bottom=trisect_points([coordinates_game[2],coordinates_game[3]])


    #storing the initial and final(the opposite coordinates) and reducing them by 10 pixel(to reduce the size of block, for accuracy)
    coordinates_final=[[[coordinates_game[0][0]+10,coordinates_game[0][1]+10],[trisect_mid[0][0]-10,trisect_mid[0][1]-10]],
                       [[[trisect_up[0][0]+10,trisect_up[0][1]+10],[trisect_mid[1][0]-10,trisect_mid[1][1]-10]]],
                       [[trisect_up[1][0]+10,trisect_up[1][1]+10],[bisectright[0]-10,bisectright[1]-10]],
                       [[bisectleft[0]+10,bisectleft[1]+10],[trisect_bottom[0][0]-10,trisect_bottom[0][1]-10]],
                       [[trisect_mid[0][0]+10,trisect_mid[0][1]+10],[trisect_bottom[1][0]-10,trisect_bottom[1][1]-10]],
                       [[trisect_mid[1][0]+10,trisect_mid[1][1]+10],[coordinates_game[3][0]-10,coordinates_game[3][1]-10]]]

    print('coordinate deliverd by coordinate_finder')
    return coordinates_final, coordinates_game
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

###########################################################################################################################
#execution starts
# Read the input image




