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

# TODO: performance timing & improvements
# TODO: implement external impulse, userdata
# TODO: improve data structure (use Data Classes)
# TODO: error handling

from struct import *
class Decoder():

    def decode(self, data):
        (delim, pkg_length, pkg_type) = unpack('HHB',data[0:5])
        # print(delim, pkg_length, type)

        i = 0
        if delim == 8995:
            i += 5
            print('\n\n')
            print('[RTLOC BINARY API]')
            
            if pkg_type is ord('D'):
                print(' > Data')
                (version, data_len, msg_id, frame_nr, frame_size, time_cnt) = unpack('<BBIIHB', data[i:i+13])
                # print(version, data_len, msg_id, frame_nr, frame_size)

                print(" >> version = " + str(version))
                if version is 3:
                    i = i+13
                else:
                    i = i+12

                print(" >> time_cnt = " + str(time_cnt))
                
                if(time_cnt > 0):
                    time_data = {}
                    for x in range(0, time_cnt):
                        time_data[x] = 0

                    for tt in range(0, time_cnt):
                        #(time_source_id, time_year, time_month, time_day, time_hour, time_minute, time_second, time_millisecond, time_flag, time_spare)
                        time_data[tt] = list(unpack('<HBBBBBBHBH', data[i:i+13]))
                        print(" >>> time: " + str(time_data[tt]))
                        i = i+13

                (tag_cnt) = unpack('<B', data[i:i+1])[0]
                print(" >> tag_cnt = " + str(tag_cnt))
                i = i+1

                if(tag_cnt > 0):

                    # Generate Tag Array
                    tag = {}
                    for x in range(0, tag_cnt):
                        tag[x] = 0

                    
                    # Loop over all tags
                    for t in range(0, tag_cnt):
                        print(" >> tag[" + str(t) + "]")
                        # tag_id, tag_offset, tag_size, tag_data, tag_quat, tag_raw_samples, tag_position, tag_userdata, tag_impulseresponse
                        (tag_id, tag_offset, tag_size) = unpack('<HHH', data[i:i+6])
                        tag_tmp = [tag_id, tag_offset, tag_size, 0, 0, 0, 0, 0, 0]
                        i = i+6
                        bytes_remaining = tag_size

                        while bytes_remaining > 0:
                            tag_type = unpack('<B', data[i:i+1])[0]
                            bytes_remaining -= 1
                            i = i + 1                      

                            if(tag_type is ord('D')):
                                print(" >>> distances")
                                anchor_cnt = unpack('<B', data[i:i+1])[0]
                                i += 1                      
                                bytes_remaining -= 1

                                if(anchor_cnt > 0):
                                    print(" >>>> anchor_cnt = " + str(anchor_cnt))
                                    # Generate Anchor Array
                                    anchor = {}
                                    for x in range(0, anchor_cnt):
                                        anchor[x] = 0

                                    # Loop over all anchors
                                    for x in range(0, anchor_cnt):
                                        #anchor_id, anchor_dist, anchor_los1, anchor_rssi1, anchor_los2, anchor_rssi2, anchor_offset
                                        anchor[x] = list(unpack('<HHBBBBH', data[i:i+10]))
    
                                        # print(anchor_tmp)
                                        i = i+10
                                        bytes_remaining -= 10                                        

                                    # Add anchor array to tag_tmp array on tag_data element (3)
                                    tag_tmp[3] = anchor

                            elif tag_type is ord('Q'):
                                print(" >>> quaternions ")
                                tag_tmp[4] = list(unpack('<ffff', data[i:i+16]))

                                # print(tag_tmp[4])
                                i = i + 16
                                bytes_remaining -= 16
                            elif tag_type is ord('R'):
                                print(" >>> raw data ")
                                raw_sample_cnt = unpack('<B', data[i:i+1])[0]
                                i = i + 1                      
                                bytes_remaining -= 1

                                # Generate Samples Array
                                raw_samples = {}
                                for x in range(0, raw_sample_cnt):
                                    raw_samples[x] = 0

                                print(" >>>> sample_cnt = " + str(raw_sample_cnt))
                                if(raw_sample_cnt > 0):
                                    #ts, ax, ay, az, gx, gy, gz, mx, my, mz
                                    for z in range(0, raw_sample_cnt):
                                        raw_samples[z] = list(unpack('<Hhhhhhhhhh', data[i:i+20]))
                                        i = i + 20                      
                                        bytes_remaining -= 20

                                # Add quat array to tag_tmp array on tag_quat element (4)
                                tag_tmp[5] = raw_samples
                                # print(tag_tmp[5])

                            elif tag_type is ord('P'):
                                print(" >>> positions ")
                                tag_tmp[6] = list(unpack('<iii', data[i:i+12]))

                                i += 12
                                bytes_remaining -= 12
                                # print(" >>>> pos = [" + str(tag_tmp[6][0]) + ", " + str(tag_tmp[6][1]) + ", " + str(tag_tmp[6][2]) + "]")
                            
                            elif tag_type is ord('U'):
                                #TODO: implement userdata parsing
                                print(" >>> userdata: ")
                                userdata_cnt = unpack('<B', data[i:i+1])[0]
                                i += 1
                                bytes_remaining -= 1
                                print(" >>>> Userdata cnt: " + str(userdata_cnt))
                                i += userdata_cnt
                                bytes_remaining -= userdata_cnt
                                # tag_tmp[7] = userdata

                            elif tag_type is ord('I'):
                                # TODO - add parsing of impulse response
                                print(" >>> impulse response")
                                print(" >>>> ERR - implement IR first ")
                                # tag_tmp[8] = impulse_response
                                exit()

                        tag[t] = tag_tmp            
                        print(tag[t])
                        print("\n")

                print("\n")

            elif pkg_type is ord('A'):
                print(' > Anchorlist')
                #NOTE: 24/01/2019 - version of this API updated to ver=1. Use cxRTLS40039 to use the following line, otherwise stick to version 0 (whicch doesn't have anchor_cnt)
                (version, block_length, anchor_cnt) = unpack('<BBH', data[i:i+4])
                i += 4

                print(' >> anchor_cnt = ' + str(anchor_cnt))
                # Anchorlist Array
                anchorlist = {}
                for x in range(0, anchor_cnt):
                    anchorlist[x] = 0

                for t in range(0, anchor_cnt):
                    #id, x-coord, y-coord, z-coord
                    anchorlist[t] = list(unpack('<Hhhh', data[i:i+8]))
                    i += 8

                print(anchorlist)

            elif pkg_type is ord('T'):
                print(' > Taglist')
                #NOTE: 24/01/2019 - version of this API updated to ver=1. Use cxRTLS40039 to use the following line, otherwise stick to version 0 (whicch doesn't have tag_cnt)
                (version, block_length, tag_cnt) = unpack('<BBH', data[i:i+4])
                i += 4

                print(' >> tag_cnt = ' + str(tag_cnt))
                # Taglist Array
                taglist = {}
                for x in range(0, tag_cnt):
                    taglist[x] = 0

                for t in range(0, tag_cnt):
                    #id, x-coord, y-coord, z-coord
                    taglist[t] = list(unpack('<HBh', data[i:i+5]))
                    i += 5

                print(taglist)


            elif pkg_type is ord('X'):
                print(' > Node Status')
                (version, block_length, node_cnt) = unpack('<BBH', data[i:i+4])
                i += 4
                # Node Array
                node_stat = {}

                print(" >> version = " + str(version))
                print(" >> block_length = " + str(block_length))
                print(" >> node_cnt = " + str(node_cnt))

                for x in range(0, node_cnt):
                    node_stat[x] = 0
                
                    #node_id, node_kind, frame_off_micro, uptime, reset_reason, config_ver, tagspeed_ver, ant_dly, last_seen
                    #  last_userdata, voltage, hw_number, loader_ver, loader_crc, anchor_ver, anchor_crc, tag_ver, tag_crc, tag_subver, deca64
                    node_stat[x] = list(unpack('<HBHIBHHHIIHBHHHHHHBQ', data[i:i+48]))

                print(node_stat)

            else:
                print('Unknown message type')