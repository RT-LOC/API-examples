# Overview
This Python script, main.py, is an integrated example of using the RTLOC system for reading and printing distances from anchor sensors. The script is designed to interface with the API provided by cxRTLS.exe, a PC program that gathers data from the anchor sensors. The main.py script connects to this API via UDP broadcast, and decodes the received data using the RTLOC parsers.

# Requirements
This script requires:

- Python 3.7 or higher (due to the use of asyncio).
- cxRTLS 45002 or higher, running on a machine accessible via the network.

# Dependencies
To run the script, you need to have the parsers module in your Python path. The module can be found in the directory three levels up (../../..) from the script. The script inserts this path at runtime. If your structure is different, you might need to adjust this path.

# How It Works
The script starts by creating a UDP client using the UDPClient class from parsers.socket.Python.udp_client. It connects to the IP address and port provided, which should be the address and port that cxRTLS.exe is broadcasting the data to.

After the connection is established, the script enters an infinite loop, where it continuously reads data from the UDP client. If valid data is received, the script processes this data using the RTLOC parsers, extracts distances array and prints them.


# How to Use
You can run the script using the command line. The script takes two arguments: the IP address and the port number to connect to.

## Example:
```
python3 main.py 0.0.0.0 13101
```

In the above example, the script connects to the IP address 0.0.0.0 (which means it listens to any host on the network) on port 13101.

Please note that if you see the error message [ERR] - parameter issue, it means that the script did not receive the correct number of parameters. Make sure you provide both the IP address and the port number.

