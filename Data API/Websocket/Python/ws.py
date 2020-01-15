import asyncio
import json
import pprint
import websockets

async def connect(
    type_:str = 'ws',
    host:str = 'localhost',
    port: int = 13510
) -> None:
    """Open a WebSocket connection to the server, handling incoming messages.

    Parameters are used to form a URI like 'ws://localhost:1234'.

    ## Parameters
        type_: Type of the connection.
        host: Hostname.
        port: Port.

    ## Returns
        None.
    """
    uri = '{}://{}:{}'.format(type_, host, port)
    print('Initiating connection to {}'.format(uri))

    async with websockets.connect(uri) as websocket:
        if websocket.open:
            print('Connection established')
        async for message in websocket:
            await process_message(message)
    if websocket.closed:
        print('Connection closed')

async def process_message(message: str) -> None:
    """Parse an incoming message, printing it's type and itself.

    ## Parameters
        message:

    ## Returns
        None.
    """
    if 'cx|' in message:
        parsed = json.loads(message[10:])
    elif message[0] == '{':
        parsed = json.loads(message)
    else:
        print('Received: {}'.format(message))

    if 'frames' in parsed:
        print('POSXYZ')
    elif 'anchorList' in parsed:
        print('ALIST')
    elif 'tagList' in parsed:
        print('TLIST')
    elif 'tagStatus' in parsed:
        print('Status')
    else:
        print('UNKNOWN PKT')
    
    pprint.PrettyPrinter(indent=2).pprint(parsed)

if __name__ == '__main__':
    type_ = 'ws'
    host = 'localhost'
    port = 13510

    asyncio.run(connect(type_, host, port))