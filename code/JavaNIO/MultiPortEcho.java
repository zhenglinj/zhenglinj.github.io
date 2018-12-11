import java.io.*;
import java.net.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;

public class MultiPortEcho
{
    private int ports[];
    private ByteBuffer echoBuffer = ByteBuffer.allocate( 1024 );

    public MultiPortEcho( int ports[] ) throws IOException {
        this.ports = ports;

        go();
    }

    private void go() throws IOException {
        // ** 异步 I/O 中的核心对象为 Selector **
        // Step1. Create a new selector
        Selector selector = Selector.open();

        // Open a listener on each port, and register each one
        // with the selector
        for (int i=0; i<ports.length; ++i) {
            // Step2. 打开 ServerSocketChannel
            ServerSocketChannel ssc = ServerSocketChannel.open();
            ssc.configureBlocking( false );

            ServerSocket ss = ssc.socket();
            InetSocketAddress address = new InetSocketAddress( ports[i] );
            ss.bind( address );

            // Step3. 向 Selector 注册各种 I/O 事件
            // SelectionKey 代表该通道在此 Selector 上的注册
            // 当 Selector 通知某个传入事件时，是通过提供对应于该事件的 SelectionKey 来进行的
            // SelectionKey 还可以用于取消通道的注册
            SelectionKey key = ssc.register( selector, SelectionKey.OP_ACCEPT );

            System.out.println( "Going to listen on "+ports[i] );
        }

        while (true) {
            // Step4. 内部循环
            int num = selector.select(); // Blocking here until event(s) occur

            // Selector 的 selectedKeys() 方法返回发生了事件的 SelectionKey 对象集合
            Set selectedKeys = selector.selectedKeys();
            Iterator it = selectedKeys.iterator();

            while (it.hasNext()) {
                SelectionKey key = (SelectionKey)it.next();
                // Step7. 删除处理过的 SelectionKey
                it.remove();

                // Step5. 监听新连接或者接收数据
                if ((key.readyOps() & SelectionKey.OP_ACCEPT)
                    == SelectionKey.OP_ACCEPT) {
                    // Step6. accept 新连接
                    // Accept the new connection
                    ServerSocketChannel ssc = (ServerSocketChannel)key.channel();
                    SocketChannel sc = ssc.accept();
                    sc.configureBlocking( false );

                    // Add the new connection to the selector
                    SelectionKey newKey = sc.register( selector, SelectionKey.OP_READ );
                    System.out.println( "Got connection from "+sc );
                } else if ((key.readyOps() & SelectionKey.OP_READ)
                           == SelectionKey.OP_READ) {
                    // Read the data
                    SocketChannel sc = (SocketChannel)key.channel();

                    // Echo data
                    int bytesEchoed = 0;
                    while (true) {
                        echoBuffer.clear();

                        int r = sc.read( echoBuffer );

                        if (r < 0) {
                            // {{
                            // TODO: 对端关闭
                            InetAddress clientAddr = sc.socket().getInetAddress();
                            System.out.println(clientAddr.getHostAddress() +
                                               " disconnected.");
                            try {
                                sc.close();
                            }
                            catch (Exception e) {
                                System.out.println("Failed to close client socket channel.");
                                e.printStackTrace();
                            }
                            break;
                            // }}
                        }

                        if (r == 0) {
                            break;
                        }

                        echoBuffer.flip();

                        sc.write( echoBuffer );
                        bytesEchoed += r;
                    }

                    System.out.println( "Echoed "+bytesEchoed+" from "+sc );
                }

            }

            //System.out.println( "going to clear" );
            //      selectedKeys.clear();
            //System.out.println( "cleared" );
        }
    }

    static public void main( String args[] ) throws Exception {
        if (args.length<=0) {
            System.err.println( "Usage: java MultiPortEcho port [port port ...]" );
            System.exit( 1 );
        }

        int ports[] = new int[args.length];

        for (int i=0; i<args.length; ++i) {
            ports[i] = Integer.parseInt( args[i] );
        }

        new MultiPortEcho( ports );
    }
}
