1.	以下網站下載所需之KV260開機檔
https://www.xilinx.com/member/forms/download/design-license-xef.html?filename=xilinx-kv260-dpu-v2021.2-v2.0.0.img.gz

2.	使用balenaEtcher(若沒有請先安裝)將img燒錄進SD卡中
3.	使用MobaXterm程式連上板子
4.	輸入登入使用者為root 按下Enter即可進入系統
5.	參考requirement.txt 提到之套件安裝python 套件
6.	下載write_for_git.zip至系統中
7.	解壓縮write_for_git.zip
8.	開始進行推論
(1)	Aqi空氣汙染等級偵測
終端機輸入以下命令
python3 air_pollute.py [../model/KV260_4096.xmodel] [../image/level4_picture.jpg]
(2)	人物去識別化
終端機輸入以下命令
使用python3 trustful_AI.py [../model/yolov4_leaky_spp_m.xmodel][ trustful_AI_example.jpg]
執行結束會輸出一個output.jpg 來顯示執行結果


