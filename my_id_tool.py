import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import easyocr
import cv2
from typing import cast
from region_of_interest import region_of_interest as roi

def click_button(event, x, y, flags, params):
    id_tool = cast(my_id_tool, params[0])
    mroi = id_tool.regions
    if event == cv2.EVENT_LBUTTONDOWN:
        print("pushing region")
        reg = roi()
        reg.set_coord(0, (x,y))
        mroi.append(reg)
    elif event == cv2.EVENT_LBUTTONUP:
        print("final coord")
        mroi[-1].set_coord(1, (x,y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("entered callback")
        cv2.destroyWindow(params[1])
    else:
        pass

def close_action(event, x, y, flags, params):
    if event == cv2.EVENT_RBUTTONDOWN:
        print("entered callback")
        cv2.destroyWindow(params[0])

class my_id_tool():
    regions: list[roi]
    img = None

    def __init__(self, regions=[]):
        self.regions = regions
        self.img = None            

    def identify(self, img=None):
        self.img = img
        if self.regions is None or len(self.regions) == 0:
            self.define_regions(img)
        extracted_text = self.extract_text_with_easyocr()
        if extracted_text:
            extracted_text = extracted_text.lower()
            output = self.clean_name(extracted_text)
            print(output)            
            cv2.imwrite(f'SWDump/{output}.png', self.img) # type: ignore
            
        return


    def clean_name(self, name):
            #output = "".join([x for x in extracted_text if x.isalnum()])
            output = ""
            for x in name:
                if x == " ":
                    output.join("_")
                elif x.isalnum():
                    output.join(x)
            
            return output
    
    def extract_text_with_easyocr(self, languages=['en']):
        """
        Extracts text from an image using EasyOCR.
        """
        if self.img is None:
            print("no image")
            return
        try:
            reader = easyocr.Reader(languages, False)
            results=[]
            extracted_text = ""
            for x in self.regions:
                results.append(reader.readtext(x.get_roi(self.img)))
            for res in results:
                extracted_text = " ".join([text for (bbox, text, prob) in res])
                print(extracted_text)
            return extracted_text
        except Exception as e:
            return f"Error: {e}"

    def define_regions(self, image):

        # Convert to grayscale
        self.img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # type: ignore
        cv2.namedWindow("grayscale")
        cv2.imshow("grayscale", self.img)
        cv2.setMouseCallback("grayscale", lambda a,b,c,d,e : click_button(a,b,c,d,e), [self, "grayscale"])
        cv2.waitKey(0)

    
    def show_selected_regions(self, roi):
        if self.img is None:
            return None
        for idx, r in enumerate(roi):
            gray_image = r.get_roi(self.img)
            title = f"title{idx}"
            cv2.imshow(title, gray_image)
            cv2.setMouseCallback("grayscale", lambda a,b,c,d,e :close_action(a,b,c,d,e), [title])


if __name__ == "__main__":
    midt = my_id_tool()
    exit_status = midt.identify()