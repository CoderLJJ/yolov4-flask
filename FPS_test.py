import os
import time

import numpy as np
from tensorflow.keras import backend as K
from PIL import Image

from utils.utils import letterbox_image
from yolo import YOLO

'''
该FPS测试不包括前处理（归一化与resize部分）、绘图。
包括的内容为：网络推理、得分门限筛选、非极大抑制。
使用'img/street.jpg'图片进行测试，该测试方法参考库https://github.com/zylo117/Yet-Another-EfficientDet-Pytorch

video.py里面测试的FPS会低于该FPS，因为摄像头的读取频率有限，而且处理过程包含了前处理和绘图部分。
'''
class FPS_YOLO(YOLO):
    def get_FPS(self, image, test_interval):
        # 调整图片使其符合输入要求
        new_image_size = (self.model_image_size[1],self.model_image_size[0])
        boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  

        if self.eager:
            # 预测结果
            input_image_shape = np.expand_dims(np.array([image.size[1], image.size[0]], dtype='float32'), 0)
            out_boxes, out_scores, out_classes = self.yolo_model.predict([image_data, input_image_shape]) 
        else:
            # 预测结果
            out_boxes, out_scores, out_classes = self.sess.run(
                [self.boxes, self.scores, self.classes],
                feed_dict={
                    self.yolo_model.input: image_data,
                    self.input_image_shape: [image.size[1], image.size[0]],
                    K.learning_phase(): 0
                })

        t1 = time.time()
        for _ in range(test_interval):
            if self.eager:
                # 预测结果
                input_image_shape = np.expand_dims(np.array([image.size[1], image.size[0]], dtype='float32'), 0)
                out_boxes, out_scores, out_classes = self.yolo_model.predict([image_data, input_image_shape]) 
            else:
                # 预测结果
                out_boxes, out_scores, out_classes = self.sess.run(
                    [self.boxes, self.scores, self.classes],
                    feed_dict={
                        self.yolo_model.input: image_data,
                        self.input_image_shape: [image.size[1], image.size[0]],
                        K.learning_phase(): 0
                    })
        t2 = time.time()
        tact_time = (t2 - t1) / test_interval
        return tact_time
        
yolo = FPS_YOLO()
test_interval = 100
img = Image.open('img/street.jpg')
tact_time = yolo.get_FPS(img, test_interval)
print(str(tact_time) + ' seconds, ' + str(1/tact_time) + 'FPS, @batch_size 1')
