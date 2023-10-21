from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QApplication

app = QApplication([])

button = QPushButton("Click me")
icon = QIcon.fromTheme("document-new")  # 使用 "document-new" 預設 icon
button.setIcon(icon)
button.show()

app.exec()