from google.cloud import vision_v1
from google.protobuf.json_format import MessageToDict
import io
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/menghao/Downloads/大學專題資料/googleAPI/manifest-surfer-400014-8bcc91f54c0b.json"

# 使用Google Cloud Vision API的凭据创建客户端
client = vision_v1.ImageAnnotatorClient()

# 读取图像文件
with io.open('image_test.png', 'rb') as image_file:
    content = image_file.read()

# 创建图像对象
image = vision_v1.Image(content=content)

# 使用document_text_detection方法进行文档文本检测
response_doc = client.document_text_detection(image=image)

# 使用text_detection方法进行文本检测
response_text = client.text_detection(image=image)

# 比较两种方法的输出
print("document_text_detection 输出：")
print(response_doc)

print("\n----------------------------------------\n")

print("text_detection 输出：")
print(response_text)
