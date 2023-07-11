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

sys.path.insert(1, '../../..')

import parsers.socket.Python.udp_client
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

# Initialize deques for distances and times
distances_deque = deque(maxlen=int(10/0.01))  # distances deque (10s worth of distances)
times_deque = deque(maxlen=int(10/0.01))  # times deque (10s worth of times)

# Function to process received data
def process_data(data, frameNr, tag_id=None, source=None):
    global df, df_updates, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time

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

    if source == 'uart':
        for anchor_id, distance in data.items():
            update_df(anchor_id, tag_id, distance)
        update_deque(anchor_id, tag_id, distance)
    elif source == 'udp':
        for x in range(len(data)):
            tag_id = data[x][0]
            anchors = data[x][3]
            for idx in anchors:
                anchor_id = anchors[idx][0]
                distance = anchors[idx][1]
                update_df(anchor_id, tag_id, distance)
        update_deque(anchor_id, tag_id, distance)
    # Clear terminal screen and display updated data
    stdscr.clear()
    elapsed_time = times_deque[-1] - times_deque[0] if times_deque else 1
    distances_per_second = len(distances_deque) / elapsed_time if elapsed_time != 0 else len(distances_deque)
    stdscr.addstr(0, 0, f"DPS = {distances_per_second:.2f}\n")
    display_data(frameNr)

# Function to display data in terminal
def display_data(frameNr):
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
    for anchor_id in df.index:
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

    # Refresh the screen
    stdscr.refresh()

    # Clear the DataFrame for next iteration, but keep all rows and columns
    df = pd.DataFrame(index=list(all_anchors), columns=list(all_tags))
    df_updates = pd.DataFrame(0, index=list(all_anchors), columns=list(all_tags))


async def udp_main(config):
    global df, df_updates, all_anchors, all_tags, start_time, total_distances, show_distances, last_update_time

    ip_addr_server = config['udp']['ip_addr_server']
    port = config['udp']['port']

    loop = asyncio.get_running_loop()

    udpClient = parsers.socket.Python.udp_client.UDPClient(loop)

    print(f"[UDP] - connecting to ({ip_addr_server}) on port {port}")

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=(ip_addr_server, port))

    while True:
        data, frameNr = udpClient.read_data()
        if data != -1:
            process_data(data, frameNr, source='udp')

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
    else:
        print(f'Unsupported connection type: {connection_type}')

# Stop curses
curses.echo()
curses.nocbreak()
curses.endwin()