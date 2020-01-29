namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            TCP tcp = new TCP(args[0]);
            tcp.ConnectToServer();
            tcp.GetMessages();
        }
    }
}
