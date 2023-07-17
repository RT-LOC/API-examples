# Overview
These Python scripts: main.py, cross.py, gui.py is an integrated example of using the RTLOC system for reading and printing distances from anchor sensors. The script is designed to interface with the API provided by cxRTLS.exe, a PC program that gathers data from the anchor sensors. The main.py script connects to this API via UDP broadcast, and decodes the received data using the RTLOC parsers.

# Requirements
This script requires:

- Python 3.7 or higher (due to the use of asyncio).
- cxRTLS 45002 or higher, running on a machine accessible via the network.

# Dependencies
To run the script, you need to have the parsers module in your Python path. The module can be found in the directory three levels up (../../..) from the script. The script inserts this path at runtime. If your structure is different, you might need to adjust this path. The list of required python packages is contained in the docs folder in requirements.txt

# How It Works
The scripts start by creating a UDP client using the UDPClient class from parsers.socket.Python.udp_client. It connects to the IP address and port provided, which should be the address and port that cxRTLS.exe is broadcasting the data to.

After the connection is established, the script enters an infinite loop, where it continuously reads data from the UDP client. If valid data is received, the script processes this data using the RTLOC parsers, extracts the distances and displays them.


# How to Use
You can run the script using the command line. The main.py script takes two arguments: the IP address and the port number to connect to. cross.py has this IP adress and port number in the config.yml file in this directory and the GUI allows for inserting it in the configuration boxes.

## Example:
```
python3 main.py 0.0.0.0 13101
```

In the above example, the script connects to the IP address 0.0.0.0 (which means it listens to any host on the network) on port 13101.

Please note that if you see the error message [ERR] - parameter issue, it means that the script did not receive the correct number of parameters. Make sure you provide both the IP address and the port number.

```
python3 gui.py
```

Opens the GUI in which you can also run the main.py and cross.py scripts and easily switch between the different views aswell as providing a more user friendly experience.
