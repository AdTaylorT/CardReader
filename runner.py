import os
from time import sleep

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
    capture_regions: list[roi]
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
        focus = 1
        foc_val = 0.0
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
            
            for r in self.tool.regions:
                if r.has_no_value():
                    continue
                point1, point2 = r.get_raw_roi()      
                cv2.rectangle(self.frame, point1, point2, (0,0,0), 2)

            cv2.imshow(self.name, self.frame)
            wk = cv2.waitKey(1)

            if wk & 0xFF == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                self.dump_cards()
                exit()
            elif wk & 0xFF == ord(' '):
                print("capturing with thread")
                rt = result_thread(self.tool.identify, args=[self.frame, self.add_card])
                rt.daemon=True
                rt.start()
                
            elif wk & 0xFF == ord('f'):
                if focus == 1:
                    print('auto focus off')
                    focus = 0
                else:
                    print('auto focus on')
                    focus = 1                    
                self.cap.set(cv2.CAP_PROP_AUTOFOCUS, focus)
            elif wk & 0xFF == ord('k'): #in
                foc_val += 1
                self.cap.set(cv2.CAP_PROP_FOCUS, foc_val)
            elif wk & 0xFF == ord('j'): #out
                foc_val -= 1
                self.cap.set(cv2.CAP_PROP_FOCUS, foc_val)
            elif wk & 0xFF == ord('m'): #in
                foc_val += 5
                self.cap.set(cv2.CAP_PROP_FOCUS, foc_val)
            elif wk & 0xFF == ord('n'): #out
                foc_val -= 5
                self.cap.set(cv2.CAP_PROP_FOCUS, foc_val)



    def dump_cards_json(self):
        import json
        try:
           with open('cards.json', 'w') as json_file:
                json.dump(self.cards, json_file, indent=4)
        except IOError as e:
            print(f"error dumping {e}")

    def dump_cards(self):
        # csv format: Set,CardNumber,Count,IsFoil
        with open('SWDump/output.csv', mode='w', newline='') as file:
            for k, v in self.cards.items():
                file.write(f'{k.play_set}, {k.number}, {v}, false\n')
            file.close()


    def add_card(self, c:card):
        print('adding card')
        while self.lock.locked():
            sleep(10)
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

    if r.mroi is not None and r.mroi.has_no_value():
        r.frame = cv2.rectangle(r.frame, r.mroi.coords[0], (x,y), (0,0,255), 2)
        cv2.imshow(r.name, r.frame)
        
    if event == cv2.EVENT_LBUTTONDOWN:
        print("entered callback - top left")
        mroi.set_coord(0, (x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        print("entered callback - bottom right")
        mroi.set_coord(1, (x,y))
    elif event == cv2.EVENT_RBUTTONUP:
        mroi.reset()
    else:
        pass

if __name__ == "__main__":
    r=runner()
    while True:
        r.__init__()
        r.main()
