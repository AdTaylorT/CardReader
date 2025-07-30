from typing import Any
import cv2
from numpy import dtype, floating, integer, ndarray
from my_id_tool import my_id_tool as midt

cap: cv2.VideoCapture
frame: cv2.Mat | ndarray[Any, dtype[integer[Any] | floating[Any]]]

name="Frame"

cap = cv2.VideoCapture(0)
# 300 x 420
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cv2.namedWindow(name)
cv2.setMouseCallback(name, lambda a,b,c,d,e : click_button(a,b,c,d,e))
tool = midt()
c1 = (0,0)
c2 = (0,0)

def click_button(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global c1
        c1=(x,y)
    elif event == cv2.EVENT_LBUTTONUP:
        global c2
        c2=(x,y)
    elif event == cv2.EVENT_RBUTTONDOWN:
        global cap
        print("entered callback")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif event == cv2.EVENT_MBUTTONDOWN:
        c1 = (0,0)
        c2 = c1
    elif event == cv2.EVENT_MOUSEWHEEL:
        print("entered callback")
        tmp = cv2.rotate(zoomed_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite('SWDump/new_image.png', tmp)
        tool.run()
    else:
        pass

while True:
    ret, frame = cap.read()
    
    if c2[1] != 0:
            # Crop the ROI
        cropped_roi = frame[c1[1]:c2[1], c1[0]:c2[0]]

        # Resize the cropped ROI to the original frame dimensions
        height, width = frame.shape[:2]
        zoomed_frame = cv2.resize(cropped_roi, (width, height), interpolation=cv2.INTER_LINEAR)
    else: 
        zoomed_frame = frame

    cv2.imshow(name, zoomed_frame)
    cv2.waitKey(50)

