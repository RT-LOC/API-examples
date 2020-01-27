using System;
using System.Collections.Generic;
using System.IO;

namespace CSharp
{
    public class Decoder
    {
        private IList<string> messageTypes;
        public Decoder()
        {
            messageTypes = new List<string>() {
                "D",
                "A",
                "T",
                "X"
            };
        }

        public (uint, uint, char, BinaryReader) Decode(BinaryReader reader)
        {
            var delim = reader.ReadUInt16();
            var pkgLength = reader.ReadUInt16();
            var pkgType = reader.ReadChar();

            if (delim == 8995)
                Console.WriteLine(
                    "Converted - Delim: {0}, Package Length: {1}, Package Type: {2}",
                    delim,
                    pkgLength,
                    pkgType
                );
            return (pkgLength, delim, pkgType, reader);
        }

        public void Decode(BinaryReader reader, uint delim, char pkgType, uint bytesLength)
        {
            if (delim == 8995)
            {
                switch (pkgType)
                {
                    case 'D':
                        new DataDecoder().Decode(reader);
                        break;
                    case 'A':
                        new AnchorListDecoder().Decode(reader);
                        break;

                    case 'T':
                        new TagListDecoder().Decode(reader);
                        break;

                    case 'X':
                        new NodeStatusDecoder().Decode(reader);
                        break;
                        
                    default:
                        Console.WriteLine("Unknown message type!");
                        break;
                }
            }
        }
    }
}