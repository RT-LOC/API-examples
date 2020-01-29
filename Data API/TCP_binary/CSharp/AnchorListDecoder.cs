using System;
using System.IO;

namespace CSharp
{
    public class AnchorListDecoder : IDecoder
    {
        private readonly BinaryReader reader;
        public AnchorListDecoder(BinaryReader reader)
        {
            this.reader = reader;
        }

        public void Decode()
        {
            Console.WriteLine("> Anchor List");
            var version = this.reader.ReadByte();
            var anchorCount = this.reader.ReadInt16();
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