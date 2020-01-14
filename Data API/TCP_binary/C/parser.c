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


/**
 * Incoming data is copied to a dedicated buffer. While being parsed, a structure with pointers is being made
 *  so that after parsing these pointers point to the expected places in the buffer.
 */
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h>
#include <sys/socket.h> 
#include <netinet/tcp.h>
#include <string.h> 
#include <netdb.h> 
#include <fcntl.h>

#include "parser.h"

#define DEBUG 0
#define PRINT_DBG(format, arg...)  do {} while (0)	
#define PRINT_DBG2(format, arg...)  do {} while (0)	
#define PRINT_DBG3(format, arg...)  do {} while (0)	
#define PRINT_DBG4(format, arg...)  do {} while (0)

#if defined(DEBUG) && (DEBUG >= 1)
	#define PRINT_DBG	printf
#if defined(DEBUG) && (DEBUG >= 2)
	#define PRINT_DBG2	printf
	#if defined(DEBUG) && (DEBUG >= 3)
	#define PRINT_DBG3	printf
	#endif
#endif
#endif

uint8_t parse_buf(uint8_t *buf2, int bufsize)
{
	/* Copy enet receive buffer to local buffer to prevent that parsed buffer is overwritten while being parsed. */
	uint8_t buf[MAXDATASIZE];
	memcpy(&buf[0], buf2, bufsize);

	/* Declaration of variables */
	hdr_t *hdr;
	data_hdr_t *data_hdr;
	data_tag_t *data_tag;
	data_dist_anchor_t *data_anchor;

	anchor_list_t *anchor_list;
	anchor_t *anchor;
	tag_list_t *tag_list;
	tag_t *tag;
	node_status_list_t *node_status_list;
	node_stat_t *node_stat;
	
	data_hdr_t data_all;
	uint8_t tag_type;
	uint16_t payload_offset;
	int i, j, k;

	int bytesparsed = 0;
	hdr = (hdr_t *)(buf);
	
	/* Print */
	printf("\r\n[RTLOC BINARY API]\r\n");
	printf(" > hash=%x, len=%u, cmd=%u, cmd_ver=%u\r\n", hdr->hash, hdr->length, hdr->cmd, hdr->cmd_ver);
	
	//NOTE: it could be that multiple 'protocols' are within 1 TCP frame. 
	/* if (hdr->length + 10 < bufsize)
	{
		//handle this situation
	}*/

	uint16_t byte_cnt = 0;
	uint16_t bytes_remaining = 0;
	uint16_t bytes_remaining_loop = 0;

	/* Loop over the incoming TCP frame */
	//NOTE: it could be that multiple 'protocols' are within 1 TCP frame, hence the looping. 
	while((bytesparsed + 8) < bufsize && (bytesparsed + 8) < MAXDATASIZE)
	{
		/* Check if preamble is ok */
		if(hdr->hash == HDR_HASH)
		{
			/* Check for command */
			switch(hdr->cmd)
			{
				case CMD_DATA:
					PRINT_DBG(" > Data\r\n");
					/* Set data header pointer */
					data_hdr = (data_hdr_t *)(&hdr->command.payload[0]);

					/* Copy all bytes up to timeCnt */
					memcpy(&data_all, data_hdr, 12);

					PRINT_DBG2(" >> len=%u, msg_id=%u, framenr=%u\r\n", data_all.length, 
							data_all.msg_id, data_all.frame_nr);
					

					/* Set tag_cnt */
					/* NOTE: data_all.tag_cnt is always the last byte of the dataheader. */
					/* NOTE: dataheader itself could vary depending on the version & timeCnt */
					data_all.tag_cnt = hdr->command.payload[data_hdr->length];
					
					PRINT_DBG2("%u - %u %u %u %u\r\n", data_all.tag_cnt, hdr->command.payload[hdr->command.data.length-2],
							hdr->command.payload[hdr->command.data.length-1],
							hdr->command.payload[hdr->command.data.length],
							hdr->command.payload[hdr->command.data.length+1] );
					
					/* Check for version and act on it if necessary */
					if(hdr->cmd_ver == 2)
					{}
					else
					{}

		
					/* Set pointer to time list */
					data_all.time_list = (data_time_list_t *)((&hdr->command.data.timeCnt) + 1);

					/* Time details */
					if(data_all.timeCnt > 0)
					{
						PRINT_DBG(" >> time_cnt = %u\r\n", data_all.timeCnt);
						for(int i = 0; i<data_all.timeCnt; i++)
						{
							PRINT_DBG(" >>> time(%u) = %uh %um %us\r\n", i, data_all.time_list->date[i].hour, data_all.time_list->date[i].minute, data_all.time_list->date[i].second);
						}
					}	

					PRINT_DBG(" >> tag_cnt = %u\r\n", data_all.tag_cnt);
					if(data_all.tag_cnt > 0)
					{
						/* Set pointer data_tag to first tag */
						bytes_remaining_loop = data_hdr->length + 1;
						data_all.tag[0] = (data_tag_t *)((&hdr->command.payload[bytes_remaining_loop]));
						
						/* Loop over all tags */
						for(i=0; i<data_all.tag_cnt;i++)
						{
							/* Set pointer data_tag to current tag */
							data_tag = (data_tag_t *)(data_all.tag[i]);

							/* Set pointer to next tag */
							bytes_remaining_loop += data_tag->size + 6;
							if(i<data_all.tag_cnt-1)
								data_all.tag[i+1] = (data_tag_t *)((&hdr->command.payload[bytes_remaining_loop]));

							PRINT_DBG(">>> tagid (%u << %u) = %u, size=%u\r\n", i, data_all.tag_cnt, data_tag->id, data_tag->size);

							payload_offset = 0;
							bytes_remaining = data_tag->size;

							/* Keep looping until all subpackages have been handled. */
							while(bytes_remaining > 0)
							{
								/* Set tag_type */
								tag_type = data_tag->subtype.payload[payload_offset];

								bytes_remaining -= 1;
								payload_offset += 1;

								switch(tag_type)
								{
									case DATA_TYPE_DISTANCES:
										data_tag->dist = (data_dist_t *)(&data_tag->subtype.payload[payload_offset-1]);
										PRINT_DBG(" >>> distances\r\n", data_tag->dist->anchorCnt);

										bytes_remaining -= 1;
										payload_offset += 1;

										/* Set pointer data_tag to first anchor */
										if(data_tag->dist->anchorCnt > 0)
										{
											PRINT_DBG(" >>>> anchor_cnt = %u\r\n", data_tag->dist->anchorCnt);

											/* Loop over all anchors */
											for(int j=0; j<data_tag->dist->anchorCnt; j++)
											{
												data_anchor = &data_tag->dist->anchors.anchor[j];

												PRINT_DBG("% >>>>> %u) id=%u, dist=%u rssi=[%u %u|%u %u| %u]\r\n",
															j, data_anchor->id, data_anchor->dist, 
															data_anchor->LOS1, data_anchor->RSSI1,
															data_anchor->LOS2, data_anchor->RSSI2,
															data_anchor->anchor_offset );

												bytes_remaining -= 10;	
												payload_offset += 10;	
											}
										}
										PRINT_DBG(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
									break;
									case DATA_TYPE_QUATERNIONS:
										PRINT_DBG(" >>> quaternions \r\n");
										/* Set quaternion pointer */
										data_tag->quat = (quat_t *)(&data_tag->subtype.payload[payload_offset-1]);
										PRINT_DBG(" >>>> quat = [%f, %f, %f, %f]\r\n", data_tag->quat->q0, data_tag->quat->q1, data_tag->quat->q2, data_tag->quat->q3);

										bytes_remaining -= 16;
										payload_offset += 16;

										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
										
									break;
									case DATA_TYPE_RAW_SENSOR:
										PRINT_DBG(" >>> raw sensor data\r\n");
										data_tag->raw_sensor = (raw_sensor_t *)(&data_tag->subtype.payload[payload_offset-1]);
										bytes_remaining -= 1;
										payload_offset += 1;

										PRINT_DBG(" >>>> sample_cnt = %u \r\n", data_tag->raw_sensor->sample_cnt);
										for(int k = 0; k<data_tag->raw_sensor->sample_cnt; k++)
										{
											PRINT_DBG(">>>>> %u) = [%i, %i, %i, %i, %i, %i, %i, %i, %i] \r\n", k, data_tag->raw_sensor->sample[k].ax, data_tag->raw_sensor->sample[k].ay, data_tag->raw_sensor->sample[k].az,
											data_tag->raw_sensor->sample[k].gx, data_tag->raw_sensor->sample[k].gy, data_tag->raw_sensor->sample[k].gz,
											data_tag->raw_sensor->sample[k].mx, data_tag->raw_sensor->sample[k].my, data_tag->raw_sensor->sample[k].mz);
											
											bytes_remaining -= 20;
											payload_offset += 20;
										}
										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
									break;
									case DATA_TYPE_POSITIONS:
										PRINT_DBG(" >>> positions\r\n");
										data_tag->pos = (position_t *)(&data_tag->subtype.payload[payload_offset-1]);

										PRINT_DBG(" >>>> pos = [%i, %i, %i]\r\n", data_tag->pos->coord_x, data_tag->pos->coord_y, data_tag->pos->coord_z);
										bytes_remaining -= 12;
										payload_offset += 12;	
										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
									break;
									case DATA_TYPE_USERDATA:
										PRINT_DBG(" >>>  userdata:\r\n");
										data_tag->userdata = (userdata_t *)(&data_tag->subtype.payload[payload_offset-1]);
										PRINT_DBG(" >>>> userdata cnt: %u\r\n", data_tag->userdata->count);

										payload_offset += 2;
										bytes_remaining -= 2;
										payload_offset += data_tag->userdata->count;
										bytes_remaining -= data_tag->userdata->count;

										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
									break;
									case DATA_TYPE_IMPULSERESP:
										PRINT_DBG(" >>>>>>>>>>>>   I\r\n");
										bytes_remaining = 0;
										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
									break;
									default:
										PRINT_DBG(" >>> [ERR] - unknown type\r\n");									
										PRINT_DBG2(" >>>>>> remaining_bytes =  %u\r\n", bytes_remaining);
										bytes_remaining = 0;
									break;
								}
							}
							PRINT_DBG("\r\n");
						}	
					}
				break;

				case CMD_TAGLIST:
					tag_list = (tag_list_t *)(&hdr->command.payload[0]);
					PRINT_DBG(" > Taglist\r\n");

					/* Temporary Workaround for bug (instead of via tag_list->tag_cnt) */
					uint16_t tag_cnt = ((hdr->length-6)/5);

					PRINT_DBG(" >> tag_cnt = %u\r\n", tag_cnt);
					// printf(" >> tag_cnt = %u\r\n", tag_list->tag_cnt);

					/* Loop over the anchors (demo)*/
					for(i = 0; i < tag_cnt; i++)
					{
						PRINT_DBG(" >>> tag_id = %u\r\n", tag_list->tag[i].id);
						PRINT_DBG(" >>> tag_speed = %u\r\n", tag_list->tag[i].speed);
						PRINT_DBG(" >>> tag_zcoord = %i\r\n", tag_list->tag[i].z_coord);
					}

				break;

				case CMD_ANCHORLIST:
					// anchor_list = (anchor_list_t *)(&hdr->command.payload[0]);
					PRINT_DBG(" > Anchorlist \r\n");

					/* Temporary Workaround for bug */
					uint16_t anchor_cnt = ((hdr->length-6)/8);

					PRINT_DBG(" >> anchor_cnt = %u\r\n", anchor_cnt);
					// PRINT_DBG(" >> anchor_cnt = %u\r\n", anchor_list->anchor_cnt);

					/* Loop over the anchors (demo)*/
					for(i = 0; i < anchor_cnt; i++)
					{
						PRINT_DBG(" >>> anchor_id = %u\r\n", hdr->command.anchorlist.anchor[i].id);
					}
				break;

				case CMD_TOTAGRAW:
					PRINT_DBG(" > To Tag Raw \r\n");
					//TODO: implement to tag raw
				break;

				case CMD_NODESTATUS:
					PRINT_DBG(" > Node Status\r\n");
					node_status_list = (node_status_list_t *)(&hdr->command.payload[0]);
					node_stat = (node_stat_t *)(&node_status_list->node[0]);

					PRINT_DBG(" >> version = %u\r\n", hdr->cmd_ver);
					PRINT_DBG(" >> block_length = %u\r\n", node_status_list->blockLength);
					PRINT_DBG(" >> node_cnt = %u\r\n", node_status_list->nodeCnt);

					/* Loop over the nodes (demo) */
					for(i = 0; i<node_status_list->nodeCnt; i++)
					{
						PRINT_DBG(" >>> node_id = %u\r\n", hdr->command.nodelist.node[i].nodeId);
					}
				break;
				default:
					PRINT_DBG(" > Unknown pkg type (%u) \r\n", hdr->cmd);
				break;
			}
		}


		//NOTE:fm - when traffic comes too fast, client seems to make a mistake and stays in infinite loop
		//because bytesparsed never grows anymore (hdr->length == 0)
		//TODO: fix
		if(hdr->length > 100)
		{
			bytesparsed += hdr->length;
		}else{
			bytesparsed += 10000;
		}
		PRINT_DBG3("[DBG3] bytes parsed = %i\r\n", bytesparsed);
		hdr = (hdr_t *)(&hdr->command.payload[hdr->length-6]);

	}
	PRINT_DBG3("Parsing finished \r\n");
	return 1;
}

int main(int argc, char *argv[])
{
	int sockfd, numbytes;  
	uint8_t buf[MAXDATASIZE];
	struct hostent *he;
	struct sockaddr_in their_addr; /* connector's address information */
	
	printf(" -- RTLOC C Parser -- \n\r");
	
	/* Check for arguments */
	if (argc != 2) 
	{
	    printf(" [USAGE] - ./parser ip_address_server\n");
	    exit(1);
	}
	/* Get the host info */
	if ((he=gethostbyname(argv[1])) == NULL) 
	{  
		printf(" > [ERR] - gethostbyname");
	    exit(1);
	}

	/* Init socket */
	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) 
	{
	    printf(" > [ERR] - socket issue");
	    exit(1);
	}

	their_addr.sin_family = AF_INET;      /* host byte order */
	their_addr.sin_port = htons(PORT);    /* short, network byte order */
	their_addr.sin_addr = *((struct in_addr *)he->h_addr);
	bzero(&(their_addr.sin_zero), 8);     /* zero the rest of the struct */

	if (connect(sockfd, (struct sockaddr *)&their_addr, sizeof(struct sockaddr)) == -1) 
	{
	    printf(" > [ERR] - cannot connect");
	    exit(1);
	}

	printf(" > Connected \r\n");

    int val = 1;
	/* Set socket options */
	if (setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &val, sizeof(val)) < 0)
	{
		printf(" > [ERR] - setsockopt error");
	}

	/* Start the while loop */
	while (1) 
	{
		int i;

		/* Receive data (blocking!!) */
		if ((numbytes=recv(sockfd, buf, MAXDATASIZE, 0)) == -1) 
		{
			PRINT_DBG3(" >> recv failed \n\r");
			//Receiving has failed
			//TODO: handle reception failure...
		}	
		buf[numbytes] = '\0';
		PRINT_DBG3("Received in pid=%d, bytes=%u, text=: %s \n\r", getpid(), numbytes, buf);

		/* Print all incoming bytes */
		PRINT_DBG4("[");
		for(i=0; i<numbytes; i++)
		{
			PRINT_DBG4("0x%02x ", buf[i]);
			PRINT_DBG4("%c ", buf[i]);
		}
		PRINT_DBG4("] \n\r");
		
		/* Parse the incoming buffer */
		if(numbytes < 10000)
		{
			parse_buf(buf, numbytes);
			PRINT_DBG("\r\n");
		}

		/* TODO: add sending commands */
	}

	/* Close socket */
	close(sockfd);
	return 0;
}
/* EOF */