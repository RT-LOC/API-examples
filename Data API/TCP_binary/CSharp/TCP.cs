using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace CSharp
{
    public class TCP
    {
        private IPAddress serverIp;
        private Int32 serverPort;
        private TcpClient tcpClient;
        private NetworkStream stream;
        public TCP(string serverIp)
        {
            this.serverIp = IPAddress.Parse(serverIp);
            this.serverPort = 13100;
        }
        
        public void ConnectToServer()
        {
            Console.WriteLine("Connecting...");
            try
            {
                this.tcpClient = new TcpClient();
                this.tcpClient.Connect(this.serverIp, this.serverPort);
                Console.WriteLine("Connected!");
                this.stream = this.tcpClient.GetStream();
            }
            catch (System.Exception ex)
            {
                Console.WriteLine(
                    "An error occurred while attempting to connect to host: {0}",
                    this.serverIp
                );
                Console.WriteLine(ex);
                throw;
            }
        }

        public void StreamMessage(string command)
        {
            ASCIIEncoding ascEncoder = new ASCIIEncoding();

            byte[] byteCommand = ascEncoder.GetBytes("##");
            byte[] payloadLength = BitConverter.GetBytes((ushort) 6);
            byte[] _command = ascEncoder.GetBytes(command);
            byte version = (byte) 0;
            var totalLength = byteCommand.Length + payloadLength.Length + _command.Length + 1;
            byte[] payload = new byte[totalLength];

            byteCommand.CopyTo(payload, 0);
            payloadLength.CopyTo(payload, byteCommand.Length);
            _command.CopyTo(payload, (totalLength - 2));
            payload[--totalLength] = version;
            using (BinaryWriter writer = new BinaryWriter(
                this.stream,
                System.Text.Encoding.ASCII,
                true
            ))
            {
                writer.Write(payload);
                writer.Flush();
            }
        }

        public void GetMessages()
        {
            try
            {
                using (BinaryReader reader = new BinaryReader(
                    this.stream,
                    System.Text.Encoding.ASCII,
                    true
                ))
                {
                    while (true)
                    {
                        if (this.stream.DataAvailable)
                        {
                            new Decoder(reader).Decode();
                        }
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
                this.tcpClient.Close();
                Console.WriteLine("Connection closed!");
            }
        }
    }
}