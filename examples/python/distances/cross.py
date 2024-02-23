"""
RTLOC - Distance Reading and Display

cross.py

(c) 2021-2023 RTLOC/Callitrix NV. All rights reserved.

Frederic Mes <fred@rtloc.com>

This script reads data from an RTLOC UDP server or UART interface, processes it to 
extract anchor IDs, tag IDs, and distance information. It then displays this 
information in a terminal with color-coded ID types for easy differentiation. Tag IDs 
are displayed in red, and anchor IDs are displayed in blue.

The script uses the asyncio library for asynchronous UDP communication, and the 
received data is processed and stored in a pandas DataFrame. The curses library 
controls the terminal display, which includes clearing the screen for each new set of 
data and setting colors for different ID types.

The script should be run from the command line with the configuration file as an argument.
"""

import socket
import time
import sys
import os
import yaml
import asyncio
import pandas as pd
import curses
from collections import deque
import datetime
import struct


sys.path.insert(1, '../../..')

import parsers.socket.Python.udp_client
from parsers.socket.Python.tcp_client import TCPClient
import parsers.socket.Python.decoder
from engine import DebugPostionEngine, Position
import parsers.uart.python.uart_api as uart_api

# Initialize terminal display control with curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()  # start color functionality
stdscr.nodelay(1)  # set getch() non-blocking

# Initialize color pairs for tag and anchor IDs
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # color pair for tag IDs
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  # color pair for anchors

# Initialize data structures and variables
df = pd.DataFrame()
df_updates = pd.DataFrame()
df_first_update_times = pd.DataFrame()
all_anchors = set()
all_tags = set()
start_time = time.time()
show_distances = True
last_update_time = time.time()
df_times = pd.DataFrame()  # DataFrame to store timestamps

# Initialize deques for distances and times
distances_deque = deque(maxlen=int(10/0.01))  # distances deque (10s worth of distances)
times_deque = deque(maxlen=int(10/0.01))  # times deque (10s worth of times)

def parse_time_data(time_data):
    """
    Parses the time data into a readable format.
    Returns a dictionary with source ID as keys and datetime objects as values.
    """
    parsed_data = {}
    # print(time_data)
    #Offset 0 for normal API, offset 1 for data from tag!
    offset = 0

    for source_id2, time_list in time_data.items():        
        year = time_list[1 + offset] + 1980  # year offset
        month = time_list[2 + offset]
        day = time_list[3 + offset]
        hour = time_list[4 + offset]
        minute = time_list[5 + offset]
        second = time_list[6 + offset]
        ms = time_list[7 + offset] * 1000
        source_id = time_list[0]

        # Combine date and time components to form a datetime object
        if ms > 999000:
            print(">>>>> MS !!!!!!!!!!!!!!!!!", ms)
            ms = 999
            second += 1
            if second > 59:
                second = 0
                minute += 1
                if minute > 59:
                    minute = 0
                    hour += 1


        # NOTE:fm - overflow of  hours still possible!
        # Check that ms, second, minute, hour, day, month and year all fall within acceptable range
        if not (0 <= ms <= 999999):
            print("Warning: Milliseconds value out of range (0-999): %d" % ms)
            ms = max(0, min(ms, 999999))
        if not (0 <= second <= 59):
            print("Warning: Seconds value out of range (0-59): %d" % second)
            second = max(0, min(second, 59))
        if not (0 <= minute <= 59):
            print("Warning: Minutes value out of range (0-59): %d" % minute)
            minute = max(0, min(minute, 59))
        if not (0 <= hour <= 23):
            print("Warning: Hours value out of range (0-23): %d" % hour)
            hour = max(0, min(hour, 23))
        if not (1 <= day <= 31):
            print("Warning: Day value out of range (1-31): %d" % day)
            day = max(1, min(day, 31))
        if not (1 <= month <= 12):
            print("Warning: Month value out of range (1-12): %d" % month)
            month = max(1, min(month, 12))
        if not (1980 <= year <= 2099):
            print("Warning: Year value out of range (1980-2099): %d" % year)
            year = max(1980, min(year, 2099))
                    
        timestamp = datetime.datetime(year, month, day, hour, minute, second, ms)
        parsed_data[source_id] = timestamp
        # print(f"Source ID {source_id}: {timestamp}")
        # print(parsed_data)
    return parsed_data

# Place this at the global scope of your script
log_files = {}
# Function to process received data
def process_data(data, frameNr, time_data=None, tag_id=None, source=None):
    global df, df_updates, df_times, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time

    # Common operation for both 'uart' and 'udp'
    def update_df(anchor_id, tag_id, distance):
        all_anchors.add(anchor_id)
        all_tags.add(tag_id)
        df.loc[anchor_id, tag_id] = distance

        if df_updates.get((anchor_id, tag_id)) is None:
            df_first_update_times.loc[anchor_id, tag_id] = time.time()

        df_updates.loc[anchor_id, tag_id] = df_updates.get((anchor_id, tag_id), 0) + 1


    def update_deque(anchor_id, tag_id, distance):
        distances_deque.append(distance)
        times_deque.append(time.time())

    # Update df_times with new time data
    if time_data is not None:
        for source_id, timestamp in time_data.items():
            df_times.loc[source_id, 'timestamp'] = timestamp

    if source == 'uart':
        for anchor_id, distance in data.items():
            update_df(anchor_id, tag_id, distance)
        update_deque(anchor_id, tag_id, distance)
    elif source in ['udp', 'tcp']:
        for x in range(len(data)):
            # print(f"data: {data}")
            # print(f"data[{x}]: {data[x]}")

            if isinstance(data[x], list):
                tag_id = data[x][0]
            else:
                #TODO:fm - fix this properly
                print(f"Unexpected data type for data[{x}]: {type(data[x])}")
                break
            tag_id = data[x][0]
            anchors = data[x][3]


            # Check if logging_distances is enabled
            if config['logging_distances']:
                # Check if the log file for this tag_id already exists
                if tag_id not in log_files:
                    # Generate a timestamp for the filename only when creating a new file
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    log_files[tag_id] = open(f'distances_{tag_id}_{timestamp}.log', 'a')
                
                # Get the log file from the dictionary
                distance_log_file = log_files[tag_id]
                # Write the frame number
                distance_log_file.write(f"{frameNr}")
                anchors = data[x][3]
                for idx in range(len(anchors)):
                    anchor_id = anchors[idx][0]
                    distance = anchors[idx][1]
                    # Write anchor ID and distance
                    distance_log_file.write(f", {anchor_id}, {distance}")
                # End the line for this frame
                distance_log_file.write("\n")


            # if config['logging_distances']:
            #     distance_log_file = open(f'distances_{tag_id}.log', 'a')
            for idx in range(len(anchors)):
                anchor_id = anchors[idx][0]
                distance = anchors[idx][1]
                # if config['logging_distances']:
                #     distance_log_file.write(f"{tag_id}, {anchor_id}, {distance}\n")
                update_df(anchor_id, tag_id, distance)
            # if config['logging_distances']:
            #     distance_log_file.close()
            # else:
            #     print(f"Unexpected data type for anchors: {type(anchors)}")
        # if 'anchor_id' in locals() and 'tag_id' in locals() and 'distance' in locals():
        #     update_deque(anchor_id, tag_id, distance)
    # Clear terminal screen and display updated data
    # stdscr.clear()
    # elapsed_time = times_deque[-1] - times_deque[0] if times_deque else 1
    # distances_per_second = len(distances_deque) / elapsed_time if elapsed_time != 0 else len(distances_deque)
    # stdscr.addstr(0, 0, f"DPS = {distances_per_second:.2f}\n")
    # if config['logging']:
    #     stdscr.attron(curses.color_pair(3))  # turn on color pair 3
    #     stdscr.addstr("Logging is enabled\n")
    #     stdscr.attroff(curses.color_pair(3))  # turn off color pair 3

    ## ENABLE THIS TO DISPLAY DATA IN TERMINAL
    # display_data(frameNr, df_times.to_dict('index'))


# Function to display data in terminal
def display_data(frameNr, time_data):
    global stdscr, df, df_updates, show_distances

    stdscr.addstr("fr = " + str(frameNr) + "\n")

    # Print the tag IDs in red
    stdscr.attron(curses.color_pair(1))  # turn on color pair 1
    stdscr.addstr(" " * 6)  # add spaces equal to the width of anchor IDs
    for tag_id in df.columns:
        stdscr.addstr(str(tag_id).ljust(6) + " ")  # 5 characters for the ID + 1 for space
    stdscr.attroff(curses.color_pair(1))  # turn off color pair 1
    stdscr.addstr("\n")
    
    # Print the anchor IDs in blue and either the distances or the update rates
    # stdscr.addstr("fr = " + str(df.index) + "\n")

    for anchor_id in df.index:
        # stdscr.addstr("id = " + str(anchor_id) + "\n")

        stdscr.attron(curses.color_pair(2))  # turn on color pair 2
        stdscr.addstr(str(anchor_id).ljust(6))  # 5 characters for the ID + 1 for space
        stdscr.attroff(curses.color_pair(2))  # turn off color pair 2

        if show_distances:
            # Print distances
            distances = [f'{x:.0f}'.ljust(6) for x in df.loc[anchor_id]]
            stdscr.addstr(" ".join(distances) + "\n")
        else:
            # Calculate and print the update rates
            update_rates = []
            for tag_id in df.columns:
                first_update_time = df_first_update_times.get((anchor_id, tag_id), times_deque[0])
                elapsed_time = times_deque[-1] - first_update_time if times_deque else 1
                rate = df_updates.loc[anchor_id, tag_id] / elapsed_time if anchor_id in df_updates.index and tag_id in df_updates.columns else 0
                update_rates.append(f'{rate:.1f}'.ljust(6))

            stdscr.addstr(" ".join(update_rates) + "\n")

    # Print the timestamps for each source ID
    stdscr.addstr("\n")
    # print(time_data)
    for source_id, timestamp_dict in time_data.items():
        timestamp = timestamp_dict['timestamp']

        stdscr.addstr(f"Source ID {source_id}: {timestamp}\n")
        
    # Refresh the screen
    stdscr.refresh()

    # Clear the DataFrame for next iteration, but keep all rows and columns
    df = pd.DataFrame(index=list(all_anchors), columns=list(all_tags))
    df_updates = pd.DataFrame(0, index=list(all_anchors), columns=list(all_tags))


async def tcp_main(config):
    global df, df_updates, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time
    host = '10.0.1.158'
    # host = '169.254.68.245'
    host = config['tcp']['host']
    print(host)
    port = 13200
    # config['tcp']['port']

    loop = asyncio.get_running_loop()

    tcp_client = TCPClient()
    
    server = await loop.create_connection(
        lambda: tcp_client,
        host, port)
    
    print(f"[TCP] - connecting to ({host}) on port {port}")

    while True:
        if tcp_client.data_available:
            data, frameNr, raw_time_data = tcp_client.read_data()  # Make sure the TCP client provides time data
            parsed_time_data = parse_time_data(raw_time_data)
            process_data(data, frameNr, parsed_time_data, source='tcp')

        if stdscr.getch() == ord(' '):
            show_distances = not show_distances

        await asyncio.sleep(0.01)




async def udp_main(config):
    global df, df_updates, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time

    ip_addr_server = config['udp']['ip_addr_server']
    port = config['udp']['port']

    loop = asyncio.get_running_loop()

    udpClient = parsers.socket.Python.udp_client.UDPClient(loop)

    print(f"[UDP] - connecting to ({ip_addr_server}) on port {port}")

    #IPV4
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=(ip_addr_server, port))
    #IPV6

    # # transport, protocol = await loop.create_datagram_endpoint(
    # #     lambda: udpClient,
    # #     local_addr=(ip_addr_server, port))

    # transport, protocol = await loop.create_datagram_endpoint(
    #         lambda: udpClient,
    #         local_addr=(ip_addr_server, port),
    #         family=socket.AF_INET6)

    # group_bin = socket.inet_pton(socket.AF_INET6, "ff02::3")
    # mreq = group_bin + struct.pack('@I', 0)
    # # udpClient._sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    # # transport.get_extra_info('socket').setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    # try:
    #     transport.get_extra_info('socket').setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    # except OSError as e:
    #     print(f"Error: {e}")
    #     print(f"IP Address: {ip_addr_server}")
    #     print(f"Port: {port}")


    # Open the file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    files = {}

    while True:
        data, frameNr, raw_time_data = udpClient.read_data()
        if data != -1:
            # print(raw_time_data)
            # stdscr.attron(curses.color_pair(1))  # turn on color pair 1
            # stdscr.addstr("\r\nFrame Number: " + str(frameNr) + "\n")  # print frame number in red
            # stdscr.attroff(curses.color_pair(1))  # turn off color pair 1
            
            if(raw_time_data != -1):
                parsed_time_data = parse_time_data(raw_time_data)
                # Write raw_time_data to the file
                #Check in config.yml that the setting 'logging' is set to 'true'
                # {0: [0, 23, 8, 23, 14, 38, 29, 173, 0, 0], 1: [4140, 23, 8, 23, 13, 58, 45, 52, 135, 169], 2: [4002, 23, 8, 23, 13, 58, 45, 52, 135, 169], 3: [3480, 23, 8, 23, 13, 58, 45, 53, 135, 169]}
                if config['logging']:
                    print("LOGGING1\n")
                    for i in range(len(raw_time_data)):
                        source_id = raw_time_data[i][0]
                        print(source_id)
                        
                        if source_id not in files:
                            print("LOGGING2\n")
                            data_dir = 'data'
                            if not os.path.exists(data_dir):
                                os.makedirs(data_dir)
                            files[source_id] = open(f'{data_dir}/raw_time_data_{timestamp}_{source_id}.txt', 'a')
                        
                        files[source_id].write(str(frameNr) + ", " + str(raw_time_data[i]) + '\n')
                process_data(data, frameNr, parsed_time_data, source='udp')
            # process_data(data, frameNr, tag_id=666, source='uart')

    # #     if data != -1:
    # #         process_data(data, frameNr, source='udp')


        if stdscr.getch() == ord(' '):
            show_distances = not show_distances

        await asyncio.sleep(0.01)


def uart_main(config):
    global df, df_updates, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time

    uart = uart_api.UART(config)
    uart.start_distances = 1
    time.sleep(1)

    while True:
        try:
            uart.uart_in()
            distances = uart.distances_dict
            frame = uart.frameNr

            if distances:
                process_data(distances, frame, tag_id=666, source='uart')

            uart.distances_dict = {}
            time.sleep(0.05)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    # Load configuration file
    config = {}
    with open("config.yml") as yaml_fh:
        config = yaml.safe_load(yaml_fh)

    print(config)
    connection_type = config.get('connection', 'uart')

    if connection_type == 'udp':
        asyncio.run(udp_main(config))
    elif connection_type == 'uart':
        uart_main(config)
    elif connection_type == 'tcp':
        asyncio.run(tcp_main(config))
    else:
        print(f'Unsupported connection type: {connection_type}')


# Stop curses
curses.echo()
curses.nocbreak()
curses.endwin()