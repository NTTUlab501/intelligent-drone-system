import os

class WebCam(object):
    def __init__(self):
        self.__free = True

    def take_photo(self):
        if self.__free:
            self.__free = False
            action = "fswebcam -p YUYV -d /dev/video0 -r 480x360 \
                --no-banner rgb.jpg"
            os.system(action)
            self.__free = True