import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

def hide_window():
    # 隱藏主窗口
    main_window.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("隱藏窗口示例")
    main_window.setGeometry(100, 100, 400, 200)

    button = QPushButton("隱藏窗口", main_window)
    button.clicked.connect(hide_window)

    main_window.show()

    sys.exit(app.exec_())