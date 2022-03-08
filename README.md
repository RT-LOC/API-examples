# API examples

Real-time tag positions (from the UWB RTLS) and other sensor data can be accessed using different **protocols** (UDP, TCP, Websocket, MQTT (TCP/WSS)) and in different **formats** (binary/JSON).
For meta data (client/project/setup configurations, containing for example floorplans), we also have a REST API.

This repo includes the following examples:
* Local data API:
  - Binary over TCP
    - [X] Python
    - [X] C
    - [X] C#
  - JSON over (local) MQTT
    - [X] Python
    - [X] JavaScript (NodeJS)
  - JSON over (local) Websocket
    - [ ] JavaScript (browser)
