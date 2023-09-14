from PIL import ImageGrab
import subprocess
image_screenshot= ImageGrab.grab()
image_screenshot.save("screen.png")
subprocess.run(["C:\Program Files\Tesseract-OCR\\tesseract.exe", "screen.png", "out"]) 