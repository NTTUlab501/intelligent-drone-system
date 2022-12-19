1. Click the link below to download the required KV260 boot filehttps://www.xilinx.com/member/forms/download/design-license-xef.html?filename=xilinx-kv260-dpu-v2021.2-v2.0.0.img.gz

1.	使用balenaEtcher(若沒有請先安裝)將img燒錄進SD卡中
2.	使用MobaXterm程式連上板子
3.	輸入登入使用者為root 按下Enter即可進入系統
4.	Refer to the package mentioned in requirement.txt to install the python package
5.	下載write_for_git.zip至系統中
6.	解壓縮write_for_git.zip
7.	start model inference
(1)	AQI Air Pollution Classification
Enter the following command in the terminal.
python3 air_pollute.py [../model/KV260_4096.xmodel] [../image/level4_picture.jpg]
(2) Character de-identification
Enter the following command in the terminal.
python3 trustful_AI.py [../model/yolov4_leaky_spp_m.xmodel][ trustful_AI_example.jpg]
At the end of the execution, an output.jpg will be output as the execution result.

