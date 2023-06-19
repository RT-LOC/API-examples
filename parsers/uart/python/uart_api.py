"""
    RTLOC

    rtloc_uart/uart.py

    (c) 2020-2022 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>
    Frederic Mes <fred@rtloc.com>

"""

from dataclasses import dataclass
import time
from struct import *
import sys
import os
sys.path.append('..')


import threading
import serial

import parsers.uart.python.COMMANDS as c
from parsers.uart.python.interface import UARTInterface

_DEFAULT_UART_DEV = "COM3"
# _DEFAULT_UART_DEV = "/dev/ttyACM0"

class UART(UARTInterface):
    def __init__(self, config):
        self.port = config["serial_port"]

        self.distances_dict = {}
        self.data_available = False

        device_id_set = False

        self.start_distances = 0
        self.stop_distances = 0
        self.get_properties = 0
        self.firmware_init = 0
        self.firmware_req = -1
        self.firmwareObj = None
        """
        Initialize serial device
        """
        self._ser = serial.Serial('COM5', baudrate=115200,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=2)

        threading.Thread(target=self.parse_thread,
                         args=(self.rtloc_uart_callback,), kwargs={"port": self.port},
                         daemon=True)\
                             .start()

    def rtloc_uart_callback(self, distances_dict):
        self.distances_dict = distances_dict
        self.data_available = True


    """
    Command functions
    """
    def parse_thread(self, callback, port=_DEFAULT_UART_DEV):
        """ Start streaming distances over uart.

        This function can be terminated by calling  the stop_streaming_distances function.

        Parameters:
        callback (function) : callback function that take a distances (in cm) dictionary of the form
                            {address_one: distance_one, ..., address_N: distance_N} as its sole argument
        port (str) : serial device/port from which to stream the distances (default: /dev/ttyACM0)

        """
        self._set_serial_port(port)

        # Open port if not already open
        # _ser.open()
        
        # initiate the streaming
        len = 7
        version = 1

        commands = self._create_header(c._SD_UART_CMD_GET_PROPS, 7, 1)

        print(commands)
        # _write_serial_packet((commands))
        time.sleep(1)

        # process received data
        while 1:
            # Send data out if there is any
            # print("[OUT]")
            self.uart_out()
            time.sleep(0.1)
            # print("[OUT DONE]")

            # print("[IN]")
            # Parse incoming data
            self.uart_in()
            # print("[IN DONE]")

            time.sleep(0.1)

    def uart_out(self):
        if self.get_properties == 1:
            self.get_properties = 0
            commands = self._create_header(c._SD_UART_CMD_GET_PROPS, 7, 1)
            self._write_serial_packet((commands))

        if self.start_distances == 1:
            self.start_distances = 0
            commands = self._create_header(c._SD_UART_CMD_START_STREAMING, 7, 1)
            self._write_serial_packet((commands))

        if self.stop_distances == 1:
            self.stop_distances = 0
            commands = self._create_header(c._SD_UART_CMD_STOP_STREAMING, 7, 1)
            self._write_serial_packet((commands))

        if self.firmware_init == 1:
            self.firmwareObj.fw_update_init(c.TARGET_ADHOC, self._write_serial_packet)
            self.firmware_init = 0

        elif self.firmware_req != 0:
            self.firmwareObj.firmware_update(c.TARGET_ADHOC, self._write_serial_packet, self.firmware_req)
            self.firmware_req = 0

    def uart_in(self):
        waiting = self._read_serial_waiting()
        # print(print("WAITING:" + str(waiting)))
        #Read header
        if(waiting >= 6):
            header = self._read_serial_packet(6)
        elif(waiting == 0):
            # print("Nope")
            return 0, -1
        else:
            print(" >> LENGTH ISSUE!")
            return -1, -1
        (preamble,length,command,version) = unpack("<HHBB", header)


        # print(">> PREAMBLE=" + str(preamble))
        # print(">> LEN = " + str(length))
        # print(">> CMD = " + str(command))
        # print(">> VER = " + str(version))

        # Check on Preamble
        if(preamble == 8995):
            #Check on length - read more if length doesn't match
            if(waiting != length):
                waiting2 = self._read_serial_waiting()
                if(waiting + waiting2 == length):
                    print(" All OK 2 - TODO - read more & proceed instead of return!!")
                    return None, None
                else:
                    print("RETURN?!")
                    return None, None
            else:
                if(waiting > 6):
                    payload = self._read_serial_packet(waiting - 6)

            if command == c._SD_UART_CMD_PROPS:
                print("Command == PROPS")
                if(length == 6 + 44):
                    (byte3, length2, uptime, antenna_delay_rx, antenna_delay_tx, reset_type, hw_version, config_ver, fasttag_ver, obsolete1_4b, fw_version, fw_crc,fw_version_sub, obsolete2_2b, obsolete3_2b, obsolete4_2b, uid_8b_1, uid_8b_2, obsolete5_2b, obsolete6_2b) = unpack("<BHIHHBBHHIHHBHHHIIHH", payload)
                    print(byte3)
                    print(length2)
                    print("ANT_DELAY_2")
                    print(antenna_delay_rx)

                    print(hw_version)
                    print(reset_type)
                    print(config_ver)

                    print(fasttag_ver)
                else:
                    print(" Issue with length of props!")
            elif command == c._SD_UART_CMD_CLEAR_CONFIG:
                print("Command == 50")

            elif command == c._SD_UART_CMD_DISTANCES:
                print("Command == 2")
                # print(len(payload))
                dist_header = payload[0:5]
                # print(len(dist_header))
                distances = payload[5:]
                if(length >= 6+5):
                    (nb_distances,frame) = unpack("<BI", dist_header)
                    # print("NB DISTANCES = " + str(nb_distances))
                    # print("FRAME = " + str(frame))

                    # distances = payload[5:]

                    if distances is not None:
                        # print(">> DECODE")
                        # print(distances)
                        distances = self._decode_distances(distances)
                        print(distances)
                        # Act on the received information here, because function does not return
                        # callback(distances)
                    else: 

                        print(">> NONE")


                    return 1, distances

            elif command == c._SD_UART_CMD_UPLOAD_ANCHOR_OUT:
                if(length == 6 + 15):
                    (target, part_req, fw_ver, hw_ver, status, obsolete1_4b, obsolete2_2b, obsolete3_1b, eoh) = unpack("<BHHBBIHBB", payload)
                    # print(target)
                    print("req: " + str(part_req))
                    # print(fw_ver)
                    # print(hw_ver)
                    # print(eoh)
                    self.firmware_req = part_req

                    return 2, part_req
        else:
            waiting = self._read_serial_waiting()
            distances = self._read_serial_packet(waiting)
            return None, None

    # Changed in V4 - added rssi
    @staticmethod
    def _decode_distances(distance_data):
        distance_data = list(distance_data)

        # compute number of distances from data
        nb_distances = int(len(distance_data) / 6)

        distance_dict = {}
        for idx in range(nb_distances):
            address = distance_data[6*idx]
            address = (distance_data[6*idx+1] << 8) + address

            distance = distance_data[6*idx+2]
            distance = (distance_data[6*idx+3] << 8) + distance

            rssi = distance_data[6*idx+4]
            rssi2 = distance_data[6*idx+5]

            # Take first bit of variable rssi
            los1 = rssi >> 6
            nlos1 = rssi >> 7
            rssi1 = rssi & 0b00111111
            
            # Take last 6 bits of variable rssi
            los2 = rssi2 >> 6
            nlos2 = rssi2 >> 7
            rssi2 = rssi2 & 0b00111111

            # print("RSSI = " + str(rssi))
            # print("RSSI2 = " + str(rssi2))

            distance_dict[address] = distance

        return distance_dict


    @staticmethod
    def _create_header(cmd, length, version):
        # ctx_cmd
        packet = bytearray("##", encoding="ascii")
        packet += int(6 + length).to_bytes(2, "little")     # length

        packet += cmd.to_bytes(1,"little") 
        packet += version.to_bytes(1,"little") 

        packet += bytearray("|", encoding="ascii")

        return packet