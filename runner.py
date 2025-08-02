import os

import my_id_tool
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2, cv2.typing as ct
from typing import Any, cast
from numpy import dtype, floating, integer, ndarray

from my_id_tool import my_id_tool as midt
from region_of_interest import region_of_interest as roi
from card_model import card

class runner():
    cap: cv2.VideoCapture
    frame: ct.MatLike
    mroi: roi
    name: str
    tool: midt
    cards: dict[card, int]

    def __init__(self):
        self.name = "Frame"
        self.tool = midt()
        self.mroi = roi()
        self.cards = {}
        self.__reset__()

    def __reset__(self):        
        self.cap = cv2.VideoCapture(0)
        # 300 x 420
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    def main(self):
        while True:
            ret, frame = self.cap.read()
            if cv2.waitKey(1) & 0xFF == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                self.dump_cards()
                exit()
            if not ret:
                print("stream died")
                return
            tmp_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.namedWindow(self.name)
            # self: mroi, frame, cap
            cv2.setMouseCallback(self.name, lambda a,b,c,d,e: click_region(a,b,c,d,e), [self])
            if not self.mroi.has_no_value():
                # Crop the ROI
                cropped_roi = self.mroi.get_roi(tmp_frame)

                # Resize the cropped ROI to the original frame dimensions
                height, width = tmp_frame.shape[:2]
                self.frame = cv2.resize(cropped_roi, (width, height), interpolation=cv2.INTER_LINEAR)
            else: 
                self.frame = tmp_frame

            cv2.imshow(self.name, self.frame)
            cv2.waitKey(50)

    def dump_cards(self):
        import json
        try:
           with open('cards.json', 'w') as json_file:
                json.dump(self.cards, json_file, indent=4)
        except IOError as e:
            print(f"error dumping {e}")

    def add_card(self, c:card):
        if not self.cards or self.cards is None:
            self.cards = {c:1}
            return
        
        if c.file_name in self.cards:
            self.cards[c] += 1
        else:
            self.cards[c] = 1

def click_region(event, x, y, flags, params):
    r = cast(runner, params[0])
    mroi = r.mroi
    frame = r.frame
    cap = r.cap
    tool = r.tool

    if event == cv2.EVENT_LBUTTONDOWN:
        print("entered callback - top left")
        mroi.set_coord(0, (x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        print("entered callback - bottom right")
        mroi.set_coord(1, (x,y))
    elif event == cv2.EVENT_MBUTTONDOWN:
        mroi.reset()
    elif event == cv2.EVENT_MOUSEWHEEL:
        print("entered callback - submit")
        c = tool.identify(frame)
        r.add_card(c)
        r.__reset__()
        print("restarting")
    else:
        pass

if __name__ == "__main__":
    r=runner()
    while True:
        r.__init__()
        r.main()
