# from test import run_ActionGroup
from robot_util.Spiderbot import SpiderBot

# run_ActionGroup("2", 4)

robot = SpiderBot(2, "192.168.2.1", 9999)
#robot = SpiderBot(2, "192.168.0.177", 9999)
robot.pynqZ2.connect() # 接pynqZ2的時候打開

robot.start()
