using System;
using System.IO;

namespace CSharp
{
    public class AnchorListDecoder : IDecoder
    {
        private readonly BinaryReader reader;
        private uint bytesLength;
        public AnchorListDecoder(BinaryReader reader, uint bytesLength)
        {
            this.reader = reader;
            this.bytesLength = bytesLength;
        }

        public void Decode()
        {
            Console.WriteLine("> Anchor List");
            var version = this.reader.ReadByte();
            bytesLength--;
            var anchorCount = (int) Math.Round(
                ((double) (bytesLength - 6) / 8),
                MidpointRounding.AwayFromZero
            );
            Console.WriteLine(">> Version: {0} - Anchor Count: {1}", version, anchorCount);

            for (int i = 0; i < anchorCount; ++i)
            {
                DecodeAnchor(i);
            }
        }
        
        private void DecodeAnchor(int i)
        {
            var id = this.reader.ReadUInt16();
            var x = this.reader.ReadInt16();
            var y = this.reader.ReadInt16();
            var z = this.reader.ReadInt16();

            Console.WriteLine(">>> Anchor {0} - Anchor Id: {1} - Coordinates: [{2}, {3}, {4}]",
                i + 1,
                id,
                x,
                y,
                z
            );
        }
    }   
}