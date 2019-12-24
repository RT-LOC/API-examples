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

import json

from struct import *
class Decoder():

    def decode(self, data):
        print('[RTLOC JSON API]')

        parsed_json = (json.loads(data.payload))

        frames = parsed_json['frames']

        #Frame size and delay are buffering parameters
        framesz = parsed_json['framesz']
        delay = parsed_json['delay']

        length = len(frames)

        # Loop over all frames within buffer
        for x in range(0, length):
            frame_nr = frames[x]['frameNr']
            tags_cnt = len(frames[x]['tags'])
            print(" > frame = " + str(frame_nr))
            # Init tag array
            tag = {}
            for x in range(0, tags_cnt):
                tag[x] = 0

            tag_cnt = 0
            
            # Loop over all tags
            for (k, v) in frames[x]['tags'].items():
                tag_id = k
                print(" >> tag[" + str(tag_id) + "]")
                tag_offset = v['offset']
                
                #[tag_id, tag_offset, tag_size, tag_data, tag_quat, tag_raw_samples, tag_position, tag_userdata, tag_impulseresponse]
                tag_tmp = [tag_id, tag_offset, 0, 0, 0, 0, 0, 0, 0]
                
                # Set anchor array
                #[anchor_id, anchor_dist, anchor_los1, anchor_rssi1, anchor_los2, anchor_rssi2, anchor_offset]
                anchor = {}
                a_cnt = 0

                # Loop over all anchors
                for(a,b) in v['data']['dist'].items():
                    anch = [8]
                    anch[0] = int(a)
                    anchor[a_cnt] = anch + b
                    a_cnt = a_cnt + 1
                # print(" >> anchor_cnt = " + str(a_cnt))
                tag_tmp[3] = anchor

                # Set tag position
                tag_tmp[6] = v['data']['pos']
                print(" >>> pos = [" + str(tag_tmp[6][0]) + ", " + str(tag_tmp[6][1]) + ", " + str(tag_tmp[6][2]) + "]")

                tag[tag_cnt] = tag_tmp
                tag_cnt = tag_cnt + 1

            print(frame_nr)
            print(" >> tag_cnt = " + str(tag_cnt))
            print("\n")
        print("\n\n")