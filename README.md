<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> f3e320e (yolov4-flask部署深度学习模型)
# yolov4-flask

#### 介绍
yolov4-flask部署深度学习模型，搭建前端界面

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
<<<<<<< HEAD
=======
=======
## YOLOV4：You Only Look Once目标检测模型在Tensorflow2当中的实现
---


### 目录
1. [性能情况 Performance](#性能情况)
2. [实现的内容 Achievement](#实现的内容)
3. [所需环境 Environment](#所需环境)
4. [注意事项 Attention](#注意事项)
5. [小技巧的设置 TricksSet](#小技巧的设置)
6. [文件下载 Download](#文件下载)
7. [预测步骤 How2predict](#预测步骤)
8. [训练步骤 How2train](#训练步骤)
9. [参考资料 Reference](#Reference)

### 性能情况
| 训练数据集 | 权值文件名称 | 测试数据集 | 输入图片大小 | mAP 0.5:0.95 | mAP 0.5 |
| :-----: | :-----: | :------: | :------: | :------: | :-----: |
| VOC07+12+COCO | [yolo4_voc_weights.h5](https://github.com/bubbliiiing/yolov4-tf2/releases/download/v1.0/yolo4_voc_weights.h5) | VOC-Test07 | 416x416 | - | 83.9
| COCO-Train2017 | [yolo4_weight.h5](https://github.com/bubbliiiing/yolov4-tf2/releases/download/v1.0/yolo4_weight.h5) | COCO-Val2017 | 416x416 | 43.1 | 66.0

### 实现的内容
- [x] 主干特征提取网络：DarkNet53 => CSPDarkNet53
- [x] 特征金字塔：SPP，PAN
- [x] 训练用到的小技巧：Mosaic数据增强、Label Smoothing平滑、CIOU、学习率余弦退火衰减
- [x] 激活函数：使用Mish激活函数
- [ ] ……balabla


### 所需环境
tensorflow-gpu==2.2.0  

### 注意事项
代码中的yolo4_weights.h5是基于608x608的图片训练的，但是由于显存原因。我将代码中的图片大小修改成了416x416。有需要的可以修改回来。 代码中的默认anchors是基于608x608的图片的。**这个库里面的h5和Keras的h5不同，不要混用。**  
**视频中说的速度慢问题已经解决了很多，现在train.py和train_eager.py速度差距不大，如果还有改进速度的地方可以私信告诉我!**  
**注意不要使用中文标签，文件夹中不要有空格！**   
**在训练前需要务必在model_data下新建一个txt文档，文档中输入需要分的类，在train.py中将classes_path指向该文件**。  

### 小技巧的设置
在train.py和train_eager.py文件下：   
1、mosaic参数可用于控制是否实现Mosaic数据增强。   
2、Cosine_scheduler可用于控制是否使用学习率余弦退火衰减。   
3、label_smoothing可用于控制是否Label Smoothing平滑。  

在train_eager.py文件下：   
1、regularization参数可用于控制是否实现正则化损失。  

### 文件下载
训练所需的yolo4_weights.h5可在百度网盘中下载。  
链接: https://pan.baidu.com/s/1DNv71lDkeWff2BmnVpgHeg 提取码: myz8  
yolo4_weights.h5是coco数据集的权重。  
yolo4_voc_weights.h5是voc数据集的权重。

### 预测步骤
#### 1、使用预训练权重
a、下载完库后解压，在百度网盘下载yolo4_weights.h5或者yolo4_voc_weights.h5，放入model_data，运行predict.py，输入  
```python
img/street.jpg
```
可完成预测。  
b、利用video.py可进行摄像头检测。  
#### 2、使用自己训练的权重
a、按照训练步骤训练。  
b、在yolo.py文件里面，在如下部分修改model_path和classes_path使其对应训练好的文件；**model_path对应logs文件夹下面的权值文件，classes_path是model_path对应分的类**。  
```python
_defaults = {
    "model_path": 'model_data/yolo4_weight.h5',
    "anchors_path": 'model_data/yolo_anchors.txt',
    "classes_path": 'model_data/coco_classes.txt,
    "score" : 0.5,
    "iou" : 0.3,
    # 显存比较小可以使用416x416
    # 显存比较大可以使用608x608
    "model_image_size" : (416, 416)
}

```
c、运行predict.py，输入  
```python
img/street.jpg
```
可完成预测。  
d、利用video.py可进行摄像头检测。  

### 训练步骤
1、本文使用VOC格式进行训练。  
2、训练前将标签文件放在VOCdevkit文件夹下的VOC2007文件夹下的Annotation中。  
3、训练前将图片文件放在VOCdevkit文件夹下的VOC2007文件夹下的JPEGImages中。  
4、在训练前利用voc2yolo4.py文件生成对应的txt。  
5、再运行根目录下的voc_annotation.py，运行前需要将classes改成你自己的classes。**注意不要使用中文标签，文件夹中不要有空格！**   
```python
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
```
6、此时会生成对应的2007_train.txt，每一行对应其**图片位置**及其**真实框的位置**。  
7、**在训练前需要务必在model_data下新建一个txt文档，文档中输入需要分的类，在train.py中将classes_path指向该文件**，示例如下：   
```python
classes_path = 'model_data/new_classes.txt'    
```
model_data/new_classes.txt文件内容为：   
```python
cat
dog
...
```
8、运行train.py即可开始训练。

### mAP目标检测精度计算更新
更新了get_gt_txt.py、get_dr_txt.py和get_map.py文件。  
get_map文件克隆自https://github.com/Cartucho/mAP  
具体mAP计算过程可参考：https://www.bilibili.com/video/BV1zE411u7Vw

### Reference
https://github.com/qqwweee/keras-yolo3/  
https://github.com/Cartucho/mAP  
https://github.com/Ma-Dan/keras-yolo4  
>>>>>>> 4f6931b (yolov4-flask部署深度学习模型)
>>>>>>> f3e320e (yolov4-flask部署深度学习模型)
