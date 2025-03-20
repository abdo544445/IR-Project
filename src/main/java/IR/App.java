package IR;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.search.similarities.ClassicSimilarity;
import org.apache.lucene.search.similarities.Similarity;

import java.util.InputMismatchException;
import java.util.Scanner;

public class App {
    private static final String CRANFIELD_DOCUMENT_PATH = "src/main/resources/cran/cran.all.1400";
    private static final String CRANFIELD_QUERY_PATH = "src/main/resources/cran/cran.qry";
    private static final String RESULTS_DIRECTORY = "src/main/resources/results/";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Select Analyzer
        int analyzerChoice = getUserChoice(scanner,
                "Select an Analyzer:\n" +
                        "1 - Standard Analyzer\n" +
                        "2 - Whitespace Analyzer\n" +
                        "3 - English Analyzer\n" +
                        "Enter choice (1/2/3): ", 1, 3);

        Analyzer analyzer;
        String scoringApproach;

        switch (analyzerChoice) {
            case 1:
                scoringApproach = "StandardAnalyzer";
                analyzer = new StandardAnalyzer();
                break;
            case 2:
                scoringApproach = "WhitespaceAnalyzer";
                analyzer = new WhitespaceAnalyzer();
                break;
            case 3:
            default:
                scoringApproach = "EnglishAnalyzer";
                analyzer = new EnglishAnalyzer();
                break;
        }

        // Select Similarity Method
        int similarityChoice = getUserChoice(scanner,
                "\nSelect a Similarity Method:\n" +
                        "1 - Vector Space Model (VSM)\n" +
                        "2 - BM25 Similarity\n" +
                        "Enter choice (1/2): ", 1, 2);

        Similarity similarity;
        switch (similarityChoice) {
            case 1:
                similarity = new ClassicSimilarity();
                scoringApproach += "VSM";
                break;
            case 2:
            default:
                similarity = new BM25Similarity();
                scoringApproach += "BM25";
                break;
        }

        // Run Indexing
        System.out.printf("\nCreating Index with %s...\n", scoringApproach);
        CreateIndex createIndexes = new CreateIndex(CRANFIELD_DOCUMENT_PATH, analyzer);

        // Run Querying
        System.out.printf("\nQuerying Index with %s...\n", scoringApproach);
        QueryIndex makeQueries = new QueryIndex(CRANFIELD_QUERY_PATH, analyzer, similarity, scoringApproach);

        // Ask if the user wants to evaluate results
        boolean evaluateResults = getUserYesNo(scanner, "\nWould you like to evaluate search performance? (y/n): ");

        if (evaluateResults) {
            System.out.printf("\nEvaluating Search Results using %s...\n", scoringApproach);
            Evaluation.evaluateResults(RESULTS_DIRECTORY + scoringApproach + ".test", "src/main/resources/cran/cranqrel");
        }

        System.out.printf("\nProcess Completed. Results saved in: %s\n", RESULTS_DIRECTORY);
        scanner.close();
    }

    private static int getUserChoice(Scanner scanner, String prompt, int min, int max) {
        int choice;
        while (true) {
            try {
                System.out.printf(prompt);
                choice = scanner.nextInt();
                if (choice >= min && choice <= max) {
                    return choice;
                }
                System.out.printf("Invalid choice. Please enter a number between %d and %d.\n", min, max);
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                scanner.next(); // Clear invalid input
            }
        }
    }

    private static boolean getUserYesNo(Scanner scanner, String prompt) {
        while (true) {
            System.out.printf(prompt);
            String input = scanner.next().trim().toLowerCase();
            if (input.equals("y")) {
                return true;
            } else if (input.equals("n")) {
                return false;
            }
            System.out.println("Invalid input. Enter 'y' for Yes or 'n' for No.");
        }
    }
}
