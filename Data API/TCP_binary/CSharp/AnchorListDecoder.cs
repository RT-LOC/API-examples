using System;
using System.IO;

namespace CSharp
{
    public class AnchorListDecoder : IDecoder
    {
        public AnchorListDecoder()
        {

        }

        /* public void Decode(Byte[] rawBytes, int bytesLength)
        {
            Console.WriteLine("> AnchorList");
            var version = rawBytes[0];
            var data_len = rawBytes.Length;
            var anchor_cnt = (data_len-6)/8;
            Console.WriteLine(
                ">> Anchor count: {0}",
                anchor_cnt
            );
            for (int i = 0; i < anchor_cnt; ++i){
                var id = DecoderHelper.ReadUShort(rawBytes[1..3]);
                var x_coord = DecoderHelper.ReadShort(rawBytes[3..5]);
                var y_coord = DecoderHelper.ReadShort(rawBytes[5..7]);
                var z_coord = DecoderHelper.ReadShort(rawBytes[7..9]);
            }
        } */

        public void Decode(BinaryReader reader)
        {
            
        }
    }   
}