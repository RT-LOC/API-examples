"""
    RTLOC - Manager Lib

    rtloc_manager/utils/firmware_update.py

    (c) 2021-2022 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>
    Frederic Mes <fred@rtloc.com>


"""

import time
import crc16
import math

from cx_packets import CXDWPacket
FW_CHUNK_SIZE = 32
binary_image = 0
nb_parts = 0
pad_len = 0
crc_tot = 0
task_count = 0
data = 0
packet = 0
class FirmwareUpdate:
    def __init__(self):
        self.binary_image = None
        self.part_nb = 0
        self.nb_parts = 0
        self.pad_len = 0
        self.task_count = 0
        self.crc_tot = 0
        self.requested = 0

    def fw_update_set_image(self, image):
        with open(image, "rb") as fh:
            self.binary_image = fh.read()

    def fw_update_init(self, target, fn):

        if self.binary_image != None:

            #NOTE - if you want to only send a part of the FW (for debugging purposes), reset binary_image here
            self.binary_image = self.binary_image[:int(124*FW_CHUNK_SIZE)]

            self.nb_parts = math.ceil(len(self.binary_image) / FW_CHUNK_SIZE)
            self.part_nb = 0

            pad_len = FW_CHUNK_SIZE - (len(self.binary_image) % FW_CHUNK_SIZE)
            if pad_len < FW_CHUNK_SIZE:
                self.binary_image += (b'\x00' * pad_len)

            print("[IMAGE SIZE INCLUDING PADDING] {}".format(len(self.binary_image)))

            self.crc_tot = crc16.crc16xmodem(self.binary_image, 0xFFFF)

            self.task_count = 0
            self.task_count += 1
        
            time.sleep(1)

            data = b'\x01'*64
            # print("TARGET = " + str(target))
            packet = self._create_fw_update_task_chunk(0, self.nb_parts, data, crc_tot, len(self.binary_image), target, task_count)

            # Send to UART
            fn((packet))
            time.sleep(1)
            print("Going to sleep for 10 sec")
            # time.sleep(5)

            self.requested = 1


    def firmware_update(self, target, fn, req):        
        self.requested = req

        if(self.requested > 0):
            print("[FW UPDATE] sending part {} of {}".format(self.part_nb, self.nb_parts))
            
            if self.part_nb == 0:
                req = 0
                data = b'\x00' * FW_CHUNK_SIZE
            else:
                data = self.binary_image[int((self.part_nb-1)*FW_CHUNK_SIZE):int((self.part_nb)*FW_CHUNK_SIZE)]

            if len(data) < FW_CHUNK_SIZE:
                data += (b'\x00' * (FW_CHUNK_SIZE - len(data)))

            # print(data)
            print("PART:")
            print(self.part_nb)
            print(req)
            # packet = self._create_fw_update_packet(part_nb, self.nb_parts, data, crc_tot, len(binary_image), target)
            packet = self._create_fw_update_task_chunk(self.part_nb, self.nb_parts, data, self.crc_tot, len(self.binary_image), target, self.task_count)
            packet += bytearray("|", encoding="ascii")
            # print(packet)
            fn((packet))

            self.part_nb += 1

            # if self.part_nb != req:
            #     print("DRAMA")
            #     self.part_nb = req
            if self.part_nb > self.nb_parts:
                self.part_nb = 1
            
            self.requested = 0


        # else:
        #     print(" ISSUE WITH SELF REQUESTED")


    @staticmethod
    def _create_fw_update_packet(part_nb, nb_parts, data, crc_tot, size_tot, target):
        # ctx_cmd
        packet = bytearray("@CX@", encoding="ascii")
        packet += bytearray("ul", encoding="ascii")
        packet += int(9 + 19 + len(data)).to_bytes(2, "little")     # length
        packet += b'\x00'                                           # version

        # msg_file
        packet += target                                    # target
        packet += b'\x00\x00'                               # version
        packet += crc_tot.to_bytes(2, "little")             # crc_tot
        packet += int(size_tot).to_bytes(4, "little")       # size

        packet += part_nb.to_bytes(2, "little")
        packet += nb_parts.to_bytes(2, "little")
        packet += len(data).to_bytes(2, "little")
        packet += crc16.crc16xmodem(data, 0xFFFF).to_bytes(2, "little")

        packet += b'\x00'   # hw_version
        packet += b'\x00'   # desc_flag

        packet += data

        return packet

    @staticmethod
    def _create_fw_update_task_chunk(part_nb, nb_parts, data, crc_tot, size_tot, target, task_count):
        # ctx_cmd
        packet = bytearray("##", encoding="ascii")
        packet += int(9 + 7 + 1 + len(data)).to_bytes(2, "little")  # length
        packet += int(10).to_bytes(1, "little")                     # type\
        packet += b'\x00'                                           # version

        packet += int(6).to_bytes(1, "little")                      # target
        packet += int(100).to_bytes(2, "little")                    # version
        packet += crc_tot.to_bytes(2, "little")                     # crc_tot
        packet += int(size_tot).to_bytes(4, "little")               # size
        packet += part_nb.to_bytes(2, "little")
        packet += nb_parts.to_bytes(2, "little")
        packet += len(data).to_bytes(2, "little")
        packet += crc16.crc16xmodem(data, 0xFFFF).to_bytes(2, "little")

        packet += b'\x00'   # hw_version
        packet += b'\x00'   # desc_flag

        # print(" DATA: ")
        # print(data)

        if(part_nb != 0):
            packet += data
        else:
            print(" PART 0!!!!!")

        packet += bytearray("|", encoding="ascii")


        return packet
