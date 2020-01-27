using System;
using System.IO;
using System.Net;
using System.Net.Sockets;

namespace CSharp
{
    public class TCP
    {
        private IPAddress _serverIp;
        private Int32 _serverPort;
        private TcpClient _tcpClient;
        public TCP(string serverIp)
        {
            _serverIp = IPAddress.Parse(serverIp);
            _serverPort = 13100;
        }
        
        public void ConnectToServer()
        {
            Console.WriteLine("Connecting...");
            _tcpClient = new TcpClient();
            try
            {
                _tcpClient.Connect(_serverIp, _serverPort);
                Console.WriteLine("Connected!");
            }
            catch (System.Exception ex)
            {
                Console.WriteLine("An error occurred while attempting to connect to host: {0}", _serverIp);
                Console.WriteLine(ex);
                throw;
            }
        }

        /*public void StreamMessage(string message)
        {
            ASCIIEncoding ascEncoder = new ASCIIEncoding();
            byte[] bytePayload = ascEncoder.GetBytes(message);

            _tcpClient.GetStream().Write(bytePayload, 0, bytePayload.Length);
        }*/

        public void GetMessages()
        {
            Byte[] header = new Byte[5];

            try
            {
                while (true)
                {

                    NetworkStream stream = _tcpClient.GetStream();

                    uint pkgLength;
                    uint delim;
                    char pkgType;
                    using (BinaryReader reader = new BinaryReader(stream, System.Text.Encoding.ASCII, true))
                    {
                        BinaryReader newReader;
                        (pkgLength, delim, pkgType, newReader) = new Decoder().Decode(reader);
                        new Decoder().Decode(newReader, delim, pkgType, pkgLength);
                    }
                }
            }
            catch (System.IO.IOException e)
            {
                Console.WriteLine("IOException: {0}", e);
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }
            finally
            {
                Console.WriteLine("Closing connection...");
                _tcpClient.Close();
                Console.WriteLine("Connection closed!");
            }
        }
    }
}