using System.Threading;

namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            TCP tcp = new TCP(args[0]);
            tcp.ConnectToServer();
            Thread t = new Thread(new ThreadStart(tcp.GetMessages));
            t.Start();
            // To get AnchorList, uncomment the line below
            //tcp.StreamMessage("A");
            // To get TagList, uncomment the line below
            //tcp.StreamMessage("T");
        }
    }
}
