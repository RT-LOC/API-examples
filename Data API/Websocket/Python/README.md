# Websocket connection

Our desktop software can open up a websocket server.
This demo code sets up a websocket client which connects to the server and prints out received messages.

## Dependencies

* Python 3 (Specifically 3.8.1, but should work in other versions too)
* [websockets](https://github.com/aaugustin/websockets)

## Getting started

* Make sure the server details are correct (host/port)
* Install dependencies with:
```
pip3 install -r requirements.txt
```
* And then run the script:
```
python3 ws.py
```

![Console view](/Data%20API/Websocket/Python/console.png?raw=true "Console API messages")