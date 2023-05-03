# Module for Using Intel Realsense Camera get color frame, depth frame, and measure depth
# HandTrack(Show lm and mouse co-ordinate)

import pyrealsense2 as rs
import numpy as np
import cv2

# Class for depth camera
class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        config = rs.config()
        self.pipeline = rs.pipeline()
        self.colorizer = rs.colorizer()
        self.tr1 = rs.threshold_filter(min_dist=0.05, max_dist=3)  # in metre

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()  # D415
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        # Device Product Line D400

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # If we are using other device like T series or L Series of company
        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        self.pipeline.start(config)


    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # To get distance
        depth_img = np.asanyarray(depth_frame.get_data())
        # color_frame = np.asanyarray(color_frame.get_data())
        # To get depth camera
        colorized_depth = np.asanyarray(self.colorizer.colorize(self.tr1.process(depth_frame)).get_data())
        depth_frame = cv2.bilateralFilter(colorized_depth, 10, 50, 100)  # Smoothing
        colorized_depth = np.asanyarray(self.colorizer.colorize(self.tr1.process(color_frame)).get_data())
        color_frame = cv2.bilateralFilter(colorized_depth, 0, 0, 0)  # Smoothing

        if (depth_frame is None) or (color_frame is None):
            return False, None, None
        return True, depth_frame, depth_img, color_frame
    # depth_img will give distance

    def release(self):
        self.pipeline.stop()




if __name__ == '__main__':
    # Initialize Intel Camera Realsense
    dc = DepthCamera()
    point = (300, 400)

    while True:
        ret, depth_frame, depth_img, color_frame = dc.get_frame()
        # ret ---> return  = TRUE or FALSE

        # Show distance for a specific point
        cv2.circle(color_frame, point, 4, (0, 0, 255), thickness=2)
        distance = depth_img[point[1], point[0]]  # 1st y point, then x-point

        # Display on screen
        cv2.putText(color_frame, "{}mm".format(distance), point, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)

        cv2.imshow("deth_frame", depth_frame)
        cv2.imshow("color_frame", color_frame)
        key = cv2.waitKey(1)
        if key == 110:  # chr(110) = n
            break