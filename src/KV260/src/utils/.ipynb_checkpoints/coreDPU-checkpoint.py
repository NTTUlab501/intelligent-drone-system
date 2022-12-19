import numpy as np
import xir
import vart

class coreDPU:
    def __init__(self,model_path):
        g = xir.Graph.deserialize(model_path)
        sub = []
        root = g.get_root_subgraph()
        
        self.__DPU_Status = False
        
        child_subgraph = root.toposort_child_subgraph()
        sub = [s for s in child_subgraph
              if s.has_attr("device") and s.get_attr("device").upper() == "DPU"]
        self.model = sub
        #self.__createDPU()
    def __createDPU_ObjectDetection(self):
        self.__dpu = vart.Runner.create_runner(self.model[0],"run")
        input_tensors = self.__dpu.get_input_tensors() #得模型DPU輸入層
        output_tensors = self.__dpu.get_output_tensors() #得模型運算DPU最終層
        self.__input_dims = tuple(input_tensors[0].dims) #(1,224,224,3)
        self.__output_dims1 = tuple(output_tensors[0].dims)
        self.__output_dims2 = tuple(output_tensors[1].dims)
        self.__output_dims3 = tuple(output_tensors[2].dims)#(1,6)
        #self.__output_dims = [self.__output_dims1,self.__output_dims2,self.__output_dims3]
        #print(np.shape(self.__output_dims))
    def runDPU_ObjectDetection(self,img):
        if self.__DPU_Status == False:
            self.__createDPU_ObjectDetection()
            self.__DPU_Status = True
        img = img.astype('float32')
        img /= 255.0
        input_data = []
        output_data_1 = []
        output_data_2 = []
        output_data_3 = []
        input_data = [np.empty(self.__input_dims, dtype =np.float32, order = "C")]
        output_data_1 = [np.empty(self.__output_dims1, dtype = np.float32, order = "C")]
        output_data_2 = [np.empty(self.__output_dims2, dtype = np.float32, order = "C")]
        output_data_3 = [np.empty(self.__output_dims3, dtype = np.float32, order = "C")]

        output_data  = [output_data_1[0],output_data_2[0],output_data_3[0]]

        dpu_image = input_data[0]
        dpu_image[0,...] =  img #圖進DPU的BUFFER,

        dpu_sync  = self.__dpu.execute_async(dpu_image,output_data)
        self.__dpu.wait(dpu_sync)
        #ans = np.argmax(output_data[0]) +1#分類
        #print(output_data[0])
        #print('AQI_LEVEL:' + str(ans+1))
        return output_data    
    
        
    def __createDPU_Classifiation(self):
        self.__dpu = vart.Runner.create_runner(self.model[0],"run")
        input_tensors = self.__dpu.get_input_tensors() #得模型DPU輸入層
        output_tensors = self.__dpu.get_output_tensors() #得模型運算DPU最終層
        self.__input_dims = tuple(input_tensors[0].dims) #(1,224,224,3)
        self.__output_dims = tuple(output_tensors[0].dims) #(1,6)
    
    def runDPU_Classifiation(self,img) ->int:
        
        if self.__DPU_Status == False:
            self.__createDPU_Classifiation()
            self.__DPU_Status = True

        input_data = []
        output_data = []
        input_data = [np.empty(self.__input_dims, dtype =np.float32, order = "C")]
        output_data = [np.empty(self.__output_dims, dtype = np.float32, order = "C")]
        dpu_image = input_data[0]
        dpu_image[0,...] =  img #圖進DPU的BUFFER,

        dpu_sync = self.__dpu.execute_async(dpu_image,output_data)
        self.__dpu.wait(dpu_sync)
        ans = np.argmax(output_data[0]) +1 #分類
        #print(output_data[0])
        #print('AQI_LEVEL:' + str(ans+1))
        return ans 