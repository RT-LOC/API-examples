"""
    RTLOC - Uart interface class

    interface.py

    (c) 2021-2022 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>
    Frederic Mes <fred@rtloc.com>

"""

import time
import threading
import parsers.uart.python.uart_api as uart_api
import serial
import sys 
sys.path.append('..')

from rtloc_manager.manager_api import ParserInterface, DistanceReport
import os

class UARTInterface(ParserInterface):
    def __init__(self, config):
        self.port = config["serial"]["port"]
        self._set_serial_port(self.port)
        # self.distances_dict = {}
        # self.data_available = False

        # device_id_set = False

    def read_data(self):
        """ Get distance data from an abstract interface.
        This function is assumed to be implemented as a blocking
        function call, until new data becomes available.

        Only returning new data will create some room for
        apps to act on the data and not putting too much
        pressure on the CPU.

        Returns:
            list: distance report list
        """
        while not self.data_available:
            time.sleep(0.1)
        self.data_available = False

        # distance_report = DistanceReport(self.device_id, self.distances_dict)
        # return [distance_report]
        return self.distances_dict

    def stop(self):
        """ Properly stop the interface
        """
        uart.stop_streaming_distances(port=self.port)

    def is_symmetrical(self):
        """ This interface is not symmetrical
        """
        return False


    """
    Serial utilies
    """
    def _create_serial_packet(self, byte_list):
        packet = bytearray()

        for byte in byte_list:
            packet.append(byte)

        return packet

    def _write_serial_packet(self,packet):
        # print(len(packet))
        self._ser.write(packet)

    def _read_serial_packet(self,nb_bytes):
        packet = self._ser.read(size=nb_bytes)
        # print(packet)
        return packet

    def _read_serial_waiting(self):
        waiting = int(self._ser.inWaiting())
        # print(waiting)
        return waiting

    def _set_serial_port(self,port):
        self._ser.port = port