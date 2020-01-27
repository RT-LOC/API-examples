using System;

namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            TCP _tcp = new TCP("192.168.200.221");
            _tcp.ConnectToServer();
            _tcp.GetMessages();
        }
    }
}
