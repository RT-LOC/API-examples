"""
    RTLOC - Integrated example of reading and printing the distances

    main.py

    (c) 2021-2022 RTLOC/Callitrix NV. All rights reserved.

    Frederic Mes   <fred@rtloc.com>

"""
import sys
sys.path.insert(1, '../../..')

import asyncio

import parsers.socket.Python.udp_client
import parsers.socket.Python.decoder
 
udpclient = 0
alist  = 0
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


async def main():
    # Get the running loop
    loop = asyncio.get_running_loop()

    #Create the UDP client
    udpClient = parsers.socket.Python.udp_client.UDPClient(asyncio.get_running_loop())
    
    print("[UDP] - connecting to (" + ip_addr_server + ") on port " + port)

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=(ip_addr_server, port))

    while(1):
        # Read out the data
        data, frameNr = udpClient.read_data()
        if data != -1:
            # Generate anchor positions array and corresponding measurements array
            measurements=[]
            # clearConsole()
            print("fr = " + str(frameNr))
            for x in range(0,len(data)):
                print("> T " + str(data[x][0]) + ": [", end="")
                # Select anchors_data   
                anchors = data[x][3]
                
                # Within anchors_data -> #anchor_id, anchor_dist, anchor_los1, anchor_rssi1, anchor_los2, anchor_rssi2, anchor_offset
                for idx in anchors:
                    if idx != 0:
                        print(", ", end="")
                    measurements.append(anchors[idx][1])
                    anchor_id = anchors[idx][0]
                    print(str(anchor_id) + ":" + str(anchors[idx][1]), end="")

                print("]")
            # print(measurements)
        await asyncio.sleep(0.01)

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

    print(ip_addr_server)

    print("[UDP] - going to start UDP loop")
    asyncio.run(main())