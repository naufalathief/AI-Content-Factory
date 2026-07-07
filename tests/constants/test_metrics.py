"""
Unit tests for metric constants.
"""

from src.constants.metrics import MetricName


def test_metric_names() -> None:
    """
    Metric constants should have correct values.
    """

    assert MetricName.ACCURACY.value == "accuracy"
    assert MetricName.PRECISION.value == "precision"
    assert MetricName.RECALL.value == "recall"
    assert MetricName.F1_SCORE.value == "f1_score"
    assert MetricName.CONFUSION_MATRIX.value == "confusion_matrix"


def test_number_of_metrics() -> None:
    """
    Metric constants should contain all required metrics.
    """

    assert len(MetricName) == 5
