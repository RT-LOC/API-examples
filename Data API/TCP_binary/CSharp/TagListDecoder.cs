using System;
using System.IO;

namespace CSharp
{
    public class TagListDecoder : IDecoder
    {
        private readonly BinaryReader reader;
        public TagListDecoder(BinaryReader reader)
        {
            this.reader = reader;
        }

        public void Decode()
        {
            Console.WriteLine("> Tag List");
            var version = this.reader.ReadByte();
            var tagCount = this.reader.ReadUInt16();
            Console.WriteLine(">> Version: {0} - Tag Count: {1}", version, tagCount);

            for (int i = 0; i < tagCount; ++i)
            {
                DecodeTag(i);
            }
        }

        private void DecodeTag(int i)
        {
            var id = this.reader.ReadUInt16();
            var speed = this.reader.ReadByte();
            var z = this.reader.ReadInt16();
            Console.WriteLine(">>> Tag {0} - Tag Id: {1} - Speed: {2} - Z-Coordinate: {3}",
                i + 1,
                id,
                speed,
                z
            );
        }
    }   
}