import io
import os
import sys
from PIL import Image
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
import pyscreenshot as ImageGrab
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

import time

class Window(QMainWindow):
  
    def __init__(self):
        super().__init__()
  
        # set the title
        self.setWindowTitle("Screen Capture region")
  
        self.setWindowOpacity(0.5)
  
        # setting  the geometry of window
        self.setGeometry(60, 60, 600, 400)

        # Create a timer to capture the screen every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)
        self.timer.start(5000)  # Capture every 5000 milliseconds (5 second)

        # show all the widgets
        self.show()

    def capture_screen(self):
        global capture_start
        # 開始測量capture時間
        capture_start = time.time()
        print("timer countdown時間： %f 秒" % (capture_start))

        # Capture the screen content within the window's geometry
        screenshot = ImageGrab.grab(bbox=(self.geometry().x(), self.geometry().y(),
                                          self.geometry().x() + self.geometry().width(),
                                          self.geometry().y() + self.geometry().height()))

        # Perform OCR using Google Cloud Vision on the screenshot
        self.perform_ocr(screenshot)

    def perform_ocr(self, screenshot):
        # Save the screenshot to an in-memory buffer as a JPEG image
        image_buffer = io.BytesIO()
        screenshot.save(image_buffer, format='PNG')
        screenshot_bytes = image_buffer.getvalue()

        # 結束測量capture時間
        capture_end = time.time()

        # 開始測量時間
        detected_start = time.time()

        # 使用Google Cloud Vision API進行文字辨識
        image = vision_v1.Image(content=screenshot_bytes)
        response = client_vision.text_detection(image=image)
        texts = response.text_annotations

        # 提取辨識到的文字
        if texts:
            detected_text = texts[0].description

            # detect text (OCR)
            detected_end = time.time()

            print("Detected Text: ")
            print(detected_text)
            print()

            # translation 測量開始
            trans_start = time.time()

            # 將辨識的文字按行分割
            lines = detected_text.split("\n")

            # 初始化翻譯後的行列表
            translated_lines = []

            # 逐行翻譯
            target_language = "zh-TW"  # 將此替換為你想要的目標語言代碼（例如：英文 --> en）
            for line in lines:
                translated_line = client_translate.translate(
                    line, target_language=target_language
                )
                translated_lines.append(translated_line["translatedText"])

            # 將翻譯後的行重新組合成一個帶有換行的字符串
            translated_text_with_newlines = "\n".join(translated_lines)

            # translation 測量結束
            trans_end = time.time()

            print(f"Translated Text ({target_language}): \n{translated_text_with_newlines}")
            print()
            print("************************************")
            # 輸出測量結果
            print("Screen Capture時間： %f 秒" % (capture_end - capture_start))
            print("OCR辨識時間： %f 秒" % (detected_end - detected_start))
            print("translation時間： %f 秒" % (trans_end - trans_start))
            tmp = trans_end
            print("----------------------------------------")
            

        else:
            print("No text detected in the image.")
  

if __name__ == "__main__":

    # 設定Google Cloud金鑰環境變數，請將YOUR_GOOGLE_CLOUD_KEY替換成你的實際金鑰
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/menghao/Downloads/大學專題資料/googleAPI/manifest-surfer-400014-6ed9f85a5367.json'
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_GOOGLE_CLOUD_KEY.json"

    # 初始化Google Cloud Vision API客戶端
    client_vision = vision_v1.ImageAnnotatorClient()

    # 初始化Google Cloud Translation API客戶端
    client_translate = translate.Client()

    # create pyqt5 app
    App = QApplication(sys.argv)
    
    # create the instance of our Window
    window = Window()
    
    # start the app
    sys.exit(App.exec())
  