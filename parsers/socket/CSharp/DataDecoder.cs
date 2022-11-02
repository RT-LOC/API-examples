using System;
using System.IO;

namespace CSharp
{
    public class DataDecoder : IDecoder
    {
        private readonly BinaryReader reader;
        private ushort remainingBytes;
        public DataDecoder(BinaryReader reader)
        {
            this.reader = reader;
        }

        public void Decode()
        {
            Console.WriteLine("> Data");
            var version = this.reader.ReadByte();
            var dataLen = this.reader.ReadByte();
            var msgId = this.reader.ReadUInt32();
            var frameNr = this.reader.ReadUInt32();
            var frameSize = this.reader.ReadUInt16();
            var timeCnt = this.reader.ReadByte();
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
                DecodeTime(timeCnt);

            var tagCnt = this.reader.ReadByte();
            Console.WriteLine(">> Tag Count: {0}", tagCnt);
            if (tagCnt > 0)
                DecodeTags(tagCnt);
        }

        private void DecodeTime(byte timeCnt)
        {
            for (int i = 0; i < timeCnt; ++i)
            {
                var sourceId = this.reader.ReadUInt16();
                var year = this.reader.ReadByte();
                var month = this.reader.ReadByte();
                var day = this.reader.ReadByte();
                var hour = this.reader.ReadByte();
                var minute = this.reader.ReadByte();
                var second = this.reader.ReadByte();
                var millisecond = this.reader.ReadUInt16();
                var timeFlag = this.reader.ReadByte();
                var spare = this.reader.ReadUInt16();

                string timeOutput = @">>> Time {0} -
                Source Id: {1}
                {2}-{3}-{4}T{5}:{6}:{7}:{8}
                Time Flag: {9}
                Spare: {10}";
                Console.WriteLine(
                    timeOutput,
                    i+1,
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
        }

        private  void DecodeTags(byte tagCnt)
        {
            for (int i = 0; i < tagCnt; ++i)
            {
                var tagId = this.reader.ReadUInt16();
                var tagOffset = this.reader.ReadUInt16();
                var tagSize = this.reader.ReadUInt16();
                this.remainingBytes = tagSize;

                Console.WriteLine(
                    ">>> Tag {0} - Tag Id: {1} - Tag Size: {2}",
                    i+1,
                    tagId,
                    tagSize
                );
                while (this.remainingBytes > 0)
                {
                    var tagType = this.reader.ReadByte();
                    this.remainingBytes--;

                    switch (tagType)
                    {
                        case 68:
                            DecodeTagDistance();
                            break;
                        case 81:
                            DecodeQuaternions();
                            break;
                        case 82:
                            DecodeRaw();
                            break;
                        case 80:
                            DecodePosition();
                            break;
                        case 85:
                            DecodeUserData();
                            break;
                        case 73:
                            DecodeImpulseResponse();
                            break;
                    }
                }
            }
        }

        private void DecodeTagDistance()
        {
            var anchorCnt = this.reader.ReadByte();
            Console.WriteLine(">>>> Anchor Count: {0}", anchorCnt);
            this.remainingBytes--;

            for (int i = 0; i < anchorCnt; ++i)
            {
                var anchorId = this.reader.ReadUInt16();
                var distance = this.reader.ReadUInt16();
                var los1 = this.reader.ReadByte();
                var rssi1 = this.reader.ReadByte();
                var los2 = this.reader.ReadByte();
                var rssi2 = this.reader.ReadByte();
                var anchorOffset = this.reader.ReadUInt16();

                string output = @">>>> Anchor {0} -
                Anchor Id: {1}
                Distance: {2}
                RSSI [{3} {4}|{5} {6}| {7}]";
                Console.WriteLine(
                    output,
                    i+1,
                    anchorId,
                    distance,
                    los1,
                    rssi1,
                    los2,
                    rssi2,
                    anchorOffset
                );
                this.remainingBytes -= 10;
            }
        }

        private void DecodeQuaternions()
        {
            var q0 = this.reader.ReadDecimal();
            var q1 = this.reader.ReadDecimal();
            var q2 = this.reader.ReadDecimal();
            var q3 = this.reader.ReadDecimal();

            Console.WriteLine(
                ">>>> Quaternions - [{}, {}, {}, {}]",
                q0,
                q1,
                q2,
                q3
            );
            this.remainingBytes -= 16;
        }

        private void DecodeRaw()
        {
            var sampleCnt = this.reader.ReadByte();
            Console.WriteLine(
                ">>>> Raw Sensor Data - Sample Count: {0}",
                sampleCnt
            );
            this.remainingBytes--;
            for (int i = 0; i < sampleCnt; ++i)
            {
                var ts = this.reader.ReadUInt16();
                var ax = this.reader.ReadUInt16();
                var ay = this.reader.ReadUInt16();
                var az = this.reader.ReadUInt16();

                var gx = this.reader.ReadUInt16();
                var gy = this.reader.ReadUInt16();
                var gz = this.reader.ReadUInt16();

                var mx = this.reader.ReadUInt16();
                var my = this.reader.ReadUInt16();
                var mz = this.reader.ReadUInt16();

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

                this.remainingBytes -= 20;
            }
        }

        private void DecodePosition()
        {
            var x = this.reader.ReadUInt32();
            var y = this.reader.ReadUInt32();
            var z = this.reader.ReadUInt32();

            Console.WriteLine(">>>> Position: [{0}, {1}, {2}]", x, y, z);

            this.remainingBytes -= 12;
        }

        private void DecodeUserData()
        {
            var count = this.reader.ReadByte();
            Console.WriteLine(">>>> User Data - Count: {0}", count);
            this.remainingBytes--;
            for (int i = 0; i < count; ++i)
            {
                Console.Write(" {0}", this.reader.ReadByte());
            }
            Console.WriteLine();
            this.remainingBytes -= count;
        }

        private void DecodeImpulseResponse()
        {
            /*var length = this.reader.ReadUInt16();
            var source = this.reader.ReadUInt16();
            var index = this.reader.ReadUInt16();
            var left = this.reader.ReadByte();
            var right = this.reader.ReadByte();*/
            Console.WriteLine(">>>> Impulse Response - Not Implemented Yet!");
            this.remainingBytes = 0;
        }
    }
}