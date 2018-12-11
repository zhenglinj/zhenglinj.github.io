import java.io.*;

public class Main {
    public static void main(String [] args) {
        String ser_filename = "./employee.ser";
        {
            // Serialize demo
            Employee e = new Employee();
            e.name = "Reyan Ali";
            e.address = "Phokka Kuan, Ambehta Peer";
            e.SSN = 11122333;
            e.number = 101;

            try {
                FileOutputStream fileOut =
                        new FileOutputStream(ser_filename);
                ObjectOutputStream out = new ObjectOutputStream(fileOut);
                out.writeObject(e);
                out.close();
                fileOut.close();
                System.out.println("Serialized data is saved in " + ser_filename);
            } catch(IOException i) {
                i.printStackTrace();
            }
        }

        {
            // Deserialize demo
            Employee e = null;
            try {
                FileInputStream fileIn = new FileInputStream(ser_filename);
                ObjectInputStream in = new ObjectInputStream(fileIn);
                e = (Employee) in.readObject();
                in.close();
                fileIn.close();
            } catch(IOException i) {
                i.printStackTrace();
                return;
            } catch(ClassNotFoundException c) {
                System.out.println("Employee class not found");
                c.printStackTrace();
                return;
            }
            System.out.println("Deserialized Employee from " + ser_filename + " ..." );
            System.out.println("Name: " + e.name);
            System.out.println("Address: " + e.address);
            System.out.println("SSN: " + e.SSN);
            System.out.println("Number: " + e.number);
            e.mailCheck();
        }
    }
}