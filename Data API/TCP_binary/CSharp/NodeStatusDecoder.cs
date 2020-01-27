using System;
using System.IO;

namespace CSharp
{
    public class NodeStatusDecoder : IDecoder
    {
        public NodeStatusDecoder()
        {

        }

        /* public void Decode(Byte[] rawBytes, int bytesLength)
        {
            Console.WriteLine("> Node Status:");
            var version = rawBytes[0];
            var blockLength = rawBytes[1];
            var nodeCount = DecoderHelper.ReadUShort(rawBytes[2..]);
            Console.WriteLine(
                ">> Version: {0} - Block Length: {1} - Node Count: {2}",
                version,
                blockLength,
                nodeCount
            );

            // TODO: Unpack node_stat
        } */
        public void Decode(BinaryReader reader)
        {
            
        }
    }   
}