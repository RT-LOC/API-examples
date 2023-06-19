"""
    RTLOC - Integrated example of firmware update via UART

    main.py

    (c) 2022 RTLOC/Callitrix NV. All rights reserved.

    Frederic Mes   <fred@rtloc.com>

"""
import time
import yaml
import os
import sys
sys.path.insert(1, '../../..')

from engine import DebugPostionEngine, Position
import parsers.uart.python.uart_api as uart_api

if __name__ == "__main__":
    # Load configuration file
    config={}
    with open("config.yml") as yaml_fh:
                config = yaml.safe_load(yaml_fh)
    print(config)

    # Create a UART interface object.
    # This will create a thread that will constantly read out the UART data whenever it is available
    uart = uart_api.UART(config)
    
    # Set firmware image
    dirname = os.path.dirname(__file__)
    
    #Create Engine Object
    anchor_set_size = 3
    engine = DebugPostionEngine(anchor_set_size)

    #Get anchor positions and feed them to the engine
    positions = config["anchor_positions"]

    # Create Position Dictionary
    position_dict = {}
    for anchor in positions:
        try:
            x = positions[anchor][0]
            y = positions[anchor][1]
            z = positions[anchor][2]
            position_dict[anchor] =  Position(x,y,z)
        except (KeyError, TypeError):
            # anchor position not known
            pass

    #Init the tag position
    new_tag_pos = Position(0, 0, 0)

    # Set firmware_init variable. This starts the firmware.
    # uart.get_properties = 1
    uart.start_distances = 1
    while True:
        try:
            # Read the distances from the UART thread
            # distances = uart.read_data()
            distances = uart.distances_dict

            # check if distances is empty
            if not distances:
                continue
            else:
                print(distances)
                # Generate anchor positions array and corresponding measurements array
                positions=[]
                measurements=[]

                for idx in distances:
                    positions.append(position_dict[idx])
                    measurements.append(distances[idx])

                print(positions)
                print(measurements)

                # Reset the anchor positions for the engine
                engine.set_anchor_positions(positions)

                # Calculate the new position
                new_tag_pos = engine.compute_tag_position(measurements, new_tag_pos)
                print(new_tag_pos)

            time.sleep(0.01)
        except KeyboardInterrupt:
            break