# Usage
Make sure the RTLOC Manager platform is running on the server. This can be on the same machine as this PC.

## TCP Client
The client is going to initiate a connection with the server.
```
python3 tcp_client.py *ip_address_of_server*
```

## UDP Client
The client is only listening and has no notion of the server's address.
On the Manager platform you need to fill in the IP address you're sending the data to and enable the UDP server. This is the IP address of the PC on which you will be running this code.
```
python3 tcp_client.py *ip_address_of_myself*
```

# Remarks
 - This demo will only work with Python 3.4+, because of the *asyncio* tcp client. But the decoder/parser should be compatible with **Python 2.7+**!
 - Feel free to change this code however you want. Improvements are welcome and can be sent via Pull Requests.