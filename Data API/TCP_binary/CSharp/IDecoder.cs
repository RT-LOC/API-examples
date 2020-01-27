using System;
using System.IO;

namespace CSharp
{
    public interface IDecoder
    {
        void Decode(BinaryReader reader);
    }
}