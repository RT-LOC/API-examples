"""
    RTLOC - Integrated example of using UDP read + feeding data to the engine

    main.py

    (c) 2021-2022 RTLOC/Callitrix NV. All rights reserved.

    Frederic Mes   <fred@rtloc.com>

"""
import asyncio

from engine import DebugPostionEngine, Position

import parsers.socket.Python.udp_client
import parsers.socket.Python.tcp_client
import parsers.socket.Python.decoder
 
udpclient = 0
async def main():
    # Get the running loop
    loop = asyncio.get_running_loop()

    #Create the UDP client
    udpClient = parsers.socket.Python.udp_client.UDPClient(asyncio.get_running_loop())
    
    # TODO - set own IP address here
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udpClient,
        local_addr=("192.168.1.66", 13102))

    
    # Create Position Dictionary
    position_dict = {}

    # Print the alist here
    # TODO - integrate TCP data properly
    alist = {0: [1, 1300, 1000, 0], 1: [119, 1000, 1269, 0], 2: [7904, 1000, 1000, 0]}
    for anchor in alist:
        try:
            x = alist[anchor][1]
            y = alist[anchor][2]
            z = alist[anchor][3]
            position_dict[alist[anchor][0]] =  Position(x,y,z)
        except (KeyError, TypeError):
            # anchor position not known
            pass

    #Create Engine Object
    anchor_set_size = 3
    engine = DebugPostionEngine(anchor_set_size)

    #Init the tag position
    new_tag_pos = Position(0, 0, 0)

    # tag_position = engine.compute_tag_position([0,0,0], tag_position)
    while(1):
        # Read out the data
        data, frameNr = udpClient.read_data()
        if data != -1:
            # print(data)
            
            # Generate anchor positions array and corresponding measurements array
            positions=[]
            measurements=[]

            # Select anchors_data   
            anchors = data[0][3]
            # print(anchors)

            # Within anchors_data -> #anchor_id, anchor_dist, anchor_los1, anchor_rssi1, anchor_los2, anchor_rssi2, anchor_offset
            for idx in anchors:
                measurements.append(anchors[idx][1])
                anchor_id = anchors[idx][0]
                positions.append(position_dict[anchor_id])

            # print(measurements)
            # print(positions)

            # Reset the anchor positions for the engine
            engine.set_anchor_positions(positions)

            # Calculate the new position
            new_tag_pos = engine.compute_tag_position(measurements, new_tag_pos)

            # Print the result
            print(str(frameNr) + ", " + str(new_tag_pos.x) + ", " + str(new_tag_pos.y))
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    ####################
    #       TCP        #
    ####################
    # #NOTE: uncommenting this will block the UDP part
    # loop = asyncio.get_event_loop()
    # tcpClient = Data_API.TCP_binary.Python.tcp_client.ApiClient(loop)
    # coro = loop.create_connection(lambda: Data_API.TCP_binary.Python.tcp_client.ApiClient(loop), "192.168.1.66", 13100)
    # loop.run_until_complete(coro)
    # loop.run_forever()


    ####################
    #       UDP        #
    ####################
    asyncio.run(main())