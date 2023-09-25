import os
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

# 設定Google Cloud金鑰環境變數，請將YOUR_GOOGLE_CLOUD_KEY替換成你的實際金鑰
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'manifest-surfer-400014-af662a2c9a6c.json'

# 初始化Google Cloud Vision API客戶端
client_vision = vision_v1.ImageAnnotatorClient()

# 初始化Google Cloud Translation API客戶端
client_translate = translate.Client()

# 載入圖片
image_path = 'img001.png'  # 將此替換為你的圖片路徑
with open(image_path, 'rb') as image_file:
    content = image_file.read()

# 使用Google Cloud Vision API進行文字辨識
image = vision_v1.Image(content=content)
response = client_vision.text_detection(image=image)
texts = response.text_annotations

# 提取辨識到的文字
if texts:
    detected_text = texts[0].description
    print("Detected Text: \n")
    print(detected_text)
    print("----------------------------------------")

     # 將辨識的文字按行分割
    lines = detected_text.split('\n')
    
    # 初始化翻譯後的行列表
    translated_lines = []

    # 逐行翻譯
    target_language = 'en'  # 將此替換為你想要的目標語言代碼（例如：英文 --> en）
    for line in lines:
        translated_line = client_translate.translate(line, target_language=target_language)
        translated_lines.append(translated_line['translatedText'])

    # 將翻譯後的行重新組合成一個帶有換行的字符串
    translated_text_with_newlines = '\n'.join(translated_lines)
    
    print(f"Translated Text ({target_language}): \n{translated_text_with_newlines}")

else:
    print("No text detected in the image.")
