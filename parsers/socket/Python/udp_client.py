'''
 * Copyright (c) 2018 - 2019 - RTLOC
 * 
 * This file is part of RTLOC API tools.
 *
 * RTLOC API tools is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 * RTLOC API tools is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  To get a copy of the GNU General Public License see <https://www.gnu.org/licenses/>.
'''
import asyncio
# from decoder import Decoder
import sys
sys.path.insert(1, '../..')
from parsers.socket.Python.decoder import Decoder

import sys

class UDPClient(asyncio.Protocol):
    def __init__(self, loop):
        print("[UDP] - init client")
        self.loop = loop
        self.decoder = Decoder()
        self.distances_dict = {}
        self.data_available = False
        self.frameNr = 0
        self.time_data = {}


    def connection_made(self, transport):
        print('[UDP] - Connection made')

    def connection_lost(self, exc):
        print("[UDP] - The server closed the connection")
        print("[UDP] - Stop the event loop")
        self.loop.stop()

    # import logging
    # logging.basicConfig(filename='udp_client.log', level=logging.DEBUG)


    def datagram_received(self, data, addr):
        # print(f'Length of the package: {len(data)}')
        distances_dict, frameNr, time_data = self.decoder.decode(data)

        # # logging.debug(f'Received packet: {data}')
        # # logging.debug(f'Frame Nr: {frameNr}')
        # # logging.debug(f'Time data: {time_data}')
        
        # print(f'Received packet: {data}')
        # print(f'Frame Nr: {frameNr}')
        # print(f'Time data: {time_data}')

        self.distances_dict = distances_dict
        self.data_available = True
        self.frameNr = frameNr
        # return
        self.time_data = time_data

        # # Print current PC time
        import datetime
        # print(datetime.datetime.now())
        # print("\n\r")

        # Calculate and print time difference to previous packet
        current_time = datetime.datetime.now()
        if hasattr(self, 'previous_time'):
            time_difference = current_time - self.previous_time
            # print(f'Time difference to previous packet: {time_difference}\r')
        self.previous_time = current_time

        # print(time_data)

    def read_data(self):
        if self.data_available == True:
            self.data_available = False 
            return self.distances_dict, self.frameNr, self.time_data
        else:
            # print("NOPE")
            return -1, -1, -1
        # while not self.data_available:
        #     time.sleep(0.1)
        self.data_available = False 

        # distance_report = DistanceReport(self.device_id, self.distances_dict)
        # return [distance_report]
        return self.distances_dict, self.frameNr, self.time_data