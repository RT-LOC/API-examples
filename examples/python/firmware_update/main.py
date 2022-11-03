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

import parsers.uart.python.uart_api as uart_api
from parsers.uart.python.fwup import FirmwareUpdate


if __name__ == "__main__":
    # Load configuration file
    config={}
    with open("config.yml") as yaml_fh:
                config = yaml.safe_load(yaml_fh)
    print(config)

    # Create a UART interface object.
    # This will create a thread that will constantly read out the UART data whenever it is available
    uart = uart_api.UART(config)
    
    # Create FirmwareUpdate object
    firmware_update = FirmwareUpdate()

    # Set firmware object. Needs to be known in uart object.    
    uart.firmwareObj = firmware_update

    # Set firmware image
    dirname = os.path.dirname(__file__)
    image = os.path.join(dirname, "fw_3_60_1_frdm.bin")
    firmware_update.fw_update_set_image(image)

    # Set firmware_init variable. This starts the firmware.
    uart.firmware_init = 1

    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break