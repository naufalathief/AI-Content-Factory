# Dependency Graph

**Document Version:** 1.0
**Status:** Approved
**Project:** Advancing Face Expression Recognition using Deep Learning Approaches
**Owner:** Thesis Research Project
**Author:** Naufal Muhammad Athif
**Last Updated:** 2026-07-03

---

# 1. Purpose

This document defines the dependency relationships between software packages within the research framework.

The objective of this document is to establish clear interaction boundaries among software components while minimizing coupling and maintaining high cohesion.

The dependency graph acts as the architectural rulebook that determines which software packages are allowed to communicate directly during execution.

---

# 2. Dependency Philosophy

The framework adopts a layered dependency architecture.

Dependencies always flow from higher-level components toward lower-level components.

Each package should depend only on the components required to accomplish its responsibility.

Circular dependencies are strictly prohibited.

---

# 3. High-Level Dependency Graph

```text
                           Experiment Orchestrator
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
 Configuration                  Dataset Layer                 Training Layer
                                      │                             │
                                      ▼                             │
                              Preprocessing Layer                   │
                                      │                             │
                                      └──────────────┐              │
                                                     ▼              ▼
                                                Model Layer
                                                     │
                                                     ▼
                                              Evaluation Layer

────────────────────────────────────────────────────────────────────────────

Shared Components

• Constants
• Utilities
• Exceptions
```

---

# 4. Dependency Rules

| Package | Allowed Dependencies |
|----------|----------------------|
| core | config, datasets, training, evaluation |
| config | None |
| constants | None |
| utils | None |
| exceptions | None |
| datasets | preprocessing, constants, exceptions |
| preprocessing | constants |
| models | constants |
| training | config, datasets, models, utils |
| evaluation | models, utils, constants |
| tests | All packages |

---

# 5. Architectural Constraints

The following architectural constraints shall always be respected.

## Rule 1

Dependencies must always point downward.

Higher-level packages may depend on lower-level packages.

Lower-level packages must never depend on higher-level packages.

---

## Rule 2

The Model layer must remain independent.

Model implementations must never contain training logic.

---

## Rule 3

Dataset modules are responsible only for data preparation.

They must never perform training or evaluation.

---

## Rule 4

Evaluation modules operate only on trained models.

They must never update model parameters.

---

## Rule 5

Configuration must remain independent from implementation packages.

Configuration only provides parameters and should never execute business logic.

---

# 6. Design Rationale

The dependency structure provides several architectural advantages.

- Low Coupling
- High Cohesion
- Better Maintainability
- Easier Testing
- Better Scalability
- Improved Research Reproducibility

The architecture also prevents circular dependencies and simplifies future framework extensions.

---

# 7. Future Extension

Future research may introduce additional packages, including:

- Backbone Registry
- Hyperparameter Optimization
- Experiment Scheduler
- Visualization Module

Any future package must comply with the dependency rules defined in this document.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-03 | Initial dependency graph. |
