# import numpy as np
# from PIL import Image
# from flask import Flask, render_template, Response
# from yolo import YOLO
# import cv2,time
# fps=0.0
# yolo = YOLO()
# class VideoCamera(object):
#     def __init__(self):
#
#         #这个有问题的
#         self.cap = cv2.VideoCapture(0)
#         ref, frame =  self.cap .read()
#         # 格式转变，BGRtoRGB
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # 转变成Image
#         frame = Image.fromarray(np.uint8(frame))
#         # 进行检测
#         frame = np.array(yolo.detect_image(frame))
#         # RGBtoBGR满足opencv显示格式
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#
#         self.frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#
#     def __del__(self):
#         self.cap.release()
#
#
#     def get_frame(self):
#         image=self.frame
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
#
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000,debug=False)


#
#
#
# import numpy as np
# from PIL import Image
# from flask import Flask, render_template, Response
# from yolo import YOLO
# import cv2,time
# fps=0.0
# class VideoCamera(object):
#     def __init__(self):
#
#         #这个有问题的
#         self.cap = cv2.VideoCapture(0)
#         self.yolo=YOLO()
#
#     def __del__(self):
#         self.cap.release()
#
#
# def get_frame():
#         video=VideoCamera()
#         if video.cap.isOpened():
#             ref, frame = video.cap.read()
#             # 格式转变，BGRtoRGB
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#             # 转变成Image
#             frame = Image.fromarray(np.uint8(frame))
#             # 进行检测
#             frame = np.array(video.yolo.detect_image(frame))
#             # RGBtoBGR满足opencv显示格式
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#
#
#
#             ret, jpeg = cv2.imencode('.jpg',frame )
#             return jpeg.tobytes()
#
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# def gen():
#     while True:
#         frame = get_frame()
#         yield (b'--frame\r\n'#这个是一个迭代器的容器
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000,debug=False)


# #-*-encoding:utf-8-*-
# #必须用英文
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
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        # 将图片转为编码输出
        return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('linjia.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


# def show_():
#     app.run(host='127.0.0.1', debug=False, port=5000)#取消Debug调试
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False, port=5000)
# show_()
