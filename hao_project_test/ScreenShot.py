# importing the required libraries
  
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
import sys
import pyautogui
import pyscreenshot as ImageGrab
  
  
class Window(QMainWindow):
  
  
    def __init__(self):
        super().__init__()
  
        # set the title
        self.setWindowTitle("Python")
  
        self.setWindowOpacity(0.5)
  
        # setting  the geometry of window
        self.setGeometry(60, 60, 600, 400)

        # Create a timer to capture the screen every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)
        self.timer.start(1000)  # Capture every 1000 milliseconds (1 second)

  
        # show all the widgets
        self.show()

    def capture_screen(self):
       # Capture the screen content within the window's geometry
        screenshot = ImageGrab.grab(bbox=(self.geometry().x(), self.geometry().y(),
                                          self.geometry().x() + self.geometry().width(),
                                          self.geometry().y() + self.geometry().height()))

         # Convert the screenshot to a QImage
        image = QImage(screenshot.tobytes(), screenshot.width, screenshot.height,
                       screenshot.width * 3, QImage.Format_RGB888)

        # Create a QPixmap from the QImage and display it in the label
        pixmap = QPixmap.fromImage(image)
        #self.label_1.setPixmap(pixmap)

        # Save the screenshot as a PNG file
        screenshot.save("screenshot.png")
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())