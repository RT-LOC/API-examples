# API examples

Real-time tag positions (from the UWB RTLS) and other sensor data can be accessed using different **protocols** (UDP, TCP, Websocket, MQTT (TCP/WSS)) and in different **formats** (binary/JSON).
For meta data (client/project/setup configurations, containing for example floorplans), we also have a REST API.

This repo includes the following examples:
* Data API:
  - Binary over TCP
    - [X] Python
    - [X] C
    - [ ] C#
  - JSON over Websocket
    - [X] Python
    - [X] JavaScript (browser)
  - JSON over MQTT
    - [X] Python
    - [X] JavaScript (NodeJS)
* REST API:
  - [X] Python
  - [X] NodeJS
