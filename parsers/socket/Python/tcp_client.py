'''
 * Copyright (c) 2018 - 2023 - RTLOC
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
import sys

sys.path.insert(1, '../..')
from parsers.socket.Python.decoder import Decoder

class TCPClient(asyncio.Protocol):
    def __init__(self):
        print("[TCP] - init client")
        self.decoder = Decoder()
        self.distances_dict = {}
        self.data_available = False
        self.frameNr = 0

    def connection_made(self, transport):
        print('[TCP] - Connection made')
        self.transport = transport

    def connection_lost(self, exc):
        print("[TCP] - The server closed the connection")
        self.loop = asyncio.get_event_loop()
        self.loop.stop()

    def data_received(self, data):
        # print("D RECEIVED")
        distances_dict, frameNr = self.decoder.decode(data)
        self.distances_dict = distances_dict
        self.data_available = True
        self.frameNr = frameNr

    def read_data(self):
        if self.data_available:
            # print("DATA AVAILABLE")
            self.data_available = False 
            return self.distances_dict, self.frameNr
        else:
            print("NOPE")
            return -1, -1

        self.data_available = False 
        return self.distances_dict, self.frameNr
