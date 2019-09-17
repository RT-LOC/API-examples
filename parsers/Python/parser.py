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
from struct import *

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print('Connection made')

    def data_received(self, data):
        (delim, type) = unpack('HB',data)
	    if delim == 8995:
		    print(unpack('HHB',data))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                              '192.168.1.7', 13100)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()