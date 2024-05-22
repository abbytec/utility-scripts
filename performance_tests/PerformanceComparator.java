package performance_tests;

import java.util.PrimitiveIterator;
import java.util.regex.Pattern;

public class PerformanceComparator {
    private static final Pattern DIGITS_ONLY = Pattern.compile("\\d+");

    // Método antiguo
    public static String getCharTypeInfoOld(String word) {
        if (DIGITS_ONLY.matcher(word).matches()) {
            return "0";
        }
        String wordLower = word.toLowerCase();
        if (word.equals(wordLower)) {
            return "";
        } else if (word.equals(word.toUpperCase())) {
            return "AA";
        } else if (word.equals(word.substring(0, 1).toUpperCase() + wordLower.substring(1))) {
            return "Aa";
        } else {
            StringBuilder builder = new StringBuilder();
            for (char character : word.toCharArray()) {
                builder.append(Character.isUpperCase(character) ? '1' : '0');
            }
            return builder.toString();
        }
    }

    // Nuevo método
    public static String getCharTypeInfoNew(String word) {
        if (DIGITS_ONLY.matcher(word).matches()) {
            return "0";
        }

        PrimitiveIterator.OfInt iterator = word.chars().iterator();

        boolean firstIsLowerCase = Character.isLowerCase(iterator.nextInt());
        boolean restIsLowerCase = true;
        boolean hasALowerCase = firstIsLowerCase;

        while (iterator.hasNext()) {
            if (Character.isUpperCase(iterator.nextInt())) {
                restIsLowerCase = false;
            } else {
                hasALowerCase = true;
            }
        }

        if (firstIsLowerCase && restIsLowerCase) {
            return "";
        } else if (restIsLowerCase) {
            return "Aa";
        } else if (!firstIsLowerCase && !hasALowerCase) {
            return "AA";
        }
        StringBuilder builder = new StringBuilder();
        builder.append(firstIsLowerCase ? '0' : '1');
        word.substring(1).chars().forEach(
                character -> builder.append(Character.isUpperCase(character) ? '1' : '0'));
        return builder.toString();
    }

    public static void main(String[] args) {
        String[] testWords = {
                "12345", "hello", "HELLO", "Hello", "HeLLo", "PerformanceTestWord", "a", "A", "aa", "AA", "Aa"
        };

        // Calcular el tiempo del método antiguo
        long startTimeOld = System.nanoTime();
        for (int i = 0; i < 10000000; i++) {
            for (String word : testWords) {
                getCharTypeInfoOld(word);
            }
        }
        long endTimeOld = System.nanoTime();
        long durationOld = endTimeOld - startTimeOld;

        // Calcular el tiempo del método nuevo
        long startTimeNew = System.nanoTime();
        for (int i = 0; i < 10000000; i++) {
            for (String word : testWords) {
                getCharTypeInfoNew(word);
            }
        }
        long endTimeNew = System.nanoTime();
        long durationNew = endTimeNew - startTimeNew;

        // Imprimir los resultados
        System.out.println("Duración del método antiguo: " + durationOld / 1000000 + " ms");
        System.out.println("Duración del método nuevo: " + durationNew / 1000000 + " ms");
        System.out
                .println(
                        "El método nuevo demora " + (durationOld - durationNew) / 1000000 + " ms menos que el antiguo");
    }
}
