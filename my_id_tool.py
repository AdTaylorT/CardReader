import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import easyocr
import cv2
import cv2.typing as ct
import torch.cuda as nv
from typing import cast

from region_of_interest import region_of_interest as roi
from card_model import card


class my_id_tool():
    regions: list[roi]
    mcard: card | None
    img: ct.MatLike | None  

    def __init__(self, image=None, regions=[]):
        print(f'gpu ready: {nv.is_available()}')
        self.regions = regions
        self.img = image
        self.mcard = None     

    def identify(self, img: ct.MatLike) -> card:
        self.img = img
        self.img_root = img.copy()
        if self.regions is None or len(self.regions) == 0:
            self.define_regions()
        extracted_text = self.extract_text_with_easyocr()
        self.mcard = card(extracted_text)    
        #cv2.imwrite(f'SWDump/{self.mcard.file_name}.png', self.img) # type: ignore
            
        return self.mcard
    
    def extract_text_with_easyocr(self, languages=['en']):
        """
        Extracts text from an image using EasyOCR.
        """
        if self.img is None:
            print("no image")
            return
        try:
            reader = easyocr.Reader(languages, gpu=nv.is_available())
            reader_res=[]
            for r in self.regions:
                reader_res.append(reader.readtext(r.get_roi(self.img)))
            extracted_text=[]
            for read in reader_res:
                for (bbox, text, prob) in read:
                    extracted_text.append(text) 
                    print(f"extraction: {text}")
            return extracted_text
        except Exception as e:
            return f"Error: {e}"

    def define_regions(self):
        """
        define regions that should be read from
        """
        if self.img is None:
            return
        # Convert to grayscale
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # type: ignore
        cv2.namedWindow("grayscale")
        cv2.setMouseCallback("grayscale", lambda a,b,c,d,e : click_button(a,b,c,d,e), [self, "grayscale"])
        while True:
            image = self.img
            cv2.imshow("grayscale", image)
            if cv2.waitKey(1) & 0xFF == 27:
                # hard exit if we don't have a name
                if len(self.regions) <= 0:
                    exit()
                cv2.destroyWindow("grayscale")
                return self.regions
            for r in self.regions:
                if r.has_no_value():
                    continue
                point1, point2 = r.get_raw_roi()      
                cv2.rectangle(image, point1, point2, (0,0,0), 2)
    
    def show_selected_regions(self, roi:tuple[roi]):
        if self.img is None:
            return None
        for idx, r in enumerate(roi):
            gray_image = r.get_roi(self.img)
            title = f"title{idx}"
            cv2.imshow(title, gray_image)
            cv2.setMouseCallback("grayscale", lambda a,b,c,d,e :close_action(a,b,c,d,e), [title])


def click_button(event:int, x:int, y:int, flags, params):
    id_tool = cast(my_id_tool, params[0])
    id_tool.img = id_tool.img_root.copy()
    cv2.putText(id_tool.img, "title", (x,y), 0, 4, (0,0,0)) # type: ignore
    if len(id_tool.regions) > 0 and id_tool.regions[-1].has_no_value():
        cv2.rectangle(id_tool.img, id_tool.regions[-1].coords[0], (x,y), (0,0,0), 2)
    if event == cv2.EVENT_LBUTTONDOWN:
        print("pushing region")
        reg = roi()
        reg.set_coord(0, (x,y))
        id_tool.regions.append(reg)
    elif event == cv2.EVENT_LBUTTONUP:
        print("final coord")
        id_tool.regions[-1].set_coord(1, (x,y))
    elif event == cv2.EVENT_RBUTTONUP:
        print("entered callback")
        if len(id_tool.regions) > 0:
            id_tool.img = id_tool.img_root.copy()
            id_tool.regions.pop()
        #cv2.destroyWindow(params[1])
    else:
        pass

def close_action(event:int, x, y, flags, params):
    if event == cv2.EVENT_RBUTTONUP:
        print("entered callback")
        cv2.destroyWindow(params[0])

if __name__ == "__main__":
    midt = my_id_tool()
    i_path = cv2.imread("test/test.png")
    if i_path is not None:
        midt.identify(i_path)