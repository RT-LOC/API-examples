using System;
using System.IO;
using System.Linq;
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
            command = "##xx" + command;
            ASCIIEncoding ascEncoder = new ASCIIEncoding();
            byte[] byteCommand = ascEncoder.GetBytes(command);
            byte version = Convert.ToByte(0);
            byte[] payload = new byte[byteCommand.Length + 1];
            byteCommand.CopyTo(payload, 0);
            payload[byteCommand.Length] = version;
            this.stream.Write(payload, 0, payload.Length);
        }

        public void GetMessages()
        {
            try
            {
                while (true)
                {
                    using (BinaryReader reader = new BinaryReader(
                        this.stream,
                        System.Text.Encoding.ASCII,
                        true
                    ))
                    {
                        new Decoder(reader).Decode();
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