package IR;

public final class EvaluationMetrics {
    private final double precisionAtK;
    private final double recall;
    private final double meanAveragePrecision;

    public EvaluationMetrics(double precisionAtK, double recall, double meanAveragePrecision) {
        this.precisionAtK = precisionAtK;
        this.recall = recall;
        this.meanAveragePrecision = meanAveragePrecision;
    }

    public double getPrecisionAtK() {
        return precisionAtK;
    }

    public double getRecall() {
        return recall;
    }

    public double getMeanAveragePrecision() {
        return meanAveragePrecision;
    }
}
