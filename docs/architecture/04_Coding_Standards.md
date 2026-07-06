# Coding Standards

**Document Version:** 1.0
**Status:** Approved
**Project:** Advancing Face Expression Recognition using Deep Learning Approaches
**Owner:** Thesis Research Project
**Author:** Naufal Muhammad Athif
**Last Updated:** 2026-07-03

---

# 1. Purpose

This document defines the coding standards adopted throughout the FER research framework.

The objective is to ensure consistency, maintainability, readability, and reproducibility across all implementation modules.

These standards apply to every Python source file within the project.

---

# 2. General Principles

The implementation follows several software engineering principles.

- Clean Code
- Object-Oriented Programming
- Single Responsibility Principle
- Separation of Concerns
- Explicit is Better than Implicit
- Configuration over Hardcoding

---

# 3. Project Structure

Every implementation must remain inside the predefined project architecture.

Source files shall only be placed inside the appropriate package.

No experimental scripts shall be stored inside the source directory.

---

# 4. Import Convention

Imports shall follow the following order.

1. Python Standard Library
2. Third-party Libraries
3. Local Project Modules

Example

```python
import os
from pathlib import Path

import torch
import torchvision

from src.datasets.base_dataset import BaseDataset
```

Wildcard imports are prohibited.

```python
from xxx import *
```

---

# 5. Type Hint

All public methods shall define explicit type hints.

Example

```python
def train(
    self,
    model: nn.Module,
    train_loader: DataLoader,
) -> None:
```

---

# 6. Documentation

Every public class shall include a class docstring.

Every public method shall include a method docstring.

The documentation should explain

- purpose
- parameters
- return values

rather than implementation details.

---

# 7. Naming Convention

## Classes

PascalCase

```
Trainer
FER2013Dataset
Evaluator
```

---

## Methods

snake_case

```
train_model()

load_dataset()

compute_metrics()
```

---

## Variables

snake_case

```
learning_rate

batch_size

train_loader
```

---

## Constants

UPPER_CASE

```
IMAGE_SIZE

NUM_CLASSES

DEFAULT_BATCH_SIZE
```

---

# 8. Hardcoded Values

Hardcoded experiment parameters are prohibited.

Incorrect

```python
epochs = 20
```

Correct

```python
epochs = config.training.epochs
```

---

# 9. Exception Handling

Custom exceptions shall be preferred over generic exceptions.

Incorrect

```python
raise ValueError(...)
```

Correct

```python
raise DatasetNotFoundError(...)
```

---

# 10. Logging

The framework shall use logging instead of print statements.

Incorrect

```python
print("Training...")
```

Correct

```python
logger.info(...)
```

---

# 11. Notebook Usage

Notebook files are reserved exclusively for

- experimentation
- visualization
- result analysis

Business logic shall never be implemented inside notebooks.

---

# 12. Reproducibility

Every experiment shall initialize

- random seed
- numpy seed
- torch seed

before training begins.

---

# 13. Code Review Checklist

Before committing code, verify the following.

- Type hints included
- Docstrings completed
- No hardcoded parameters
- No duplicate code
- Proper exception handling
- Correct package placement
- Proper logging

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-03 | Initial coding standards. |
