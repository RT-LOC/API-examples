"""
    RTLOC - Integrated example of reading and printing the distances

    cross.py

    (c) 2021-2023 RTLOC/Callitrix NV. All rights reserved.

    Frederic Mes   <fred@rtloc.com>

    This script demonstrates how to use the RTLOC UDP client to read 
    data from a UDP server, process the data to extract anchor ID, tag ID,
    and distance information, and display this information in a terminal 
    with color highlighting for different ID types.
    
    The script uses the asyncio library to handle the UDP communication 
    asynchronously. The data received from the UDP server is processed 
    and stored in a pandas DataFrame for easy manipulation and display.
    
    The curses library is used to control the terminal display, including 
    clearing the screen for each new set of data and setting colors for 
    different types of IDs. The tag IDs are displayed in red and the anchor IDs 
    are displayed in blue for easy differentiation.
    
    The script is designed to be run from the command line with the IP address 
    and port of the UDP server as arguments.

"""

import socket
import time
import sys
import os
import yaml
import asyncio
sys.path.insert(1, '../../..')

import parsers.socket.Python.udp_client
import parsers.socket.Python.decoder
import parsers.uart.python.uart_api as uart_api

import os
import pandas as pd  # make sure to import pandas
import curses
import numpy as np
import math
import subprocess

# Initialize curses for terminal display control
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()  # start color functionality

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # initialize a color pair for tag IDs
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  # initialize a color pair for anchors
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # initialize a color pair for missing data

async def main():
    # Get the running loop
    loop = asyncio.get_running_loop()

    # Create the UDP client
    udpClient = parsers.socket.Python.udp_client.UDPClient(asyncio.get_running_loop())

    # Print connection information
    print("[UDP] - connecting to (" + ip_addr_server + ") on port " + port + "\n")

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=(ip_addr_server, port))

    # Initialize empty DataFrame to store the data
    
    
    # Initialize sets to keep track of all anchors and tags
    all_anchors = set()
    all_tags = set()
    df = pd.DataFrame(index=list(all_anchors), columns=list(all_tags), dtype=str)  

    while True:
        # Read out the data from the UDP client
        data, frameNr = udpClient.read_data()
        if data != -1:
            # Process the data to extract the tag ID, anchor ID, and distance
            for x in range(len(data)):
                tag_id = data[x][0]
                anchors = data[x][3]
                for idx in anchors:
                    anchor_id = anchors[idx][0]
                    distance = anchors[idx][1]                    
                    # Add anchor_id and tag_id to the sets
                    all_anchors.add(anchor_id)
                    all_tags.add(tag_id)

                    # Store the distance in the DataFrame
                    df.loc[anchor_id, tag_id] = distance
                    
            # Clear the terminal screen
            stdscr.clear()

            # Print the cross-table
            stdscr.addstr(0, 0, "fr = " + str(frameNr) + "\n")

            # Change nans to - instead 
            df = df.fillna("-")
            
            # Print the tag IDs in green 
            
            stdscr.addstr(" " * 6)  # add spaces equal to the width of anchor IDs

            
            for tag_id in df.columns:
                # If significant amount of entries are missing, paint the tag id in red else green
                if list(df.loc[:, tag_id]).count("-") > 5: 
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(str(tag_id).ljust(6) + " ")  # 5 characters for the ID + 1 for space
                    stdscr.attroff(curses.color_pair(3))  # turn off color pair 1

                else: 
                    stdscr.attron(curses.color_pair(1))  # turn on color pair 1
                    stdscr.addstr(str(tag_id).ljust(6) + " ")  # 5 characters for the ID + 1 for space
                    stdscr.attroff(curses.color_pair(1))  # turn off color pair 1
                
            stdscr.addstr("\n")

            # Print the anchor IDs in blue and the distances in default color
            for anchor_id in df.index:
                
                # If anchor is missing significant amount of data, paints the ID in red instead
                if list(df.loc[anchor_id]).count("-") > 5:
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(str(anchor_id).ljust(6)) 
                    stdscr.attroff(curses.color_pair(3))                    
                else: 
                    stdscr.attron(curses.color_pair(2))  # turn on color pair 2
                    stdscr.addstr(str(anchor_id).ljust(6))  # 5 characters for the ID + 1 for space
                    stdscr.attroff(curses.color_pair(2))  # turn off color pair 2
                
                # Curses throws exception if window is too small to print to
                try: 
                    stdscr.addstr(" ".join([str(x).ljust(6) for x in df.loc[anchor_id]]) + "\n")
                except: 
                    os.system("clear")
                    print("Error occured during printing, try increasing window size or running main.py instead \n")
                    exit()
                    
                    
            
            # Refresh the terminal screen to show the new data
            stdscr.refresh()
            
            # Clear the DataFrame for the next iteration, but keep all rows and columns

            df = pd.DataFrame(index=list(all_anchors), columns=list(all_tags))

        # Sleep for a short time to allow other tasks to run
        await asyncio.sleep(0.2)

# Stop curses
curses.echo()
curses.nocbreak()
curses.endwin()

if __name__ == "__main__":
    ####################
    #       UDP        #
    ####################
    param_cnt = len(sys.argv)
    if param_cnt != 3:
        print("[ERR] - parameter issue")
        exit(1)

    ip_addr_server = str(sys.argv[1])
    port = str(sys.argv[2])

    # Print the server IP address
    print(ip_addr_server)

    print("[UDP] - going to start UDP loop")
    asyncio.run(main())