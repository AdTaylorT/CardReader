import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from threading import Thread
from typing import Any
import cv2
from numpy import dtype, floating, integer, ndarray
from my_id_tool import my_id_tool as midt
from region_of_interest import region_of_interest as roi

cap: cv2.VideoCapture
frame: cv2.Mat | ndarray[Any, dtype[integer[Any] | floating[Any]]]

name="Frame"

cap = cv2.VideoCapture(0)
# 300 x 420
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
tool = midt()
mroi = roi()
count = 0

def click_button(event, x, y, flags, params):
    global mroi, frame, my_thread
    if event == cv2.EVENT_LBUTTONDOWN:
        mroi.set_coord(0, (x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        mroi.set_coord(1, (x,y))        
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("entered callback")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif event == cv2.EVENT_MBUTTONDOWN:
        mroi.reset()
    elif event == cv2.EVENT_MOUSEWHEEL:
        print("entered callback")
        Thread(None, tool.identify(frame)).start()
    else:
        pass

while True:
    ret, frame = cap.read()
    tmp_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)    
    cv2.namedWindow(name)
    cv2.setMouseCallback(name, lambda a,b,c,d,e: click_button(a,b,c,d,e))
    if not mroi.has_no_value():
        # Crop the ROI
        cropped_roi = mroi.get_roi(tmp_frame)

        # Resize the cropped ROI to the original frame dimensions
        height, width = tmp_frame.shape[:2]
        frame = cv2.resize(cropped_roi, (width, height), interpolation=cv2.INTER_LINEAR)
    else: 
        frame = tmp_frame

    cv2.imshow(name, frame)
    cv2.waitKey(50)
