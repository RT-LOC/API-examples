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
        (delim, package_length, type) = unpack('HHB',data[0:5])
        # print(delim, package_length, type)

        i = 0
        if delim == 8995:
            i += 5
            print('\n\n')
            print('[RTLOC BINARY API]')
            
            if type is ord('D'):
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
                        time_data_tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                        (time_data_tmp[0], time_data_tmp[1], time_data_tmp[2], time_data_tmp[3], time_data_tmp[4], time_data_tmp[5], time_data_tmp[6], time_data_tmp[7], time_data_tmp[8], time_data_tmp[9])  = unpack('<HBBBBBBHBH', data[i:i+13])
                        time_data[tt] = time_data_tmp
                        # print((time_source_id, time_year, time_month, time_day, time_hour, time_minute, time_second, time_millisecond, time_flag, time_spare))
                        print(" >>> time: " + str(time_data_tmp[0]))
                        i = i+13

                (tag_cnt) = unpack('<B', data[i:i+1])[0]
                print(" >> tag_cnt = " + str(tag_cnt))
                i = i+1

                print(" >> data_len = " + str(data_len))
                print("\n")
                if(tag_cnt > 0):

                    # Generate Tag Array
                    tag = {}
                    for x in range(0, tag_cnt):
                        tag[x] = 0

                    
                    for t in range(0, tag_cnt):
                        print(" >> tag[" + str(t) + "]")
                        # tag_id, tag_offset, tag_size, tag_data, tag_quat, tag_raw_samples, tag_position, tag_userdata, tag_impulseresponse
                        tag_tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        (tag_tmp[0], tag_tmp[1], tag_tmp[2]) = unpack('<HHH', data[i:i+6])
                        # print(tag_tmp[0], tag_tmp[1], tag_tmp[2])
                        i = i+6
                        bytes_remaining = tag_tmp[2]

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
                                        anchor_tmp = [0, 0, 0, 0, 0, 0, 0, 0]
                                        (anchor_tmp[0], anchor_tmp[1], anchor_tmp[2], anchor_tmp[3], anchor_tmp[4], anchor_tmp[5], anchor_tmp[6]) = unpack('<HHBBBBH', data[i:i+10])

                                        anchor[x] = anchor_tmp
                                        # print(anchor_tmp)
                                        i = i+10
                                        bytes_remaining -= 10                                        

                                    # Add anchor array to tag_tmp array on tag_data element (3)
                                    tag_tmp[3] = anchor

                            elif tag_type is ord('Q'):
                                print(" >>> quaternions ")
                                quat_tmp = [0, 0, 0, 0]
                                (quat_tmp[0], quat_tmp[1], quat_tmp[2], quat_tmp[3]) = unpack('<ffff', data[i:i+16])
                                # Add quat array to tag_tmp array on tag_quat element (4)
                                tag_tmp[4] = quat_tmp
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
                                    raw_samples_tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                                    for z in range(0, raw_sample_cnt):
                                        (raw_samples_tmp[0], raw_samples_tmp[1], raw_samples_tmp[2], raw_samples_tmp[3],
                                        raw_samples_tmp[4], raw_samples_tmp[5], raw_samples_tmp[6], raw_samples_tmp[7], 
                                        raw_samples_tmp[8], raw_samples_tmp[9])  = unpack('<Hhhhhhhhhh', data[i:i+20])
                                        raw_samples[z] = raw_samples_tmp

                                        i = i + 20                      
                                        bytes_remaining -= 20

                                # Add quat array to tag_tmp array on tag_quat element (4)
                                tag_tmp[5] = raw_samples_tmp
                                # print(tag_tmp[5])

                            elif tag_type is ord('P'):
                                print(" >>> positions ")
                                position_tmp = [0, 0, 0]
                                (position_tmp[0], position_tmp[1], position_tmp[2])  = unpack('<iii', data[i:i+12])
                                tag_tmp[6] = position_tmp
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

            elif type is ord('A'):
                print(' > Anchorlist')
                ########
                ## Note - there is a bug in the get_anchorlist API. The anchor_cnt is not included. Hence the following workaround.
                ## (version, anchor_cnt) = unpack('<BH', data[i:i+3])
                ## i += 3
                ######
                (version) = unpack('<B', data[i:i+1])[0]
                i += 1
                data_length = len(data)
                anchor_cnt =  round((data_length-6)/8)
                #######

                print(' >> anchor_cnt = ' + str(anchor_cnt))
                # Anchorlist Array
                anchorlist = {}
                for x in range(0, anchor_cnt):
                    anchorlist[x] = 0

                for t in range(0, anchor_cnt):
                    #id, x-coord, y-coord, z-coord
                    anchor_tmp = [0, 0, 0, 0]
                    (anchor_tmp[0], anchor_tmp[1], anchor_tmp[2], anchor_tmp[3]) = unpack('<Hhhh', data[i:i+8])
                    i += 8
                    anchorlist[t] = anchor_tmp

                print(anchorlist)

            elif type is ord('T'):
                print(' > Taglist')
                ########
                ## Note - there is a bug in the get_anchorlist API. The anchor_cnt is not included. Hence the following workaround.
                #(version, tag_cnt) = unpack('<BH', data[i:i+3])
                #i += 3
                ######
                (version) = unpack('<B', data[i:i+1])[0]
                i += 1
                data_length = len(data)
                tag_cnt =  round((data_length-6)/5)
                #######

                print(' >> tag_cnt = ' + str(tag_cnt))

                # Taglist Array
                taglist = {}
                for x in range(0, tag_cnt):
                    taglist[x] = 0

                for t in range(0, tag_cnt):
                    #id, x-coord, y-coord, z-coord
                    tag_tmp = [0, 0, 0]
                    (tag_tmp[0], tag_tmp[1], tag_tmp[2]) = unpack('<HBh', data[i:i+5])
                    i += 5
                    taglist[t] = tag_tmp

                print(taglist)


            elif type is ord('X'):
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
                    node_stat_tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     
                    (node_stat_tmp[0], node_stat_tmp[1], node_stat_tmp[2], node_stat_tmp[3], node_stat_tmp[4]) = unpack('<HBHIB', data[i:i+10])
                    i += 10

                    (node_stat_tmp[5], node_stat_tmp[6], node_stat_tmp[7], node_stat_tmp[8], node_stat_tmp[9]) = unpack('<HHHII', data[i:i+14])
                    i += 14

                    (node_stat_tmp[10], node_stat_tmp[11], node_stat_tmp[12], node_stat_tmp[13], node_stat_tmp[14]) = unpack('<HBHHH', data[i:i+9])
                    i += 9

                    (node_stat_tmp[15], node_stat_tmp[16], node_stat_tmp[17], node_stat_tmp[18], node_stat_tmp[19]) = unpack('<HHHBQ', data[i:i+15])
                    i += 15

                    node_stat[x] = node_stat_tmp

                print(node_stat)

            else:
                print('Unknown message type')