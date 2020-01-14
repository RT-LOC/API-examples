/*
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
 */

#define PORT 13100    /* the port client will be connecting to */

#define MAXDATASIZE 1024*8 /* max number of bytes we can get at once */

#define HDR_HASH 0x2323

#define CMD_TAGSPEED 		'S'
#define CMD_DATA 		      'D'
#define CMD_TOTAGRAW 		'U'
#define CMD_GETTAGLIST 		'T'
#define CMD_TAGLIST 		'T'
#define CMD_GETANCHORLIST 	'A'
#define CMD_ANCHORLIST 		'A'
#define CMD_NODESTATUS 		'X'

#define DATA_TYPE_DISTANCES    'D'
#define DATA_TYPE_QUATERNIONS  'Q'
#define DATA_TYPE_RAW_SENSOR   'R'
#define DATA_TYPE_POSITIONS    'P'
#define DATA_TYPE_USERDATA     'U'
#define DATA_TYPE_IMPULSERESP  'I'

/* Time Struct (part of Data Struct) */
struct data_time {
      uint16_t sourceId;
      uint8_t year;
      uint8_t month;
      uint8_t day;
      uint8_t hour;
      uint8_t minute;
      uint8_t second;
      uint16_t millisecond;
      uint8_t timeFlag;
      uint16_t spare;
} __attribute__((__packed__));
typedef struct data_time data_time_t;

struct data_time_list {
      data_time_t date[10];
} __attribute__((__packed__));
typedef struct data_time_list data_time_list_t;


/* Position Struct */
struct position {
      uint8_t type;
      int32_t coord_x;
      int32_t coord_y;
      int32_t coord_z;
} __attribute__((__packed__));
typedef struct position position_t;

/* Quaternion Struct */
struct quat {
      uint8_t type;
      float q0;
      float q1;
      float q2;
      float q3;
} __attribute__((__packed__));
typedef struct quat quat_t;

/* Raw Sensor Struct */
struct raw_sensor_sample {
      uint16_t ts;
      int16_t ax;
      int16_t ay;
      int16_t az;
      int16_t gx;
      int16_t gy;
      int16_t gz;
      int16_t mx;
      int16_t my;
      int16_t mz;                        
} __attribute__((__packed__));
typedef struct raw_sensor_sample raw_sensor_sample_t;

struct raw_sensor {
      uint8_t type;
      uint8_t sample_cnt;
      raw_sensor_sample_t sample[30];
} __attribute__((__packed__));
typedef struct raw_sensor raw_sensor_t;

/* Time Struct (part of Data Struct) */
struct userdata {
      uint8_t type;
      uint16_t count;
      uint8_t payload[200];
} __attribute__((__packed__));
typedef struct userdata userdata_t;

struct data_dist_anchor {
      uint16_t id;
      uint16_t dist;
      uint8_t LOS1;
      uint8_t RSSI1;
      uint8_t LOS2;
      uint8_t RSSI2;
      uint16_t anchor_offset;
} __attribute__((__packed__));
typedef struct data_dist_anchor data_dist_anchor_t;

struct data_dist {
      uint8_t type;
      uint8_t anchorCnt;
      union{
            /* Pointers NOT necessary because length of 1 anchor is not always the same.*/
            data_dist_anchor_t anchor[100];
            uint8_t payload[700];
      }anchors;
} __attribute__((__packed__));
typedef struct data_dist data_dist_t;

struct data_tag {
      uint16_t id;
      uint16_t offset;
      uint16_t size;

      //NOTE:fm - onderstaande moet nog weg!!
      union{
            data_dist_t dist;
            uint8_t payload[700];
      }subtype;

      data_dist_t *dist;
      position_t *pos;
      userdata_t *userdata;
      quat_t *quat;
      raw_sensor_t *raw_sensor;
} __attribute__((__packed__));
typedef struct data_tag data_tag_t;


/* Data Struct */
struct data_hdr {
      uint8_t length;
      uint32_t msg_id;
      uint32_t frame_nr;
      uint16_t frame_size;
      uint8_t timeCnt;
      // data_time_t time[6]; /* Note: by default only 0 or 1 time is given. Max is 6. */
      data_time_list_t *time_list; /* Note: by default only 0 or 1 time is given. Max is 6. */
      uint8_t tag_cnt;
      /* List of pointers to tags. Pointers necessary because length of 1 tag is not always the same.*/
      data_tag_t *tag[200];
} __attribute__((__packed__));
typedef struct data_hdr data_hdr_t;

/* Anchorlist */
struct anchor {
      uint16_t id;
      int16_t x_coord;
      int16_t y_coord;
      int16_t z_coord;
} __attribute__((__packed__));
typedef struct anchor anchor_t;

struct anchor_list {
      /* Temporary commented due to bug */
      // uint16_t anchor_cnt;
      anchor_t anchor[100];
} __attribute__((__packed__));
typedef struct anchor_list anchor_list_t;

/* Taglist */
struct tag {
      uint16_t id;
      uint8_t speed;
      int16_t z_coord; 
} __attribute__((__packed__));
typedef struct tag tag_t;

struct tag_list {
      /* Temporary commented due to bug */
      // uint16_t tag_cnt;
      tag_t tag[300];
} __attribute__((__packed__));
typedef struct tag_list tag_list_t;

/* Node statistics */
struct node_stat {
      uint16_t nodeId;
      uint8_t nodeKind;
      uint16_t frameOffMicro;
      uint32_t uptime;
      uint8_t resetReason;
      uint16_t configVer;
      uint16_t tagspeedVer;
      uint16_t antDly;
      uint32_t lastSeen;
      uint32_t lastUserData;
      uint16_t voltage;
      uint8_t hwNumber;
      uint16_t loaderVer;
      uint16_t loaderCrc;
      uint16_t anchorVer;
      uint16_t anchorCrc;
      uint16_t tagVer;
      uint16_t tagCrc;
      uint8_t tagSubVer;
      uint64_t longId;
} __attribute__((__packed__));
typedef struct node_stat node_stat_t;

struct node_status_list{
      uint8_t blockLength;
      uint16_t nodeCnt;
      node_stat_t node[300];
} __attribute__((__packed__));
typedef struct node_status_list node_status_list_t;


/* Main Header Struct */
struct hdr {
      uint16_t hash;
      uint16_t length;
      uint8_t cmd;
      uint8_t cmd_ver;
	union{
            data_hdr_t data;
            tag_list_t taglist;
            anchor_list_t anchorlist;
            node_status_list_t nodelist;
            uint8_t payload[4096];
	}command;      
} __attribute__((__packed__));
typedef struct hdr hdr_t;

/* EOF */