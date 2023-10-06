import sys
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 

# 创建一个新的类以用于设置窗口
class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和属性
        self.setWindowTitle("設定")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # 使设置窗口始终位于顶层
        self.resize(400, 300)  # 視窗大小 400 x 300
        self.center()  # 視窗顯示在螢幕正中間

        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the tab widget for switch pages
        tabs = QTabWidget()
        tabs.addTab(self.create_text_settings(), "文字")
        tabs.addTab(self.create_recognition_settings(), "辨識")
        tabs.addTab(self.create_system_settings(), "系統")
        tabs.addTab(self.create_about_page(), "關於")
 
        layout.addWidget(tabs)

    
    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = screen_geometry.height() // 5
        self.move(x, y)

    def create_text_settings(self):
        # 创建一个用于文本设置的 QWidget
        text_settings = QWidget()

        # 创建文本大小下拉框
        text_size_label = QLabel("文字大小:")
        text_size_combo = QComboBox()
        for size in range(10, 21, 2):
            text_size_combo.addItem(str(size))
        text_size_combo.setCurrentText("14")  # 设置默认文本大小
        text_size_combo.currentTextChanged.connect(self.update_text_size)

        # 创建文本颜色按钮
        text_color_label = QLabel("文字顏色:")
        text_color_button = QPushButton("選擇顏色")
        text_color_button.clicked.connect(self.choose_text_color)

        # 将小部件添加到文本设置布局
        layout = QVBoxLayout()
        layout.addWidget(text_size_label)
        layout.addWidget(text_size_combo)
        layout.addWidget(text_color_label)
        layout.addWidget(text_color_button)
        text_settings.setLayout(layout)

        return text_settings

    def create_recognition_settings(self):
        # 创建一个用于辨识设置的 QWidget
        recognition_settings = QWidget()

        # 创建辨识频率下拉框
        frequency_label = QLabel("辨識頻率:")
        frequency_combo = QComboBox()
        frequency_combo.addItem("高 (1 秒)")
        frequency_combo.addItem("標準 (2 秒)")
        frequency_combo.addItem("慢 (5 秒)")
        frequency_combo.setCurrentIndex(1)  # 设置默认频率
        frequency_combo.currentIndexChanged.connect(self.update_recognition_frequency)

        # 创建辨識靈敏度下拉框
        sensitivity_label = QLabel("辨識靈敏度:")
        sensitivity_combo = QComboBox()
        sensitivity_combo.addItem("低 (0.6)")
        sensitivity_combo.addItem("普通 (0.75)")
        sensitivity_combo.addItem("高 (0.9)")
        sensitivity_combo.setCurrentIndex(1)  # 设置默认靈敏度
        sensitivity_combo.currentIndexChanged.connect(self.update_recognition_sensitivity)

        # 将小部件添加到辨識设置布局
        layout = QVBoxLayout()
        layout.addWidget(frequency_label)
        layout.addWidget(frequency_combo)
        layout.addWidget(sensitivity_label)
        layout.addWidget(sensitivity_combo)
        recognition_settings.setLayout(layout)

        return recognition_settings

    def create_system_settings(self):
        # 创建一个用于系統设置的 QWidget
        system_settings = QWidget()

        # 创建一个按钮以设置 Google 凭证
        set_credentials_button = QPushButton("設定 Google 凭证")
        set_credentials_button.clicked.connect(self.set_google_credentials)

        # 创建一个到凭证教程的链接
        credentials_link = QLabel('<a href="file:///path/to/your/tutorial.html">取得凭证教程</a>')
        credentials_link.setOpenExternalLinks(True)

        # 将小部件添加到系統设置布局
        layout = QVBoxLayout()
        layout.addWidget(set_credentials_button)
        layout.addWidget(credentials_link)
        system_settings.setLayout(layout)

        return system_settings

    def create_about_page(self):
        # 创建一个用于“关于”页面的 QWidget
        about_page = QWidget()

        # 创建包含版本和作者信息的标签
        version_label = QLabel("版本: 1.0")
        author_label = QLabel("作者: 你的名字")

        # 创建用于其他信息的文本浏览器
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml('<a href="file:///path/to/your/manual.html">用户手册</a><br><a href="https://github.com/your/repo">GitHub</a>')

        # 将小部件添加到“关于”页面布局
        layout = QVBoxLayout()
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(text_browser)
        about_page.setLayout(layout)

        return about_page

    def update_text_size(self, text):
        # 根据用户选择的文本大小更新应用程序中的文本大小
        # 您可以使用 'text' 变量来访问所选的大小
        pass

    def choose_text_color(self):
        # 打开颜色对话框，并根据用户的选择设置文本颜色
        color = QColorDialog.getColor()
        if color.isValid():
            # 更新文本颜色
            pass

    def update_recognition_frequency(self, index):
        # 根据用户选择的频率更新辨识频率
        # 您可以使用 'index' 变量来访问所选的索引
        pass

    def update_recognition_sensitivity(self, index):
        # 根据用户选择的靈敏度更新辨識靈敏度
        # 您可以使用 'index' 变量来访问所选的索引
        pass

    def set_google_credentials(self):
        # 打开一个文件对话框，让用户选择 Google 凭证文件
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setWindowTitle("选择 Google 凭证文件")
        file_dialog.exec()

        # 获取所选文件路径并根据文件路径设置 Google 凭证
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            credentials_file = selected_files[0]  # 获取第一个选择的文件
            # 根据文件路径设置 Google 凭证
            pass


# 主应用程序窗口
class MaincapturingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置标题
        self.setWindowTitle("主控制窗口")

        # ... 其余的代码 ...

        # 创建一个按钮以打开设置窗口
        self.settings_button = QPushButton("設定", self)
        self.settings_button.clicked.connect(self.show_settings)

    def show_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

# ... 其余的代码 ...

if __name__ == "__main__":
    App = QApplication([])

    main_capturing_window = MaincapturingWindow()
    main_capturing_window.show()

    sys.exit(App.exec())
