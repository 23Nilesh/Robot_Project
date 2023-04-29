from Camera_init import *
import numpy as np
import pandas as pd


dc = DepthCamera()
point = [[500, 300], [600, 300], [500, 400], [600, 400]]
x = point[1][0] - point[0][0] + 1
y = point[2][1] - point[0][1] + 1
print(x, y)
arr = np.ones((x, y))
columns = [str(i) for i in range(1, 102)]
print(len(columns), columns)



for ij in range(1):
    # Show distance for a specific point
    for i in range(0, x, 3):  # range([start], [stop], [step])
        print(i)
        for j in range(0, y, 3):
            print(j)
            ret, depth_frame, depth_img, color_frame = dc.get_frame()
            if not ret:
                print("Return value is ", ret)
                break

            # 1st y point, then x-point in distance
            distance = depth_img[point[0][1]+j, point[0][0]+i]
            arr[i][j] = distance
            print('distance is ', distance)

            # Display on screen
            cv2.circle(color_frame, (point[0][1]+j, point[0][0]+i), 4, (0, 0, 255), thickness=2)
            cv2.imshow("depth_frame", depth_frame)
            cv2.imshow("color_frame", color_frame)
            key = cv2.waitKey(1)
            if key == 110:
                break

        key = cv2.waitKey(1)
        if key == 110:
            break


print(arr)
arr = np.array(arr)
df = pd.DataFrame(arr, columns=columns)
df.to_csv('mydata.csv', index=False, float_format='%.2f')
