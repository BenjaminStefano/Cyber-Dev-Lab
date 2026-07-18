import java.util.Scanner;

public class Main {

    private static final int MIN_LENGTH = 8;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        printHeader();

        System.out.print("Ingresa una contraseña para analizar: ");
        String password = scanner.nextLine();

        boolean hasMinimumLength = hasMinimumLength(password);
        boolean hasUppercase = hasUppercase(password);
        boolean hasLowercase = hasLowercase(password);
        boolean hasNumber = hasNumber(password);
        boolean hasSpecialCharacter = hasSpecialCharacter(password);
        boolean hasNoSpaces = hasNoSpaces(password);

        int score = calculateScore(
                hasMinimumLength,
                hasUppercase,
                hasLowercase,
                hasNumber,
                hasSpecialCharacter,
                hasNoSpaces
        );

        printResults(
                hasMinimumLength,
                hasUppercase,
                hasLowercase,
                hasNumber,
                hasSpecialCharacter,
                hasNoSpaces,
                score
        );

        scanner.close();
    }

    private static void printHeader() {
        System.out.println("==================================");
        System.out.println("     PASSWORD VALIDATOR - JAVA");
        System.out.println("==================================");
        System.out.println();
    }

    private static boolean hasMinimumLength(String password) {
        return password.length() >= MIN_LENGTH;
    }

    private static boolean hasUppercase(String password) {
        for (char character : password.toCharArray()) {
            if (Character.isUpperCase(character)) {
                return true;
            }
        }

        return false;
    }

    private static boolean hasLowercase(String password) {
        for (char character : password.toCharArray()) {
            if (Character.isLowerCase(character)) {
                return true;
            }
        }

        return false;
    }

    private static boolean hasNumber(String password) {
        for (char character : password.toCharArray()) {
            if (Character.isDigit(character)) {
                return true;
            }
        }

        return false;
    }

    private static boolean hasSpecialCharacter(String password) {
        String specialCharacters = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~";

        for (char character : password.toCharArray()) {
            if (specialCharacters.indexOf(character) >= 0) {
                return true;
            }
        }

        return false;
    }

    private static boolean hasNoSpaces(String password) {
        return !password.contains(" ");
    }

    private static int calculateScore(
            boolean hasMinimumLength,
            boolean hasUppercase,
            boolean hasLowercase,
            boolean hasNumber,
            boolean hasSpecialCharacter,
            boolean hasNoSpaces
    ) {
        int score = 0;

        if (hasMinimumLength) {
            score++;
        }

        if (hasUppercase) {
            score++;
        }

        if (hasLowercase) {
            score++;
        }

        if (hasNumber) {
            score++;
        }

        if (hasSpecialCharacter) {
            score++;
        }

        if (hasNoSpaces) {
            score++;
        }

        return score;
    }

    private static String getStrength(int score) {
        if (score <= 2) {
            return "DEBIL";
        } else if (score <= 4) {
            return "MEDIA";
        } else {
            return "FUERTE";
        }
    }

    private static String formatResult(boolean condition) {
        return condition ? "[OK]" : "[X]";
    }

    private static void printResults(
            boolean hasMinimumLength,
            boolean hasUppercase,
            boolean hasLowercase,
            boolean hasNumber,
            boolean hasSpecialCharacter,
            boolean hasNoSpaces,
            int score
    ) {
        System.out.println();
        System.out.println("RESULTADOS");
        System.out.println("----------------------------------");

        System.out.println(
                formatResult(hasMinimumLength)
                        + " Minimo " + MIN_LENGTH + " caracteres"
        );

        System.out.println(
                formatResult(hasUppercase)
                        + " Contiene una letra mayuscula"
        );

        System.out.println(
                formatResult(hasLowercase)
                        + " Contiene una letra minuscula"
        );

        System.out.println(
                formatResult(hasNumber)
                        + " Contiene un numero"
        );

        System.out.println(
                formatResult(hasSpecialCharacter)
                        + " Contiene un caracter especial"
        );

        System.out.println(
                formatResult(hasNoSpaces)
                        + " No contiene espacios"
        );

        System.out.println("----------------------------------");
        System.out.println("Puntuacion: " + score + "/6");
        System.out.println("Fortaleza: " + getStrength(score));

        if (score == 6) {
            System.out.println("La contraseña cumple todas las reglas.");
        } else {
            System.out.println(
                    "La contraseña necesita mejoras antes de considerarse segura."
            );
        }
    }
}