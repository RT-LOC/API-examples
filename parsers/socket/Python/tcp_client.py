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
#TODO: check for correct input parameter
#TODO: Help information


import asyncio
from parser.socket.Python.decoder import Decoder
import sys


class ApiClient(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.decoder = Decoder()
        self.msg_get_anchorlist = b'##\x06\x00A\x00'
        self.msg_get_taglist = b'##\x06\x00T\x00'


    def connection_made(self, transport):
        print('Connection made')
        self.transport = transport

        # Request Anchorlist
        self.transport.write(self.msg_get_anchorlist)

        # Request Taglist
        self.transport.write(self.msg_get_taglist)
        print(" SENT!")
    def data_received(self, data):
        print(" TCP DATA RECEIVED!!")
        self.decoder.decode(data)
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()



#TODO - uncomment when using only this file

# ip_addr_server = str(sys.argv[1])
# param_cnt = len(sys.argv)
# loop = asyncio.get_event_loop()
# #NOTE: use port 13100 to connect to LIVE server, use 13200 to connect to REPLAY server.
# coro = loop.create_connection(lambda: ApiClient(loop), ip_addr_server, 13200)
# loop.run_until_complete(coro)
# loop.run_forever()
# loop.close()