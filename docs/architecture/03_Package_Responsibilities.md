# Package Responsibilities

**Document Version:** 1.0
**Status:** Approved
**Project:** Advancing Face Expression Recognition using Deep Learning Approaches
**Owner:** Thesis Research Project
**Author:** Naufal Muhammad Athif
**Last Updated:** 2026-07-03

---

# 1. Purpose

This document defines the responsibilities of each software package within the research framework.

The objective is to establish clear ownership for every architectural component, ensuring that each package has a single well-defined responsibility.

This document follows the Single Responsibility Principle (SRP) and serves as the implementation guideline throughout the development process.

---

# 2. Package Overview

| Package | Primary Responsibility |
|----------|------------------------|
| config | Store experiment configurations. |
| core | Coordinate the complete experiment lifecycle. |
| datasets | Load benchmark datasets and prepare samples. |
| preprocessing | Perform image preprocessing and augmentation. |
| models | Define neural network architectures. |
| training | Execute model training and optimization. |
| evaluation | Evaluate trained models and compute performance metrics. |
| utils | Provide reusable utility functions. |
| constants | Store immutable project constants. |
| exceptions | Define custom exception classes. |

---

# 3. Detailed Responsibilities

## Configuration Package (`config`)

### Responsibilities

- Store experiment configurations.
- Store hyperparameters.
- Store dataset paths.
- Store experiment settings.

### Must Not

- Train models.
- Load datasets.
- Execute preprocessing.

---

## Core Package (`core`)

### Responsibilities

- Coordinate experiment execution.
- Initialize the experiment pipeline.
- Connect all framework components.
- Manage experiment workflow.

### Must Not

- Train models directly.
- Compute evaluation metrics.
- Read datasets manually.

---

## Dataset Package (`datasets`)

### Responsibilities

- Load datasets.
- Parse labels.
- Prepare PyTorch Dataset objects.
- Harmonize dataset formats.

### Must Not

- Perform model training.
- Compute evaluation metrics.

---

## Preprocessing Package (`preprocessing`)

### Responsibilities

- Resize images.
- Normalize images.
- Apply data augmentation.
- Prepare image transformations.

### Must Not

- Load datasets.
- Train models.

---

## Models Package (`models`)

### Responsibilities

- Define neural network architectures.
- Build MobileNetV2.
- Configure transfer learning layers.

### Must Not

- Perform optimization.
- Execute training loops.
- Save checkpoints.

---

## Training Package (`training`)

### Responsibilities

- Execute training.
- Optimize network parameters.
- Save checkpoints.
- Produce training logs.

### Generated Artifacts

- Best Model Checkpoint
- Last Model Checkpoint
- Training Logs

---

## Evaluation Package (`evaluation`)

### Responsibilities

- Perform inference.
- Compute evaluation metrics.
- Evaluate cross-dataset performance.
- Generate evaluation reports.

### Generated Artifacts

- Accuracy
- Precision
- Recall
- F1-score
- Performance Tables
- Figures

---

## Utilities Package (`utils`)

### Responsibilities

- Random seed initialization.
- Device selection.
- Logging utilities.
- Helper functions.

---

## Constants Package (`constants`)

### Responsibilities

Store immutable project constants.

Examples include

- Emotion labels
- Dataset names
- Image size
- Strategy names

---

## Exceptions Package (`exceptions`)

### Responsibilities

Provide custom exceptions for the framework.

Examples include

- DatasetNotFoundError
- InvalidConfigurationError
- InvalidTrainingStrategyError

---

# 4. Experiment Artifacts

The framework generates several persistent artifacts throughout the experiment lifecycle.

| Producer | Artifact | Output Directory |
|----------|----------|------------------|
| Training | Model Checkpoints | outputs/checkpoints |
| Training | Training Logs | outputs/logs |
| Evaluation | Metrics | outputs/reports/metrics |
| Evaluation | Figures | outputs/reports/figures |
| Evaluation | Performance Tables | outputs/reports/tables |
| Core (Optional) | Experiment Summary | outputs/reports |

---

# 5. Design Principles

The package architecture follows the principles below.

- Single Responsibility Principle
- Separation of Concerns
- Low Coupling
- High Cohesion
- Configuration-Driven Design
- Reproducible Research

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-03 | Initial package responsibility specification. |
