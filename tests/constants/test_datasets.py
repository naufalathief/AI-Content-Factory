"""
Unit tests for dataset constants.
"""

from src.constants.datasets import (
    DatasetName,
    EmotionLabel,
)


def test_dataset_names() -> None:
    """
    Dataset constants should have correct values.
    """

    assert DatasetName.FER2013.value == "FER2013"
    assert DatasetName.FERPLUS.value == "FERPlus"
    assert DatasetName.AFFECTNET.value == "AffectNet"


def test_emotion_labels() -> None:
    """
    Emotion labels should contain standard FER classes.
    """

    expected = {
        "angry",
        "disgust",
        "fear",
        "happy",
        "sad",
        "surprise",
        "neutral",
    }

    labels = {emotion.value for emotion in EmotionLabel}

    assert labels == expected
