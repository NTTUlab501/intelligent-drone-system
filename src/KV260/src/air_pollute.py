import numpy as np
from matplotlib import pyplot as plt
import cv2
import xir
import vart
import time 
import sys

class coreDPU:
    def __init__(self,model_path):
        g = xir.Graph.deserialize(model_path)
        sub = []
        root = g.get_root_subgraph()

        child_subgraph = root.toposort_child_subgraph()
        sub = [s for s in child_subgraph
              if s.has_attr("device") and s.get_attr("device").upper() == "DPU"]
        self.model = sub
        self.__createDPU()
        
    def __createDPU(self):
        self.__dpu = vart.Runner.create_runner(self.model[0],"run")
        input_tensors = self.__dpu.get_input_tensors() #得模型DPU輸入層
        output_tensors = self.__dpu.get_output_tensors() #得模型運算DPU最終層
        self.__input_dims = tuple(input_tensors[0].dims) #(1,224,224,3)
        self.__output_dims = tuple(output_tensors[0].dims) #(1,6)
    def runDPU(self,img) ->int:
        input_data = []
        output_data = []
        input_data = [np.empty(self.__input_dims, dtype =np.float32, order = "C")]
        output_data = [np.empty(self.__output_dims, dtype = np.float32, order = "C")]
        dpu_image = input_data[0]
        dpu_image[0,...] =  img #圖進DPU的BUFFER,

        self.__dpu.execute_async(dpu_image,output_data)
        ans = np.argmax(output_data[0]) +1#分類
        return ans
    
##run DPU Demo


#image_path = "/home/root/from501_github/all_test_AQI_picture/AQI_6/1.jpg"
image_path =sys.argv[2]
#model_path = "/home/root/from_engineer/compiled_model_cut_word/vgg16_cut_word.xmodel"
model_path =sys.argv[1]

image = cv2.imread(image_path)
image_resize = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
im_plt = cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB)

time1 = time.time()
print('Loading...')
DPU_Class = coreDPU(model_path)
time2 = time.time()
level = DPU_Class.runDPU(image_resize)
time3 = time.time()
print("load model consume" ,time2-time1,"seconds")
print("compute consume",time3-time2,"seconds")
print('AQI_LEVEL:',level)