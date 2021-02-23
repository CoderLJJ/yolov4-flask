from yolo import YOLO
from PIL import Image
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

yolo = YOLO()
def image():
    try:
        img ='img/street.jpg'
        print(img)
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
    else:
        r_image = yolo.detect_image(image)
        r_image.show()


if __name__ == '__main__':
    image()
