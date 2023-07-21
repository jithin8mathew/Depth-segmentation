import pyrealsense2 as rs
import os
import cv2
import numpy as np
from pathlib import Path
import time
from datetime import datetime
import re

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

print("[INFO] Starting streaming...")
pipeline.start(config)
print("[INFO] Camera ready.")

# creating the display window with opencv2
cv2.namedWindow('D405', cv2.WINDOW_NORMAL)
cv2.resizeWindow('D405', 600, 800)

range_value = 40

def update(val):
    global range_value
    range_value = val

cv2.createTrackbar('Depth', 'D405', 7, 50, update)

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    color_image = np.asanyarray(color_frame.get_data())
    depth_color_frame = rs.colorizer().colorize(depth_frame)
    temp_depth = np.asanyarray(depth_frame.get_data())
    temp_depth[temp_depth > (range_value * 100)] = 0
    color_image[temp_depth == 0] = [255, 255, 255]
    color_image = cv2.rotate(color_image, cv2.ROTATE_90_CLOCKWISE)

    cv2.imshow('D405', color_image)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
