import cv2
import numpy as np
from PIL import Image

# 假設您有一個灰度圖像 current_gray_image 和一個灰度圖像 previous_gray_image
# 指定圖像文件的路徑
image01_path = "current1.png"  # 替換為您的圖像文件路徑
image02_path = "current.png"  # 替換為您的圖像文件路徑

# 使用Pillow打開圖像文件
image01 = Image.open(image01_path)
image02 = Image.open(image02_path)

# 將PIL圖像轉換為OpenCV格式
cmp1 = cv2.cvtColor(np.array(image01), cv2.COLOR_RGB2BGR)
cmp2 = cv2.cvtColor(np.array(image02), cv2.COLOR_RGB2BGR)

# 使用OpenCV的相似度比較方法
result = cv2.matchTemplate(cmp2, cmp1, cv2.TM_CCOEFF_NORMED)

# 獲取最大匹配值
max_similarity = np.max(result)
print("匹配度：", max_similarity)

# 使用OpenCV的相似度比較方法
result = cv2.matchTemplate(cmp1, cmp2, cv2.TM_CCOEFF_NORMED)

# 獲取最大匹配值
max_similarity = np.max(result)
print("匹配度：", max_similarity)