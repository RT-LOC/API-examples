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
from decoder import Decoder
import sys

class ApiClient(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.decoder = Decoder()

    def connection_made(self, transport):
        print('Connection made')

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def datagram_received(self, data, addr):
        self.decoder.decode(data)

async def main():
    print("Starting UDP Client")
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ApiClient(loop),
        local_addr=(my_ip_addr, 13102))

    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()

my_ip_addr = str(sys.argv[1])
asyncio.run(main())