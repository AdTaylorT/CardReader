import easyocr
import cv2
import os

class my_id_tool():
    def __init__(self):
        pass

    def run(self):
        path = 'SWDump'
        image_file = 'SWDump/new_image.png'  # Replace with your image file path
        gray = self.to_grayscale(image_file)
        self.img = gray
        extracted_text = self.extract_text_with_easyocr(gray)
        extracted_text = extracted_text.lower()
        output = "".join([x for x in extracted_text if x.isalnum()])
        print(extracted_text)
        output = self.clean_name(output)
        print(output)

        os.rename(image_file, f'{path}/{output}.png')


    def clean_name(self, name):
        if "event" in name:
            return name[5:]

        return name
    
    def extract_text_with_easyocr(self, image_path, languages=['en']):
        """
        Extracts text from an image using EasyOCR.
        """
        try:
            reader = easyocr.Reader(languages, False)

            results = reader.readtext(image_path)
            extracted_text = " ".join([text for (bbox, text, prob) in results])
            return extracted_text
        except Exception as e:
            return f"Error: {e}"

    def to_grayscale(self, image_name):
        image = cv2.imread(image_name)

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # type: ignore
        
        #cv2.imshow('gray1 Image', gray_image)
        #cv2.waitKey(0)
        ## 1280 by 720
        # online image size 
        # 300 by 420
        #gray_image = gray_image[20:50, 50:280]
        gray_image = gray_image[20:150, 100:1100]

        #cv2.imshow('gray1 Image', gray_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return gray_image

if __name__ == "__main__":
    midt = my_id_tool()
    midt.run()