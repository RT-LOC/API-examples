using System;
using System.IO;

namespace CSharp
{
    public class DataDecoder : IDecoder
    {
        public DataDecoder()
        {
        }

        public void Decode(BinaryReader reader)
        {
            Console.WriteLine("> Data");
            var version = reader.ReadByte();
            var dataLen = reader.ReadByte();
            var msgId = reader.ReadUInt32();
            var frameNr = reader.ReadUInt32();
            var frameSize = reader.ReadUInt16();
            var timeCnt = reader.ReadByte();
            Console.WriteLine(
                ">> Version: {0} - Data Length: {1} - Message Id: {2} - Frame Number: {3} - Frame Size: {4}",
                version,
                dataLen,
                msgId,
                frameNr,
                frameSize
            );
            Console.WriteLine(">> Time Count: {0}", timeCnt);
            if (timeCnt > 0)
                reader = DecodeTime(reader, timeCnt);

            var tagCnt = reader.ReadByte();
            Console.WriteLine(">> Tag Count: {0}", tagCnt);
            if (tagCnt > 0)
                DecodeTags(reader, tagCnt);

            Console.WriteLine();
        }

        private BinaryReader DecodeTime(BinaryReader reader, byte timeCnt)
        {
            for (int i = 0; i < timeCnt; ++i)
            {
                var sourceId = reader.ReadUInt16();
                var year = reader.ReadByte();
                var month = reader.ReadByte();
                var day = reader.ReadByte();
                var hour = reader.ReadByte();
                var minute = reader.ReadByte();
                var second = reader.ReadByte();
                var millisecond = reader.ReadUInt16();
                var timeFlag = reader.ReadByte();
                var spare = reader.ReadUInt16();

                string timeOutput = @">>> Time {0} -
                Source Id: {1}
                {2}-{3}-{4}T{5}:{6}:{7}:{8}
                Time Flag: {9}
                Spare: {10}";
                Console.WriteLine(
                    timeOutput,
                    i,
                    sourceId,
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    second,
                    millisecond,
                    timeFlag,
                    spare
                );
            }
            return reader;
        }

        private void DecodeTags(BinaryReader reader, byte tagCnt)
        {
            for (int i = 0; i < tagCnt; ++i)
            {
                var tagId = reader.ReadUInt16();
                var tagOffset = reader.ReadUInt16();
                var tagSize = reader.ReadUInt16();
                var remainingBytes = tagSize;

                Console.WriteLine(
                    ">>> Tag {0} - Tag Id: {1} - Tag Size: {2}",
                    i,
                    tagId,
                    tagSize
                );
                while (remainingBytes > 0)
                {
                    var tagType = reader.ReadByte();
                    remainingBytes--;

                    switch (tagType)
                    {
                        case 68:
                            remainingBytes = DecodeTagDistance(reader, remainingBytes);
                            break;
                        case 81:
                            remainingBytes = DecodeQuaternions(reader, remainingBytes);
                            break;
                        case 82:
                            remainingBytes = DecodeRaw(reader, remainingBytes);
                            break;
                        case 80:
                            remainingBytes = DecodePosition(reader, remainingBytes);
                            break;
                        case 85:
                            remainingBytes = DecodeUserData(reader, remainingBytes);
                            break;
                        case 73:
                            remainingBytes = DecodeImpulseResponse(reader, remainingBytes);
                            break;
                    }
                }
            }
        }

        private ushort DecodeTagDistance(BinaryReader reader, ushort remainingBytes)
        {
            var anchorCnt = reader.ReadByte();
            Console.WriteLine(">>>> Anchor Count: {0}", anchorCnt);
            remainingBytes--;

            for (int i = 0; i < anchorCnt; ++i)
            {
                var anchorId = reader.ReadUInt16();
                var distance = reader.ReadUInt16();
                var los1 = reader.ReadByte();
                var rssi1 = reader.ReadByte();
                var los2 = reader.ReadByte();
                var rssi2 = reader.ReadByte();
                var anchorOffset = reader.ReadUInt16();

                string output = @">>>> Anchor {0} -
                Anchor Id: {1}
                Distance: {2}
                RSSI [{3} {4}|{5} {6}| {7}]";
                Console.WriteLine(output, i, anchorId, distance, los1, rssi1, los2, rssi2, anchorOffset);
                remainingBytes -= 10;
            }

            return remainingBytes;
        }

        private ushort DecodeQuaternions(BinaryReader reader, ushort remainingBytes)
        {
            var q0 = reader.ReadDecimal();
            var q1 = reader.ReadDecimal();
            var q2 = reader.ReadDecimal();
            var q3 = reader.ReadDecimal();

            Console.WriteLine(
                ">>>> Quaternions - [{}, {}, {}, {}]",
                q0,
                q1,
                q2,
                q3
            );
            return remainingBytes -= 16;
        }

        private ushort DecodeRaw(BinaryReader reader, ushort remainingBytes)
        {
            var sampleCnt = reader.ReadByte();
            Console.WriteLine(
                ">>>> Raw Sensor Data - Sample Count: {0}",
                sampleCnt
            );
            remainingBytes--;
            for (int i = 0; i < sampleCnt; ++i)
            {
                var ts = reader.ReadUInt16();
                var ax = reader.ReadUInt16();
                var ay = reader.ReadUInt16();
                var az = reader.ReadUInt16();

                var gx = reader.ReadUInt16();
                var gy = reader.ReadUInt16();
                var gz = reader.ReadUInt16();

                var mx = reader.ReadUInt16();
                var my = reader.ReadUInt16();
                var mz = reader.ReadUInt16();

                Console.WriteLine(
                    ">>>> Sample {0} - [{1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}]",
                    ts,
                    ax,
                    ay,
                    az,
                    gx,
                    gy,
                    gz,
                    mx,
                    my,
                    mz
                );

                remainingBytes -= 20;
            }

            return remainingBytes;
        }

        private ushort DecodePosition(BinaryReader reader, ushort remainingBytes)
        {
            var x = reader.ReadUInt32();
            var y = reader.ReadUInt32();
            var z = reader.ReadUInt32();

            Console.WriteLine(">>>> Position - [{0}, {1}, {2}]", x, y, z);

            return remainingBytes -= 12;
        }

        private ushort DecodeUserData(BinaryReader reader, ushort remainingBytes)
        {
            var count = reader.ReadByte();
            Console.WriteLine(">>>> User Data - Count: {0}", count);
            remainingBytes--;
            for (int i = 0; i < count; ++i)
            {
                Console.Write(" {0}", reader.ReadByte());
            }
            Console.WriteLine();
            return remainingBytes -= count;
        }

        private ushort DecodeImpulseResponse(BinaryReader reader, ushort remainingBytes)
        {
            /*var length = reader.ReadUInt16();
            var source = reader.ReadUInt16();
            var index = reader.ReadUInt16();
            var left = reader.ReadByte();
            var right = reader.ReadByte();*/
            Console.WriteLine(">>>> Impulse Response - Not Implemented Yet!");
            return 0;
        }
    }
}