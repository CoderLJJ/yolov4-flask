import base64
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from yolo import YOLO
from PIL import Image
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
app = Flask(__name__)
"""
Flask如何读取服务器本地图片, 并返回图片流给前端显示
"""


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
        return img_stream


@app.route('/')  # 主页
def index():
    return render_template('image.html')


@app.route('/success', methods=['POST', 'GET'])
def image():
    yolo = YOLO()
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, secure_filename(f.filename))
        f.save(f.filename)
        img = f.filename
        image = Image.open(img)
        r_image = yolo.detect_image(image)
        img_path = r'C:\Users\81316\PycharmProjects\yolov4-flask\static\lin.jpg'
        r_image.save(img_path)
        upload_path = return_img_stream(upload_path)
        img_stream = return_img_stream(img_path)
        return render_template('image.html', img_stream=img_stream, upload_path=upload_path)


if __name__ == '__main__':
    app.run()
