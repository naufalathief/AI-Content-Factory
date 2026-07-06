"""
Evaluation metric constants.

This module defines supported evaluation metrics
for model performance analysis.
"""

from __future__ import annotations

from enum import StrEnum


class MetricName(StrEnum):
    """
    Supported evaluation metrics.
    """

    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    CONFUSION_MATRIX = "confusion_matrix"
