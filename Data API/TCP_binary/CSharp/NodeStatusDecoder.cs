using System;
using System.IO;

namespace CSharp
{
    public class NodeStatusDecoder : IDecoder
    {
        public NodeStatusDecoder()
        {

        }

        public void Decode(BinaryReader reader)
        {
            Console.WriteLine("> Node Status:");
            var version = reader.ReadByte();
            var blockLength = reader.ReadByte();
            var nodeCount = reader.ReadUInt16();
            Console.WriteLine(
                ">> Version: {0} - Block Length: {1} - Node Count: {2}",
                version,
                blockLength,
                nodeCount
            );

            for (int i = 0; i < nodeCount; ++i)
            {
                var nodeId = reader.ReadUInt16();
                var nodeKind = reader.ReadByte();
                var frameOffMicro = reader.ReadUInt16();
                var uptime = reader.ReadUInt32();
                var resetReason = reader.ReadByte();

                var configVer = reader.ReadUInt16();
                var tagspeedVer = reader.ReadUInt16();
                var antDelay = reader.ReadUInt16();
                var lastSeen = reader.ReadUInt32();
                var lastUserData = reader.ReadUInt32();
                var voltage = reader.ReadUInt16();

                var hwNumber = reader.ReadByte();
                var loaderVer = reader.ReadUInt16();
                var loaderCrc = reader.ReadUInt16();
                var anchorVer = reader.ReadUInt16();
                var anchorCrc = reader.ReadUInt16();
                var tagVer = reader.ReadUInt16();
                var tagCrc = reader.ReadUInt16();
                var tagSubver = reader.ReadByte();
                var deca64 = reader.ReadUInt64();

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
}