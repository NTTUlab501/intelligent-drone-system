# intelligent-drone-system
Using drones as mobile monitoring stations, we build the core chip system of the drone using FPGA, which includes a Neural Engine that can load an AI model for determining the Air Quality Index (AQI) and detecting private objects according to the requirements to provide real-time judgment capabilities. In addition, the drone does not transmit the real-time image directly to the back-end information system via the network, but only sends the determined AQI air quality level results and the corresponding GPS information to the back-end information platform to create an air pollution monitoring map. If the back-end information system needs to retrieve the real-time image of the drone, it will also blur the detected private objects to meet the requirements of trustworthy AI.
## system Design
![System Design](https://github.com/NTTUlab501/intelligent-drone-system/blob/main/images/System%20Design.jpg "System Design")
### Backend
------------
The results of the AQI air quality level monitored by the drones are presented in a more intuitive visual interface, which includes marking each area with different colors on a Google map and being able to retrieve the real-time image of the drone after de-identification.
### UAV
------------
- ### Air pollution Classification 
The AI model based on VGG16 is quantized and can be loaded into the Neural Engine of the drone chip system. Based on the current image captured, it classifies the AQI level of the area to create an air pollution monitoring map on the back-end information system.
- ### de-identification streaming
When the back-end information system needs to retrieve the real-time image of the drone, the AI model based on YOLO is loaded into the Neural Engine of the drone chip system to detect private objects. In addition, when a private object is detected, it is first blurred (pixelated) and then the processed real-time image is transmitted to the back-end information system.
- ### Automatic drone navigation
The drone system has an automated flight control design that can automatically go to the designated area for air pollution monitoring based on the GPS information input by the back-end information system.

### Cryptography
------------