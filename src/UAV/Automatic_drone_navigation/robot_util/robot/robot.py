from abc import ABCMeta, abstractmethod

class Robot(metaclass=ABCMeta):

    def __init__(self, id, type):
        self.id = id
        self.type = type

    #@abstractmethod
    #def move(self):
    #    pass

    #@abstractmethod
    #def get_bluetooth_position(self):
    #    pass

    #@abstractmethod
    #def get_gps_position(self):
    #    pass

    def __str__(self):
        return ('Id:\t\t' + str(self.id) +
                '\nType:\t\t' + self.type)
