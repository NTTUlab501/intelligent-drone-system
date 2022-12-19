# intelligent-drone-system
Using drones as mobile monitoring stations, we build the core chip system of the drone using FPGA, which includes a Neural Engine that can load an AI model for determining the Air Quality Index (AQI) and detecting private objects according to the requirements to provide real-time judgment capabilities. In addition, the drone does not transmit the real-time image directly to the back-end information system via the network, but only sends the determined AQI air quality level results and the corresponding GPS information to the back-end information platform to create an air pollution monitoring map. If the back-end information system needs to retrieve the real-time image of the drone, it will also blur the detected private objects to meet the requirements of trustworthy AI.

## system Design

![System Design](https://github.com/NTTUlab501/intelligent-drone-system/blob/main/images/System%20Design.jpg "System Design")

### Backend

### UAV
### Cryptography
### Air pollution Classification 
### de-identification streaming