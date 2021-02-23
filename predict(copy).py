from yolo import YOLO
from PIL import Image
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
    
yolo = YOLO()

while True:
    # img_path='img/street.jpg'
    img = input('Input image filename:')
    print(img)
    # print(img_path)
    try:
        image = Image.open(img)
        # print(image)
    except:
        print('Open Error! Try again!')
        continue
    else:
        r_image = yolo.detect_image(image)
        # print(r_image)
        r_image.show()
        # r_image.save()
        # break
