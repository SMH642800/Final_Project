import os
import toml


class ConfigHandler():
    DEFAULT_FONT_SIZE = 14
    DEFAULT_FONT_COLOR = "#FFFFFF"
    DEFAULT_CAPTURE_FREQUENCY = "標準 (2 秒)"
    DEFAULT_GOOGLE_CREDENTIAL_PATH = ""
    
    def __init__(self):
        self.config = self.read_config_file()

    def read_config_file(self):
        # 檢查是否有 config file
        if not os.path.exists("config.toml"):
            self._create_config_file()

        # 載入 config
        with open("config.toml", "r") as config_file:
            config = toml.load(config_file)
        
        return config

    def _create_config_file(self):
        # 如果文件不存在，创建默认配置
        default_config = {
            "Settings": {
                "text_font_size": self.DEFAULT_FONT_SIZE,
                "text_font_color": self.DEFAULT_FONT_COLOR,
                "capture_frequency": self.DEFAULT_CAPTURE_FREQUENCY,
                "google_cloud_key_file_path": self.DEFAULT_GOOGLE_CREDENTIAL_PATH,
            }
        }
        with open("config.toml", "w") as config_file:
            toml.dump(default_config, config_file)

    def set_font_size(self, new_font_size):
        self.config["Settings"]["text_font_size"] = new_font_size
        with open('config.toml', 'w') as f:
            toml.dump(self.config, f)
    
    def set_font_color(self, new_font_color):
        self.config["Settings"]["text_font_color"] = new_font_color
        with open('config.toml', 'w') as f:
            toml.dump(self.config, f)
    
    def set_capture_frequency(self, new_capture_frequency):
        self.config["Settings"]["capture_frequency"] = new_capture_frequency
        with open('config.toml', 'w') as f:
            toml.dump(self.config, f)
    
    def set_google_credential_path(self, new_google_credential_path):
        self.config["Settings"]["google_cloud_key_file_path"] = new_google_credential_path
        with open('config.toml', 'w') as f:
            toml.dump(self.config, f)

    def get_font_size(self):
        return self.config.get('Settings', {}).get('text_font_size', self.DEFAULT_FONT_SIZE)
    
    def get_font_color(self):
        return self.config.get('Settings', {}).get('text_font_color', self.DEFAULT_FONT_COLOR)
    
    def get_capture_frequency(self):
        return self.config.get('Settings', {}).get('capture_frequency', self.DEFAULT_CAPTURE_FREQUENCY)
    
    def get_google_credential_path(self):
        return self.config.get('Settings', {}).get('google_cloud_key_file_path', self.DEFAULT_GOOGLE_CREDENTIAL_PATH)

