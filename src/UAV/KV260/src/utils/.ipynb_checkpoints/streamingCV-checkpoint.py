import cv2
import threading

class streamingCV:
    def __init__(self,video_path):
        self.__video = cv2.VideoCapture(video_path)
        self.__video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.ret = False
        self.image = []
        if video_path == 0:
            self.__video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.__video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("USE Camera")
        else:
            print("USE Video")
        self.frame_width = int(self.__video.get(3))
        self.frame_height = int(self.__video.get(4))
        
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #self.__out = cv2.VideoWriter('output.avi', fourcc, 30.0,(self.frame_width, self.frame_height))
        
        t = threading.Thread(target =self.__Start_streaming,name = "Stream")
        t.setDaemon(True)
        t.start()
    
    def __Start_streaming(self):
        while(True):
            try:
                ret, frame = self.__video.read()
                self.ret = ret
                if not ret:
                    break
                self.image = frame
                cv2.waitKey(10)
                
            except KeyboardInterrupt:
                self.__video.release()
                self.__out.release()
            except Exception as a:
                print(a)
    def close_streaming(self):
        self.__video.release()
    def get_frame(self):
        return self.image
    def get_frame_width(self):
        return self.frame_width
    def get_frame_height(self):
        return self.frame_height
