"""
Unit tests for metric constants.
"""

from src.constants.metrics import MetricName


def test_metric_names() -> None:
    """
    Metric constants should have correct values.
    """

    assert MetricName.ACCURACY == "accuracy"
    assert MetricName.PRECISION == "precision"
    assert MetricName.RECALL == "recall"
    assert MetricName.F1_SCORE == "f1_score"
    assert MetricName.CONFUSION_MATRIX == "confusion_matrix"


def test_number_of_metrics() -> None:
    """
    Metric constants should contain all required metrics.
    """

    assert len(MetricName) == 5
