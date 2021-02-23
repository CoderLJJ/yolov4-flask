from __future__ import unicode_literals
from flask import Flask, render_template, Response
import cv2, time
from yolo import YOLO
from PIL import Image
import numpy as np


class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)
        self.yolo = YOLO()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame = np.array(self.yolo.detect_image(frame))
        # RGBtoBGR满足opencv显示格式
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    return render_template('video.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False, port=5000)
