public class oammanager {

    public static void main(String[] args) {
        while (true) {
            System.out.println("Binary is running...");
            try {
                Thread.sleep(2000); // Sleep for 2 seconds
            } catch (InterruptedException e) {
                System.out.println("Interrupted! Exiting...");
                break;
            }
        }
    }
}
