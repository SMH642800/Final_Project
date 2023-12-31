# -*- coding: utf-8 -*-

import os
import sys
import shutil
from PySide6.QtCore import * 
from PySide6.QtGui import * 
from PySide6.QtWidgets import * 
from PySide6.QtGui import QDesktopServices

from config_handler import ConfigHandler


# 创建一个新的类以用于设置窗口
class SettingsWindow(QDialog):
    # Create a custom signal for closed event
    setting_window_closed = Signal()

    def __init__(self, config_handler: ConfigHandler):
        super().__init__()

        # 設定 setting window 字體大小
        self._font_size = 16

        # 讀取 config file
        self.config_handle = config_handler

        # Set the window background color to black
        # settings_window_palette = QPalette()
        # settings_window_palette.setColor(QPalette.Window, QColor(70, 70, 70))
        # self.setPalette(settings_window_palette)

        # # Set the window opacity
        self.setWindowOpacity(0.99)

        # 設置參數
        self._text_font_size = self.config_handle.get_font_size()
        self._text_font_color = self.config_handle.get_font_color()
        self._text_font_color_name = self._text_font_color
        self._frequency = self.config_handle.get_capture_frequency()
        self._google_credentials = self.config_handle.get_google_credential_path()

        # 设置窗口标题和属性
        self.setWindowTitle("設定")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # 使设置窗口始终位于顶层
        self.setFixedSize(300, 200)  # 視窗大小 300 x 200
        #self.resize(300, 200)
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

        # set font size to 14px
        text_font = QFont()
        text_font.setPointSize(14)
        text_font.setBold(True) # 設置粗體

        # 创建文本大小下拉框
        text_size_label = QLabel("字體大小 ")
        text_size_label.setFont(text_font)
        text_size_combo = QComboBox()
        #text_size_combo.setFixedWidth(80)
        for text_size in range(10, 25, 2):
            text_size_combo.addItem(str(text_size))
        text_size_combo.setCurrentText(str(self._text_font_size))  # 設置文本字體大小
        text_size_combo.currentTextChanged.connect(self.update_text_size)

        # 创建文本颜色按钮以及預覽顏色
        text_color_label = QLabel("字體顏色 ")
        text_color_label.setFont(text_font)
        text_color_button = QPushButton("選擇顏色")
        #text_color_button.setFixedWidth(70)
        # 使用样式表自定义按钮的外观
        text_color_button.setStyleSheet(
            "QPushButton {"
            "    background-color: rgba(0, 0, 0, 0);"
            "    color: rgb(58, 134, 255);"
            "    border: 2px solid rgb(58, 134, 255);"
            "    border-radius: 8px;"
            "    padding: 3px;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgb(28, 134, 238);"
            "    color: white;"
            "}"
        )

        text_color_button.clicked.connect(self.choose_text_color)

        self.text_color_show = QLabel()
        self.text_color_show.setFixedSize(55, 25)  # 設置預覽顏色的範圍大小
        self.text_color_show.setStyleSheet(
            'border: 2px solid lightgray;'  # 邊框線條顏色
            'border-radius: 5px;'  # 邊框圓角
            f'background-color: {self._text_font_color};'  # 設置背景顏色
        )
        self.color_name = QLabel()
        self.color_name.setText(self._text_font_color_name)  # 設置顏色名稱
        self.color_name.setStyleSheet(f'color: {self._text_font_color_name}; qproperty-alignment: AlignCenter;')
        color_name_font = QFont()
        color_name_font.setPointSize(16)
        color_name_font.setBold(True) # 設置粗體
        self.color_name.setFont(color_name_font)

        # 创建 text_size 水平布局
        text_size_layout = QHBoxLayout()
        # 添加一个占位符来距离左边至少 10px
        text_size_layout.addSpacing(10)
        # 将文本大小标签和下拉框添加到水平布局
        text_size_layout.addWidget(text_size_label)
        # 添加一个60px的空白空間
        text_size_layout.addSpacing(5)
        text_size_layout.addWidget(text_size_combo)
        # 添加一个60px的空白空間
        text_size_layout.addSpacing(10)

        # 创建 text_color 水平布局
        text_color_layout = QHBoxLayout()
        # 添加一个占位符来距离左边至少 10px
        text_color_layout.addSpacing(10)
        # 将文本大小标签和下拉框添加到水平布局
        text_color_layout.addWidget(text_color_label)
        # 添加一个60px的空白空間
        #text_color_layout.addSpacing(40)
        text_color_layout.addWidget(text_color_button)
         # 添加一个60px的空白空間
        text_color_layout.addSpacing(10)

        # 创建 color_show 水平布局
        color_show_layout = QHBoxLayout()
        # 添加一个占位符来距离左边至少 10px
        color_show_layout.addSpacing(12)
        # 将文本大小标签和下拉框添加到水平布局
        color_show_layout.addWidget(self.text_color_show)
        # 添加一个60px的空白空間
        color_show_layout.addSpacing(45)
        color_show_layout.addWidget(self.color_name)
        # 添加一个60px的空白空間
        color_show_layout.addSpacing(10)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add the horizontal button layout to the vertical layout
        layout.addLayout(text_size_layout)
        layout.addLayout(text_color_layout)
        layout.addSpacing(5)
        layout.addLayout(color_show_layout)

        # 设置水平布局作为文本设置的布局
        text_settings.setLayout(layout)

        return text_settings

    def create_recognition_settings(self):
        # 创建一个用于辨识设置的 QWidget
        recognition_settings = QWidget()

        frequency_label = QLabel("辨識頻率 ")

        # set font size to 14px
        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True) # 設置粗體
        frequency_label.setFont(label_font)

        # 建立辨識頻率的下拉式選單
        frequency_combo = QComboBox()
        frequency_combo.addItem("高 (1 秒)")
        frequency_combo.addItem("標準 (2 秒)")
        frequency_combo.addItem("慢 (3 秒)")
        frequency_combo.addItem("非常慢 (5 秒)")
        match self._frequency:
            case "高 (1 秒)":
                frequency_combo.setCurrentIndex(0)  

            case "標準 (2 秒)":
                frequency_combo.setCurrentIndex(1)  

            case "慢 (3 秒)":
                frequency_combo.setCurrentIndex(2)  

            case "非常慢 (5 秒)":
                frequency_combo.setCurrentIndex(3)  

        frequency_combo.currentIndexChanged.connect(self.update_recognition_frequency)

        # 将小部件添加到辨識设置布局
        layout = QHBoxLayout()
        layout.addSpacing(10)  # 添加一个占位符来距离左边至少 10px
        layout.addWidget(frequency_label)
        layout.addWidget(frequency_combo)
        recognition_settings.setLayout(layout)

        return recognition_settings

    def create_system_settings(self):
        # 创建一个用于系統设置的 QWidget
        system_settings = QWidget()

        # set font size to 14px
        font = QFont()
        font.setPointSize(14)
        font.setBold(True) # 設置粗體

        # 创建一个按钮以设置 Google 凭证
        set_credentials_button = QPushButton("設定 Google 憑證")
        set_credentials_button.setFont(font)
        set_credentials_button.clicked.connect(self.set_google_credentials)
        # 使用样式表自定义按钮的外观
        set_credentials_button.setStyleSheet(
            "QPushButton {"
            "    background-color: rgba(0, 0, 0, 0);"
            "    color: rgb(58, 134, 255);"
            "    border: 2px solid rgb(58, 134, 255);"
            "    border-radius: 8px;"
            "    padding: 3px;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgb(28, 134, 238);"
            "    color: white;"
            "}"
        )

        # 創建如何取得google憑證連結
        current_directory = os.path.dirname(os.path.abspath(__file__))
        new_file_path = os.path.join(current_directory, "test.html")
        self.credentials_link = QLabel(f'<a href="file://{new_file_path}">如何取得 Google 憑證？</a>')
        self.credentials_link.setFont(font)
        self.credentials_link.setStyleSheet("QLabel { qproperty-alignment: AlignCenter; } ")
        self.credentials_link.setOpenExternalLinks(True)  # 允許外部連結
        self.credentials_link.linkActivated.connect(self.open_google_credential_settings_link)

        # 将小部件添加到系統设置布局
        layout = QVBoxLayout()
        layout.addSpacing(15)  # 添加一个占位符来距离左边至少 10px
        layout.addWidget(set_credentials_button)
        layout.addWidget(self.credentials_link)
        layout.addSpacing(15)  # 添加一个占位符来距离左边至少 10px
        system_settings.setLayout(layout)

        return system_settings
    
    def open_google_credential_settings_link(self, url):
        # 使用 QDesktopServices 打開 URL
        QDesktopServices.openUrl(QUrl(url))

    def create_about_page(self):
        # 创建一个用于“关于”页面的 QWidget
        about_page = QWidget()

        # set font size to 14px
        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True) # 設置粗體

        # 建立版本訊息、作者名稱
        version_label = QLabel("版本: ver1.0")
        author_label = QLabel("作者: Hsieh Meng-Hao")

        # 創建使用說明連結、Github連結
        current_directory = os.path.dirname(os.path.abspath(__file__))
        manual_file_path = os.path.join(current_directory, "manual.html")
        github_file_path = os.path.join(current_directory, "githublink.html")
        self.manual_link = QLabel(f'<a href="file://{manual_file_path}"><span> &lt; </span>使用說明<span> &gt; </span></a>')
        self.github_link = QLabel(f'<a href="file://{github_file_path}"><span> &lt; </span>GitHub<span> &gt; </span></a>')
        self.manual_link.setFont(label_font)
        self.github_link.setFont(label_font)
        self.manual_link.setOpenExternalLinks(True)  # 允許外部連結
        self.manual_link.linkActivated.connect(self.open_manual_link)
        self.github_link.setOpenExternalLinks(True)  # 允許外部連結
        self.github_link.linkActivated.connect(self.open_github_website_link)

        # 創建一條水平線以隔開 label
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1.5)  # 設置線條寬度為 2px

        # 将小部件添加到“关于”页面布局
        layout = QVBoxLayout()
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(line)
        layout.addWidget(self.manual_link)
        layout.addWidget(self.github_link)
        about_page.setLayout(layout)

        return about_page
    
    def open_manual_link(self, url):
        # 使用 QDesktopServices 打開 URL
        QDesktopServices.openUrl(QUrl(url))

    def open_github_website_link(self, url):
        # 使用 QDesktopServices 打開 URL
        QDesktopServices.openUrl(QUrl(url))

    def update_text_size(self, selected_font_size):
        # 更新文本字體大小
        self._text_font_size = int(selected_font_size)
        
        # 保存用户设置到JSON配置文件
        self.config_handle.set_font_size(self._text_font_size)
        
    def choose_text_color(self):
        # 打开颜色对话框，并根据用户的选择设置文本颜色
        color = QColorDialog.getColor()
        hex_color = ""  # 初始化 hex_color 為空字符串
        if color.isValid():
            name = color.name().upper()
            self.color_name.setText(name)

            # 將選定的顏色轉換為十六進位格式
            hex_color = color.name()

            # 更新 color_name 的字體顏色
            self.color_name.setStyleSheet(f'color: {hex_color};')

            # 更新 text_color_show 的背景顏色
            self.text_color_show.setStyleSheet(
                'border: 2px solid lightgray;'  # 邊框線條顏色
                'border-radius: 5px;'  # 邊框圓角
                f'background-color: {hex_color};' # 更新顏色
            )

            # 保存用户设置到 TOML 配置文件
            self._text_font_color = hex_color.upper()
            self.config_handle.set_font_color(self._text_font_color)

    def update_recognition_frequency(self, selected_frequency):
        # 更新偵測的頻率
        match selected_frequency:
            case 0:
                self._frequency = "高 (1 秒)"

            case 1:
                self._frequency = "標準 (2 秒)"

            case 2:
                self._frequency = "慢 (3 秒)" 

            case 3:
                self._frequency = "非常慢 (5 秒)" 
        
        # 保存用户设置到 TOML 配置文件
        self.config_handle.set_capture_frequency(self._frequency)

    def set_google_credentials(self):
        # 打开一个文件对话框，让用户选择 Google 凭证文件
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setWindowTitle("选择 Google 凭证文件")
        #file_dialog.exec()

        # 获取所选文件路径并根据文件路径设置 Google 凭证
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                credentials_file = selected_files[0]  # 获取第一个选择的文件
                project_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的目录
                new_file_path = os.path.join(project_dir, os.path.basename(credentials_file))
                
                previous_file_path = self.config_handle.get_google_credential_path()
                if os.path.exists(previous_file_path):
                    os.remove(previous_file_path)  # 如果文件已存在，先删除它

                try:
                    shutil.copy(credentials_file, new_file_path)
                    # 保存用户设置到 TOML 配置文件
                    self.config_handle.set_google_credential_path(new_file_path)
                except Exception as e:
                    pass

    def closeEvent(self, event):
        self.setting_window_closed.emit()
        event.accept()

if __name__ == "__main__":
    config_handler = ConfigHandler()

    # create pyqt5 app
    App = QApplication(sys.argv)
    
    # Create the screen capture window and the main capturing control window
    settings_window = SettingsWindow(config_handler)

    # Show the windows
    settings_window.show()

    count = 0
    
    # start the app
    sys.exit(App.exec())
  