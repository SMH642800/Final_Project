import io
import os
import sys
from PIL import Image
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
from PySide6.QtCore import QObject, Signal
import pyscreenshot as ImageGrab
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

import time

class MainRecordingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title
        self.setWindowTitle("Main Control Windows")

        # Set the window background color to black
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        # Set the window opacity
        self.setWindowOpacity(0.7)

        # Set the window geometry
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry.x() + (screen_geometry.width() // 3) * 2, 
                         screen_geometry.y() + screen_geometry.height() // 3,
                         screen_geometry.width() // 4, screen_geometry.height() // 2)

        # Create a button to add or check the screen capture window
        self.add_window_button = QPushButton("Add Screen Capture Window", self)
        self.add_window_button.clicked.connect(self.add_or_check_screen_capture_window)

        # Create a recording button to start screen capture
        self.record_button = QPushButton("Record", self)
        self.record_button.clicked.connect(self.start_capture)

        # Create a stop button to stop screen capture
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setEnabled(False)  # Initially disabled

        # Set button backgrounds to transparent
        #self.add_window_button.setStyleSheet('QPushButton {background-color: transparent; color: red;}')
        self.add_window_button.setStyleSheet('QPushButton {background-color: white; color: red;}')
        self.record_button.setStyleSheet('QPushButton {background-color: white; color: red;}')
        self.stop_button.setStyleSheet('QPushButton {background-color: white; color: red;}')

        # Create a vertical layout to accommodate the buttons
        layout = QVBoxLayout()
        layout.addWidget(self.add_window_button)
        layout.addWidget(self.record_button)
        layout.addWidget(self.stop_button)

        # Create a QWidget as a container for the layout
        widget = QWidget(self)
        widget.setLayout(layout)

        # Add the QWidget to the main window
        self.setCentralWidget(widget)
        

    def add_or_check_screen_capture_window(self):
        # Check if a screen capture window is already open
        if hasattr(self, 'screen_capture_window') and self.screen_capture_window:
            QMessageBox.information(self, "Info", "You already have the Screen Capture Window open.")
        else:
            # Create and show the screen capture window
            self.screen_capture_window = ScreenCaptureWindow()
            self.screen_capture_window.closed.connect(self.handle_screen_capture_window_closed)
            self.screen_capture_window.show()
        
    def start_capture(self):
        if hasattr(self, 'screen_capture_window') and self.screen_capture_window:
            self.record_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.screen_capture_window.start_capture()
        else:
            QMessageBox.information(self, "Info", "You haven't opened the Screen Capture Window yet.")

    def stop_capture(self):
        if hasattr(self, 'screen_capture_window') and self.screen_capture_window:
            self.record_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.screen_capture_window.stop_capture()

    def handle_screen_capture_window_closed(self):
        # Slot to handle the screen capture window being closed
        self.screen_capture_window = None

    def closeEvent(self, event):
        # Check if the screen_capture_window is open and close it
        if self.screen_capture_window is not None:
            self.screen_capture_window.close()
        
        event.accept()


class ScreenCaptureWindow(QMainWindow):
    # Define a custom signal at the class level
    closed = Signal()
  
    def __init__(self):
        super().__init__()
  
        # set the title
        self.setWindowTitle("Screen Capture region")
  
        self.setWindowOpacity(0.5)
  
        # setting  the geometry of window
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry.left() + screen_geometry.width() // 4, 
                         screen_geometry.top() + screen_geometry.height() // 2,
                         screen_geometry.width() // 2, screen_geometry.height() // 3)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)

        # show all the widgets
        self.show()

    def start_capture(self):
        self.timer.start(10000)  # Capture every 1000 milliseconds (1 second)

    def stop_capture(self):
        self.timer.stop()
        QMessageBox.information(self, "Info", "Screen capture stopped.")

    def capture_screen(self):
        global capture_start

        if self.isVisible():
            # 開始測量capture時間
            capture_start = time.time()

            # Capture the screen content within the window's geometry
            screenshot = ImageGrab.grab(bbox=(self.geometry().x(), self.geometry().y(),
                                                self.geometry().x() + self.geometry().width(),
                                                self.geometry().y() + self.geometry().height()))

            # Perform OCR using Google Cloud Vision on the screenshot
            self.perform_ocr(screenshot)

    def closeEvent(self, event):
        # Stop the timer when the screen capture window is closed
        self.timer.stop()
        event.accept()
        self.closed.emit()  # Emit the signal when the window is closed

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
            target_language = "en"  # 將此替換為你想要的目標語言代碼（例如：英文 --> en）
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
    
    # Create the screen capture window and the main recording control window
    #screen_capture_window = ScreenCaptureWindow()
    main_recording_window = MainRecordingWindow()

    # Show the windows
    #screen_capture_window.show()
    main_recording_window.show()
    
    # start the app
    sys.exit(App.exec())
  