import os
import sys
import toml
import json
import configparser
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 


# 创建一个新的类以用于设置窗口
class SettingsWindow(QDialog):
    # Create a custom signal for closed event
    setting_window_closed = Signal()

    def __init__(self, config):
        super().__init__()

        # 設定 setting window 字體大小
        self._font_size = 16

        # 讀取 config file
        self.config = config

        # 設置參數
        self._text_font_size = self.config['Settings']['text_font_size']
        self._text_font_color = self.config['Settings']['text_font_color']
        self._text_font_color_name = self._text_font_color

        # 设置窗口标题和属性
        self.setWindowTitle("設定")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # 使设置窗口始终位于顶层
        self.resize(300, 200)  # 視窗大小 400 x 300
        self.center()  # 視窗顯示在螢幕正中間

        # text_color_show 和 color_name 初始化
        self.text_color_show = QLabel()
        self.color_name = QLabel()

        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the tab widget for switch pages
        tabs = QTabWidget()
        tabs.addTab(self.create_text_settings(), "文字")
        tabs.addTab(self.create_recognition_settings(), "辨識")
        tabs.addTab(self.create_system_settings(), "系統")
        tabs.addTab(self.create_about_page(), "關於")
        tabs.setStyleSheet("QTabBar::tab { font-size: 14px; }")  # set tabs font size: 14px
 
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
        for text_size in range(10, 25, 2):
            text_size_combo.addItem(str(text_size))
        text_size_combo.setCurrentText(str(self._text_font_size))  # 設置文本字體大小
        text_size_combo.currentTextChanged.connect(self.update_text_size)

        # 创建文本颜色按钮以及預覽顏色
        text_color_label = QLabel("文字顏色:")
        text_color_button = QPushButton("選擇顏色")
        text_color_button.clicked.connect(self.choose_text_color)

        self.text_color_show.setFixedSize(70, 40)  # 設置預覽顏色的範圍大小
        self.text_color_show.setStyleSheet(
            'border: 5px solid lightgray;'  # 邊框線條顏色
            'border-radius: 5px;'  # 邊框圓角
            f'background-color: {self._text_font_color};'  # 設置背景顏色
        )
        self.color_name.setText(self._text_font_color_name)  # 設置顏色名稱


        # 创建 text_size 水平布局
        text_size_layout = QHBoxLayout()
        # 将文本大小标签和下拉框添加到水平布局
        text_size_layout.addWidget(text_size_label)
        text_size_layout.addWidget(text_size_combo)

        # 创建 text_color 水平布局
        text_color_layout = QHBoxLayout()
        # 将文本大小标签和下拉框添加到水平布局
        text_color_layout.addWidget(text_color_label)
        text_color_layout.addWidget(text_color_button)

        # 创建 color_show 水平布局
        color_show_layout = QHBoxLayout()
        # 将文本大小标签和下拉框添加到水平布局
        color_show_layout.addWidget(self.text_color_show)
        color_show_layout.addWidget(self.color_name)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add the horizontal button layout to the vertical layout
        layout.addLayout(text_size_layout)
        layout.addLayout(text_color_layout)
        layout.addLayout(color_show_layout)

        # 设置水平布局作为文本设置的布局
        text_settings.setLayout(layout)

        return text_settings

    def create_recognition_settings(self):
        # 创建一个用于辨识设置的 QWidget
        recognition_settings = QWidget()

        # 建立辨識頻率的下拉式選單
        frequency_label = QLabel("辨識頻率:")
        frequency_combo = QComboBox()
        frequency_combo.addItem("高 (1 秒)")
        frequency_combo.addItem("標準 (2 秒)")
        frequency_combo.addItem("慢 (5 秒)")
        frequency_combo.setCurrentIndex(1)  # 设置默认频率
        frequency_combo.currentIndexChanged.connect(self.update_recognition_frequency)

        # 将小部件添加到辨識设置布局
        layout = QVBoxLayout()
        layout.addWidget(frequency_label)
        layout.addWidget(frequency_combo)
        recognition_settings.setLayout(layout)

        return recognition_settings

    def create_system_settings(self):
        # 创建一个用于系統设置的 QWidget
        system_settings = QWidget()

        # 创建一个按钮以设置 Google 凭证
        set_credentials_button = QPushButton("設定 Google 憑證")
        set_credentials_button.clicked.connect(self.set_google_credentials)

        # 创建一个到凭证教程的链接
        credentials_link = QLabel('<a href="file:///path/to/your/tutorial.html">取得 Google 憑證教學</a>')
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

        # 建立版本訊息、作者名稱、使用說明連結、Github連結
        version_label = QLabel("版本: ver1.0")
        author_label = QLabel("作者: Hsieh Meng-Hao")
        manual_link_label = QLabel('<a href="file:///path/to/your/manual.html">使用說明</a>')
        github_link_label = QLabel('<a href="https://github.com/your/repo">GitHub</a>')

        # 創建一條水平線以隔開 label
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(2)  # 設置線條寬度為 2px

        # 将小部件添加到“关于”页面布局
        layout = QVBoxLayout()
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(line)
        layout.addWidget(manual_link_label)
        layout.addWidget(github_link_label)
        about_page.setLayout(layout)

        return about_page

    def update_text_size(self, selected_font_size):
        # 更新文本字體大小
        self._text_font_size = int(selected_font_size)
        
        # 保存用户设置到JSON配置文件
        self.config["Settings"]["text_font_size"] = self._text_font_size
        with open("config.toml", "w") as config_file:
            toml.dump(self.config, config_file)
        
    def choose_text_color(self):
        # 打开颜色对话框，并根据用户的选择设置文本颜色
        color = QColorDialog.getColor()
        hex_color = ""  # 初始化 hex_color 為空字符串
        if color.isValid():
            name = color.name()
            self.color_name.setText(name)

            # 將選定的顏色轉換為十六進位格式
            hex_color = color.name()

            # 更新 color_name 的字體顏色
            self.color_name.setStyleSheet(f'color: {hex_color};')

            # 更新 text_color_show 的背景顏色
            self.text_color_show.setStyleSheet(
                'border: 5px solid lightgray;'  # 邊框線條顏色
                'border-radius: 5px;'  # 邊框圓角
                f'background-color: {hex_color};' # 更新顏色
            )

            # 保存用户设置到JSON配置文件
            self._text_font_color = hex_color
            self.config["Settings"]["text_font_color"] = self._text_font_color
            with open("config.toml", "w") as config_file:
                toml.dump(self.config, config_file)

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

    def closeEvent(self, event):
        self.setting_window_closed.emit()
        event.accept()


# 主应用程序窗口
class MaincapturingWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()

        self.config = config

        # 设置标题
        self.setWindowTitle("主控制窗口")

        # ... 其余的代码 ...

        # 创建一个按钮以打开设置窗口
        self.settings_button = QPushButton("設定", self)
        self.settings_button.clicked.connect(self.show_settings)

    def show_settings(self):
        self.settings_window = SettingsWindow(self.config)
        self.settings_window.show()

# ... 其余的代码 ...

if __name__ == "__main__":
    # 檢查是否有 config file
    if not os.path.exists("config.toml"):
        # 如果文件不存在，创建默认配置
        default_config = {
            "Settings": {
                "text_font_size": 14,
                "text_color": "white"
                # 添加其他配置项
            }
        }
        with open("config.toml", "w") as config_file:
            toml.dump(default_config, config_file)

    # 載入 config
    with open("config.toml", "r") as config_file:
        config = toml.load(config_file)

    App = QApplication([])

    main_capturing_window = MaincapturingWindow(config)
    main_capturing_window.show()

    sys.exit(App.exec())
