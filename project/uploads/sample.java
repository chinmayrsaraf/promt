public class Sample {
    public static void main(String[] args) {
        int n = 10;

        // Unoptimized factorial calculation
        int factorial = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                factorial = factorial * 1; // Redundant operation
            }
        }
        System.out.println("Factorial of " + n + " is: " + factorial);

        // Unoptimized sum calculation
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += i;
        }
        sum = sum + 0; // Unnecessary addition
        System.out.println("Sum of first " + n + " numbers is: " + sum);
    }
}
