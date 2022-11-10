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


    def connection_made(self, transport):
        print('[UDP] - Connection made')

    def connection_lost(self, exc):
        print("[UDP] - The server closed the connection")
        print("[UDP] - Stop the event loop")
        self.loop.stop()

    def datagram_received(self, data, addr):
        distances_dict, frameNr = self.decoder.decode(data)
        # print(distances_dict)
        self.distances_dict = distances_dict
        self.data_available = True
        self.frameNr = frameNr

    def read_data(self):
        if self.data_available == True:
            # print("DATA AVAILABLE")
            self.data_available = False 
            return self.distances_dict, self.frameNr
        else:
            # print("NOPE")
            return -1, -1
        # while not self.data_available:
        #     time.sleep(0.1)
        self.data_available = False 

        # distance_report = DistanceReport(self.device_id, self.distances_dict)
        # return [distance_report]
        return self.distances_dict, self.frameNr