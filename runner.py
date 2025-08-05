import os

import my_id_tool
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2, cv2.typing as ct
from typing import Any, cast
from numpy import dtype, floating, integer, ndarray
from threading import Lock

from result_thread import result_thread
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
    lock: Lock

    def __init__(self):
        self.name = "Frame"
        self.tool = midt()
        self.mroi = roi()
        self.cards = {}
        self.__reset__()
        self.lock = Lock()

    def __reset__(self):        
        self.cap = cv2.VideoCapture(0)
        # 300 x 420
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    def main(self):
        t: result_thread | None
        t = None

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("stream died")
                return
            cv2.namedWindow(self.name)
            self.frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # self: mroi, frame, cap
            cv2.setMouseCallback(self.name, lambda a,b,c,d,e: click_region(a,b,c,d,e), [self])
            if not self.mroi.has_no_value():
                # Crop the ROI
                cropped_roi = self.mroi.get_roi(self.frame)

                # Resize the cropped ROI to the original frame dimensions
                height, width = self.frame.shape[:2]
                self.frame = cv2.resize(cropped_roi, (width, height), interpolation=cv2.INTER_LINEAR)

            cv2.imshow(self.name, self.frame)
            wk = cv2.waitKey(1)

            if wk & 0xFF == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                self.dump_cards()
                exit()
            elif wk & 0xFF == ord(' '):
                print("capturing with thread")
                result_thread(self.tool.identify, args=[self.frame, self.add_card]).start()


    def dump_cards_json(self):
        import json
        try:
           with open('cards.json', 'w') as json_file:
                json.dump(self.cards, json_file, indent=4)
        except IOError as e:
            print(f"error dumping {e}")

    def dump_cards(self):
        # csv format: Set,CardNumber,Count,IsFoil
        with open('output.csv', mode='w', newline='') as file:
            for k, v in self.cards.items():
                file.write(f'{k.play_set}, {k.number}, {v}, false\n')
            file.close()


    def add_card(self, c:card):
        print('adding card')
        self.lock.acquire()
        print('lock aquired')
        if not self.cards or self.cards is None:
            self.cards = {}
            self.cards[c] = 1
        else:
            if c in self.cards:
                self.cards[c] += 1
            else:
                self.cards[c] = 1

        self.lock.release()
        print('lock released')

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
