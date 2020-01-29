using System;
using System.IO;

namespace CSharp
{
    public class Decoder : IDecoder
    {
        private readonly BinaryReader reader;
        private uint pkgLength;
        private uint delim;
        private char pkgType;
        public Decoder(BinaryReader reader)
        {
            this.reader = reader;
        }

        public void Decode()
        {
            this.delim = reader.ReadUInt16();
            this.pkgLength = reader.ReadUInt16();
            this.pkgType = reader.ReadChar();

            if (this.delim.Equals(8995))
                Console.WriteLine(
                    "\nConverted - Delim: {0}, Package Length: {1}, Package Type: {2}",
                    this.delim,
                    this.pkgLength,
                    this.pkgType
                );
            DecodeMessageByType();
        }

        public void DecodeMessageByType()
        {
            if (this.delim == 8995)
            {
                switch (this.pkgType)
                {
                    case 'D':
                        new DataDecoder(this.reader).Decode();
                        break;
                    case 'A':
                        new AnchorListDecoder(this.reader, this.pkgLength).Decode();
                        break;
                    case 'T':
                        new TagListDecoder(this.reader, this.pkgLength).Decode();
                        break;
                    case 'X':
                        new NodeStatusDecoder(this.reader).Decode();
                        break;
                    default:
                        Console.WriteLine("Unknown message type!");
                        break;
                }
            }
        }
    }
}