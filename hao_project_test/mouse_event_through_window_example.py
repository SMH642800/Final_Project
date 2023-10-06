from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

app = QApplication([])

def show_information():
    QMessageBox.information(None, "Information", "This is an information message.")

def show_warning():
    QMessageBox.warning(None, "Warning", "This is a warning message.")

def show_error():
    QMessageBox.critical(None, "Error", "This is an error message.")

def ask_question():
    result = QMessageBox.question(None, "Question", "Do you want to continue?", QMessageBox.Yes | QMessageBox.No)
    if result == QMessageBox.Yes:
        print("User clicked 'Yes'")
    else:
        print("User clicked 'No'")

main_window = QMainWindow()
button_info = QPushButton("Show Information Box", main_window)
button_warning = QPushButton("Show Warning Box", main_window)
button_error = QPushButton("Show Error Box", main_window)
button_question = QPushButton("Ask a Question", main_window)

button_info.clicked.connect(show_information)
button_warning.clicked.connect(show_warning)
button_error.clicked.connect(show_error)
button_question.clicked.connect(ask_question)

main_window.setCentralWidget(button_info)
main_window.addToolBar(button_warning)
main_window.addToolBar(button_error)
main_window.addToolBar(button_question)

main_window.show()

app.exec()