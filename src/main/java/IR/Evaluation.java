package IR;

import java.io.*;
import java.util.*;

public final class Evaluation {
    private static final int TOP_K = 25;

    private Evaluation() {
        throw new UnsupportedOperationException("Utility class should not be instantiated.");
    }

    public static void evaluateResults(String resultsFile, String qrelsFile) {
        Map<Integer, Set<Integer>> relevantDocs = loadQrels(qrelsFile);
        Map<Integer, List<SearchResult>> retrievedDocs = loadSearchResults(resultsFile);

        if (relevantDocs.isEmpty() || retrievedDocs.isEmpty()) {
            System.err.println("Error: Missing data in qrels or results file.");
            return;
        }

        EvaluationMetrics metrics = computeMetrics(retrievedDocs, relevantDocs);

        System.out.printf("%nEvaluation Results:%n");
        System.out.printf("Precision@%d: %.4f%n", TOP_K, metrics.getPrecisionAtK());
        System.out.printf("Recall: %.4f%n", metrics.getRecall());
        System.out.printf("Mean Average Precision (MAP): %.4f%n", metrics.getMeanAveragePrecision());
    }

    private static Map<Integer, Set<Integer>> loadQrels(String qrelsFile) {
        Map<Integer, Set<Integer>> qrels = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(qrelsFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.trim().split("\\s+");
                if (parts.length == 3) {  // Accepts 3-column format
                    int queryId = Integer.parseInt(parts[0]);
                    int docId = Integer.parseInt(parts[1]);
                    int relevance = Integer.parseInt(parts[2]);

                    if (relevance > 0) {
                        qrels.computeIfAbsent(queryId, k -> new HashSet<>()).add(docId);
                    }
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error reading qrels file: " + e.getMessage());
        }
        return qrels;
    }

    private static Map<Integer, List<SearchResult>> loadSearchResults(String resultsFile) {
        Map<Integer, List<SearchResult>> results = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(resultsFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.trim().split("\\s+");
                if (parts.length == 6) {
                    int queryId = Integer.parseInt(parts[0]);
                    int docId = Integer.parseInt(parts[2]);
                    int rank = Integer.parseInt(parts[3]);
                    float score = Float.parseFloat(parts[4]);
                    String runId = parts[5];

                    results.computeIfAbsent(queryId, k -> new ArrayList<>())
                            .add(new SearchResult(queryId, docId, rank, score, runId));
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error reading results file: " + e.getMessage());
        }
        return results;
    }

    private static EvaluationMetrics computeMetrics(Map<Integer, List<SearchResult>> retrievedDocs,
                                                    Map<Integer, Set<Integer>> relevantDocs) {
        double totalPrecision = 0.0;
        double totalRecall = 0.0;
        double totalMAP = 0.0;
        int queryCount = retrievedDocs.size();

        for (int queryId : retrievedDocs.keySet()) {
            List<SearchResult> retrievedList = retrievedDocs.get(queryId);
            Set<Integer> relevantSet = relevantDocs.getOrDefault(queryId, Collections.emptySet());

            totalPrecision += computePrecisionAtK(retrievedList, relevantSet);
            totalRecall += computeRecall(retrievedList, relevantSet);
            totalMAP += computeAveragePrecision(retrievedList, relevantSet);
        }

        return new EvaluationMetrics(
                queryCount > 0 ? totalPrecision / queryCount : 0.0,
                queryCount > 0 ? totalRecall / queryCount : 0.0,
                queryCount > 0 ? totalMAP / queryCount : 0.0
        );
    }

    private static double computePrecisionAtK(List<SearchResult> retrieved, Set<Integer> relevant) {
        long relevantRetrieved = retrieved.stream()
                .limit(TOP_K)
                .filter(result -> relevant.contains(result.getDocId()))
                .count();
        return TOP_K == 0 ? 0.0 : (double) relevantRetrieved / TOP_K;
    }

    private static double computeRecall(List<SearchResult> retrieved, Set<Integer> relevant) {
        if (relevant.isEmpty()) return 0.0;
        long retrievedRelevant = retrieved.stream()
                .filter(result -> relevant.contains(result.getDocId()))
                .count();
        return (double) retrievedRelevant / relevant.size();
    }

    private static double computeAveragePrecision(List<SearchResult> retrieved, Set<Integer> relevant) {
        if (relevant.isEmpty()) return 0.0;
        double sumPrecision = 0.0;
        int relevantCount = 0;

        for (int i = 0; i < retrieved.size(); i++) {
            if (relevant.contains(retrieved.get(i).getDocId())) {
                relevantCount++;
                sumPrecision += (double) relevantCount / (i + 1);
            }
        }
        return sumPrecision / relevant.size();
    }
}
