using System;
using System.IO;

namespace CSharp
{
    public class NodeStatusDecoder : IDecoder
    {
        private readonly BinaryReader reader;
        public NodeStatusDecoder(BinaryReader reader)
        {
            this.reader = reader;
        }

        public void Decode()
        {
            Console.WriteLine("> Node Status:");
            var version = this.reader.ReadByte();
            var blockLength = this.reader.ReadByte();
            var nodeCount = this.reader.ReadUInt16();
            Console.WriteLine(
                ">> Version: {0} - Block Length: {1} - Node Count: {2}",
                version,
                blockLength,
                nodeCount
            );

            for (int i = 0; i < nodeCount; ++i)
            {
                DecodeNode();
            }
        }

        private void DecodeNode()
        {
            var nodeId = this.reader.ReadUInt16();
            var nodeKind = this.reader.ReadByte();
            var frameOffMicro = this.reader.ReadUInt16();
            var uptime = this.reader.ReadUInt32();
            var resetReason = this.reader.ReadByte();

            var configVer = this.reader.ReadUInt16();
            var tagspeedVer = this.reader.ReadUInt16();
            var antDelay = this.reader.ReadUInt16();
            var lastSeen = this.reader.ReadUInt32();
            var lastUserData = this.reader.ReadUInt32();
            var voltage = this.reader.ReadUInt16();

            var hwNumber = this.reader.ReadByte();
            var loaderVer = this.reader.ReadUInt16();
            var loaderCrc = this.reader.ReadUInt16();
            var anchorVer = this.reader.ReadUInt16();
            var anchorCrc = this.reader.ReadUInt16();
            var tagVer = this.reader.ReadUInt16();
            var tagCrc = this.reader.ReadUInt16();
            var tagSubver = this.reader.ReadByte();
            var deca64 = this.reader.ReadUInt64();

            string output = @">>> Node {0} -
            Node Id: {1}
            Node Kind: {2}
            Frame Off Micro: {3}
            Uptime: {4}
            Reset Reason: {5}
            Config Ver: {6}
            Tagspeed Ver: {7}
            Ant Delay: {8}
            Last Seen: {9}
            Last User Data: {10}
            Voltage: {11}
            Hardware Number: {12}
            Loader Ver: {13}
            Loader CRC: {14}
            Anchor Ver: {15}
            Anchor CRC: {16}
            Tag Ver: {17}
            Tag CRC: {18}
            Tag Subver: {19}
            Deca64: {20}";

            Console.WriteLine(
                output,
                nodeId,
                nodeKind,
                frameOffMicro,
                uptime,
                resetReason,
                configVer,
                tagspeedVer,
                antDelay,
                lastSeen,
                lastUserData,
                voltage,
                hwNumber,
                loaderVer,
                loaderCrc,
                anchorVer,
                anchorCrc,
                tagVer,
                tagCrc,
                tagSubver,
                deca64
            );
        }
    }   
}