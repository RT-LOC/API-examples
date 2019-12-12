# API examples
Real-time tag positions (from the UWB RTLS) and other sensor data can be accessed using different protocols (UDP, TCP, Websocket, MQTT (TCP/WSS)) and in different formats (binary/JSON).
For meta data (client/project/setup configurations), we also have a REST API.

This repo includes the following examples:
* Data API:
  + Binary API:
    - [X] Python TCP client & parser
    - [X] C TCP client & parser
    - [ ] NodeJS TCP client & parser (TODO)
  + JSON api:
    - [X] NodeJS / Browser MQTT websocket JS client

* REST API:
  + [X] NodeJS / browser example

If you have a preference for a parser in a different language, let us know!
