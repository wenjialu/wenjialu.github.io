# 导入模块
# import pytesseract
# 导入图片库 【注意】需要安装库: pip install Pillow
# 导入库
from PIL import Image

i = Image.Image
print(i)



# 创建图片对象
# image = Image.open("/Users/lujiawen/Desktop/屏幕快照\ 2019-08-26\ 下午9.06.34.png")
# 识别图片
# pytesseract.image_to_string(numImage, config="-psm 7"))