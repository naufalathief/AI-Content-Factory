"""
Dataset-related constants.

This module defines supported datasets and emotion labels
for Facial Expression Recognition experiments.
"""

from __future__ import annotations

from enum import StrEnum


class DatasetName(StrEnum):
    """
    Supported FER datasets.
    """

    FER2013 = "FER2013"
    FERPLUS = "FERPlus"
    AFFECTNET = "AffectNet"


class EmotionLabel(StrEnum):
    """
    Standard facial emotion labels.

    Based on common FER datasets.
    """

    ANGRY = "angry"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"
