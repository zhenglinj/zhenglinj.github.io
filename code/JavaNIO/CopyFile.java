import java.io.*;
import java.nio.*;
import java.nio.channels.*;

public class CopyFile
{
    static public void main(String args[]) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: java CopyFile infile outfile");
            System.exit(1);
        }

        String infile = args[0];
        String outfile = args[1];

        // Step1. 从 FileInputStream / FileOutputStream 获取通道 fcin / fcout
        FileInputStream fin = new FileInputStream(infile);
        FileOutputStream fout = new FileOutputStream(outfile);
        FileChannel fcin = fin.getChannel();
        FileChannel fcout = fout.getChannel();

        // Step2. 创建缓冲区 buffer
        ByteBuffer buffer = ByteBuffer.allocate(1024);

        while (true) {
            // 重设缓冲区
            buffer.clear();

            // Step3. 将数据从通道 fin 读到缓冲区 buffer 中
            int r = fcin.read(buffer);
            // 当没有更多的数据时，拷贝就算完成，并且可以在 read() 方法返回 -1 是判断这一点
            if (r == -1) {
                break;
            }

            // Step3. 将数据 put() 到 buffer，再写入到通道 fcout
            // buffer.put('$');
            // flip() 方法让缓冲区可以将新读入的数据写入另一个通道
            buffer.flip();
            fcout.write(buffer);
        }
    }
}