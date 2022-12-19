import cv2
from matplotlib import pyplot as plt
from utils.coreDPU import coreDPU
from utils.drawYolo import drawYolo
from IPython.display import clear_output, Image, display, HTML
import base64
import sys
#image_path = "/home/root/from501_github/original_image_test/test/AQI_1/201407221115.jpg"
image_path =sys.argv[2]
#model_path = "/home/root/from_engineer/yolov4_leaky_spp_m.xmodel"
model_path =sys.argv[1]

#video = cv2.VideoCapture(0)
#ret, image = video.read()
image = cv2.imread(image_path)
#print(image)
image_resize = cv2.resize(image, (416, 416), interpolation=cv2.INTER_AREA)
im_plt = cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB)

    
image_h,image_w = image.shape[0], image.shape[1]
#video.release()



DPU_Class = coreDPU(model_path)
drawYolo_Class = drawYolo(image_h,image_w)    
print(image_h,image_w)
network_out = DPU_Class.runDPU_ObjectDetection(im_plt)
v_boxes, v_labels, v_scores = drawYolo_Class.computeYoloNetWork(network_out)
image_draw = drawYolo_Class.draw_boxes_opencv(image,v_boxes,v_labels,v_scores)


def arrayShow(img):
    _,ret = cv2.imencode('.jpg', img)
    return Image(data=ret)

img = arrayShow(image_draw)
print(type(image_draw))
cv2.imwrite('output.jpg', image_draw)
#display(img)