# API examples
Real-time tag positions (from the UWB RTLS) and other sensor data can be accessed using different protocols (UDP, TCP, Websocket, MQTT (TCP/WSS)) and in different formats (binary/JSON).
For meta data (client/project/setup configurations), we also have a REST API.

This repo includes the following examples:
* Data API:
  + Binary API:
    - [X] C TCP client & parser
    - [ ] C# TCP client & parser (TODO)
    - [ ] NodeJS TCP client & parser (TODO)
    - [X] Python TCP client & parser
  + JSON api:
    - [X] NodeJS / Browser MQTT WebSocket JS client
    - [X] Python WebSocket client

* REST API:
  + [X] NodeJS / browser example
  + [X] Python example

If you have a preference for a parser in a different language, let us know!
