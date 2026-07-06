# Software Architecture Blueprint

| Item | Description |
|------|-------------|
| Document | Software Architecture Blueprint |
| Version | 1.0 |
| Status | Approved |
| Project | Advancing Face Expression Recognition using Deep Learning Approaches |
| Owner | Thesis Research Project |
| Author | Naufal Muhammad Athif |
| Last Updated | 2026-07-03 |

---

# 1. Purpose

This document defines the overall software architecture of the research framework developed for the thesis entitled **"Advancing Face Expression Recognition using Deep Learning Approaches."**

The primary objective of this document is to establish a stable architectural foundation before implementation begins.

Instead of documenting implementation details, this blueprint defines the architectural vision that governs the entire software framework throughout the research lifecycle.

Every architectural decision described within this document is intended to improve software quality while maintaining consistency with the research methodology presented in the thesis.

The architecture emphasizes modularity, maintainability, scalability, reproducibility, and software quality.

This document serves as the highest-level architectural reference for the project.

All subsequent architecture documents, implementation modules, and software components shall conform to the principles defined within this blueprint.

---

# 2. Scope

This document covers the software architecture of the complete machine learning research framework.

The architecture is responsible for supporting the following research activities.

- Dataset preparation.
- Image preprocessing.
- Deep learning model construction.
- Transfer learning implementation.
- Model training.
- Model validation.
- Cross-dataset evaluation.
- Performance analysis.
- Experiment artifact generation.

The scope of this document is intentionally limited to software architecture.

Research methodology, implementation details, source code, and experimental results are documented separately within other project documents.

---

# 3. Assumptions

The architecture is designed based on the following assumptions.

## 3.1 Research-Oriented Framework

The software framework is developed exclusively for academic research purposes.

Although software engineering best practices are adopted, the framework prioritizes research reproducibility rather than production deployment.

---

## 3.2 Controlled Execution Environment

All experiments are assumed to be executed within a controlled software environment.

Software dependencies, Python versions, and framework configurations remain consistent throughout the research.

---

## 3.3 Benchmark Datasets

Benchmark datasets are assumed to be available before experiment execution begins.

Dataset preparation, licensing, and acquisition are outside the scope of this architecture.

---

## 3.4 Approved Research Scope

Only software components directly related to the approved research methodology are implemented.

Additional models, datasets, or algorithms may be incorporated only if they remain consistent with future research extensions.

---

## 3.5 Reproducibility

Reproducibility is considered a primary architectural requirement.

Given identical configurations and random seeds, the framework should produce consistent experimental results.

---

# 4. Architectural Objectives

The software architecture has been designed to achieve the following objectives.

---

## 4.1 Modularity

The framework shall be divided into independent software modules.

Each module performs one clearly defined responsibility.

The architecture minimizes unnecessary coupling between software components.

---

## 4.2 Maintainability

Software maintenance should require minimal modification to existing modules.

Changes introduced into one component should have minimal impact on unrelated packages.

---

## 4.3 Scalability

Although the current research focuses on MobileNetV2-based transfer learning, the architecture shall remain extensible.

Future backbone architectures, datasets, evaluation metrics, and transfer learning strategies should be incorporated without significant architectural redesign.

---

## 4.4 Reproducibility

Experimental execution shall be configuration-driven.

Software behavior should depend on experiment configuration rather than hardcoded implementation.

This design improves experiment reproducibility while simplifying comparative analysis.

---

## 4.5 Separation of Responsibilities

Each architectural layer shall own a single well-defined responsibility.

Responsibilities must never overlap between independent software packages.

This objective directly supports the Single Responsibility Principle (SRP).

---

## 4.6 Research Traceability

The software architecture shall maintain direct correspondence with the research methodology presented in Chapter 3 of the thesis.

Each major stage of the methodology is represented by a dedicated software package.

This mapping simplifies software maintenance and strengthens consistency between the implementation and the written research methodology.

---

# 5. Design Philosophy

The proposed framework follows several software engineering philosophies.

These philosophies guide every architectural decision throughout the project.

---

## 5.1 Object-Oriented Programming

The framework adopts an Object-Oriented Programming (OOP) architecture.

Each software component is represented as an independent object responsible for one logical activity.

Object-oriented design improves maintainability, extensibility, and software readability.

---

## 5.2 Separation of Concerns

Different stages of the machine learning pipeline are separated into dedicated software packages.

For example,

- dataset preparation,
- preprocessing,
- model definition,
- training,
- evaluation,

are implemented independently.

Each package focuses exclusively on its assigned responsibility.

---

## 5.3 Configuration-Driven Design

Experiment behavior shall be controlled by configuration rather than source code modification.

Hyperparameters, dataset locations, experiment settings, and execution parameters should be centralized inside the configuration layer.

This approach minimizes implementation changes while improving experiment reproducibility.

---

## 5.4 Reusable Components

Reusable software components are preferred whenever possible.

Utilities, preprocessing pipelines, evaluation modules, and configuration mechanisms should remain independent from specific experiments.

This enables future research to reuse the framework with minimal modification.

---

## 5.5 Explicit Design

Software behavior should remain explicit.

Hidden dependencies, implicit initialization, and unpredictable execution flow should be avoided.

Every major software action should be directly traceable from the architecture.

---

# 6. Technology Stack

The framework is implemented using modern software technologies selected for machine learning research.

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.12 |
| Deep Learning Framework | PyTorch |
| Computer Vision Library | Torchvision |
| Development Environment | Visual Studio Code |
| Dependency Management | uv |
| Version Control | Git |
| Documentation | Markdown |
| Operating System | Windows 11 (Development Environment) |

The selected technologies prioritize compatibility, reproducibility, maintainability, and long-term research support.

---

# 7. High-Level Architecture

The proposed framework adopts a modular layered architecture in which each software component represents a distinct stage of the research workflow.

Rather than implementing the entire machine learning pipeline inside a single script, the framework separates responsibilities into multiple independent architectural layers.

Each layer communicates only with components that are necessary for accomplishing its assigned responsibility.

This architectural approach improves maintainability, simplifies debugging, and enhances software extensibility while maintaining consistency with the research methodology.

The overall execution flow is illustrated below.

```text
                    Experiment Configuration
                               │
                               ▼
                  Experiment Orchestrator (Core)
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
   Dataset Layer         Training Layer      Evaluation Layer
        │                      │                      │
        ▼                      ▼                      ▼
Preprocessing Layer      Model Layer         Experiment Outputs
```

The Experiment Orchestrator acts as the central controller responsible for coordinating the complete experiment lifecycle.

Individual layers remain independent and are responsible only for their own functionality.

---

# 8. Architectural Layers

The framework is organized into multiple architectural layers.

Each layer corresponds directly to one stage of the proposed research methodology.

## 8.1 Configuration Layer

The Configuration Layer stores all experiment parameters.

Examples include:

- dataset paths
- hyperparameters
- transfer learning strategy
- optimizer configuration
- random seed
- output directories

The configuration layer does not execute any business logic.

Its sole responsibility is to provide configuration data to other software components.

---

## 8.2 Core Layer

The Core Layer represents the entry point of the framework.

This layer is responsible for coordinating the complete experiment lifecycle.

Typical responsibilities include:

- loading experiment configuration
- initializing framework components
- controlling execution flow
- coordinating experiment stages

The Core Layer never performs model training or dataset processing directly.

---

## 8.3 Dataset Layer

The Dataset Layer provides standardized access to benchmark datasets.

Responsibilities include:

- loading datasets
- validating dataset structure
- parsing labels
- preparing dataset objects

The Dataset Layer does not perform preprocessing or model training.

---

## 8.4 Preprocessing Layer

The Preprocessing Layer applies image transformations before training or evaluation.

Typical preprocessing operations include:

- image resizing
- normalization
- data augmentation
- tensor conversion

Image preprocessing remains independent from dataset loading and model implementation.

---

## 8.5 Model Layer

The Model Layer defines the neural network architecture adopted by the research.

Responsibilities include:

- constructing the backbone model
- configuring transfer learning layers
- exposing the model interface

The Model Layer does not perform optimization or evaluation.

---

## 8.6 Training Layer

The Training Layer manages the optimization process.

Responsibilities include:

- forward propagation
- loss computation
- backward propagation
- optimizer update
- checkpoint generation
- training log generation

The Training Layer is responsible only for learning model parameters.

---

## 8.7 Evaluation Layer

The Evaluation Layer measures model performance after training has completed.

Responsibilities include:

- inference
- performance evaluation
- metric computation
- cross-dataset evaluation
- report generation

Evaluation never modifies model parameters.

---

# 9. Execution Flow

Every experiment follows the same execution sequence regardless of the selected dataset or transfer learning strategy.

The standardized execution workflow improves reproducibility while simplifying experiment management.

The execution process consists of the following stages.

1. Load experiment configuration.
2. Initialize the Experiment Orchestrator.
3. Load benchmark dataset.
4. Apply preprocessing pipeline.
5. Construct the neural network architecture.
6. Configure the transfer learning strategy.
7. Train the model.
8. Save checkpoints and training logs.
9. Evaluate the trained model.
10. Generate experiment artifacts.

The standardized execution flow ensures that every experiment follows the same software lifecycle.

---

# 10. Design Principles

The architecture follows several software engineering principles.

## Object-Oriented Programming

Each software component is represented as an independent class.

The framework favors composition over unnecessary code duplication.

---

## Single Responsibility Principle

Every package and class has one clearly defined responsibility.

Software modules should have only one reason to change.

---

## Separation of Concerns

Dataset loading, preprocessing, model definition, training, and evaluation remain independent software components.

Business logic is never shared between unrelated packages.

---

## Low Coupling

Software modules communicate through clearly defined interfaces.

Dependencies between modules are intentionally minimized.

---

## High Cohesion

Closely related responsibilities remain grouped inside the same package.

This improves readability and software maintainability.

---

## Configuration-Driven Execution

Experiment behavior is determined by configuration rather than source code modification.

Researchers should execute new experiments by changing configuration values instead of editing implementation code.

---

## Reproducible Research

The framework prioritizes deterministic experiment execution whenever possible.

Experiment configurations, random seeds, and generated artifacts should be sufficient to reproduce previous experimental results.

---

# 11. Future Extensibility

Although the current framework is developed to support the objectives of this research, the proposed software architecture is intentionally designed to accommodate future extensions.

The modular organization enables new components to be incorporated with minimal impact on existing modules.

Potential future enhancements include:

- Support for additional benchmark datasets.
- Integration of alternative backbone architectures.
- Additional transfer learning strategies.
- Hyperparameter optimization modules.
- Automated experiment scheduling.
- Model explainability and visualization.
- Experiment tracking integration.
- Distributed training support.

Future software components shall comply with the architectural principles, dependency rules, and package responsibilities defined throughout this document.

Any architectural extension should preserve modularity, maintainability, and reproducibility.

---

# 12. Architecture Decision Record (ADR)

The following architectural decision has been formally adopted for this research framework.

## AD-001

### Title

Adopt a Modular Object-Oriented Software Architecture

### Status

Accepted

### Context

The proposed research involves multiple software components, including dataset management, image preprocessing, model construction, transfer learning strategies, model training, evaluation, and experiment reporting.

Implementing these components within a monolithic codebase would significantly reduce maintainability and complicate future extensions.

A structured software architecture is therefore required to organize responsibilities while maintaining consistency with the proposed research methodology.

---

### Decision

The framework adopts a modular Object-Oriented Programming (OOP) architecture.

The implementation is divided into independent software packages.

Each package represents one stage of the machine learning experimentation pipeline and owns a clearly defined responsibility.

Dependencies between packages follow a layered architecture with strict dependency rules.

The overall experiment lifecycle is coordinated by a single Experiment Orchestrator.

---

### Rationale

The selected architecture provides several advantages.

- Improved maintainability.
- Clear separation of responsibilities.
- Better scalability.
- Easier software testing.
- Improved experiment reproducibility.
- Better alignment between software implementation and research methodology.

The architecture also simplifies future framework extensions while minimizing implementation complexity.

---

### Consequences

The adoption of this architecture introduces several implementation constraints.

- Every package shall maintain a single responsibility.
- Package dependencies shall follow the approved dependency graph.
- New functionality should extend the framework rather than modify existing modules.
- Experiment execution shall remain configuration-driven.
- Architectural changes shall be documented before implementation.

These constraints establish a consistent software engineering process throughout the research project.

---

# 13. Architecture Governance

The Software Architecture Blueprint serves as the primary architectural reference for the project.

All implementation decisions shall conform to the architectural principles defined within this document.

Changes to the software architecture are permitted only when one or more of the following conditions are satisfied.

- A significant modification to the research methodology has been approved.
- A major architectural limitation has been identified.
- A new research requirement cannot be accommodated by the existing architecture.

Minor implementation improvements that do not affect the overall architecture should not require modifications to this document.

This governance policy ensures architectural stability throughout the software development lifecycle.

---

# 14. References

The architectural design is influenced by the following software engineering principles and standards.

- Object-Oriented Programming (OOP)
- SOLID Design Principles
- Separation of Concerns (SoC)
- Clean Architecture
- IEEE 1016 Software Design Description
- Reproducible Machine Learning Research

These principles provide the conceptual foundation for the software architecture adopted in this project.

---

# 15. Revision History

| Version | Date | Description |
|----------|------------|-------------------------------------------|
| 1.0 | 2026-07-03 | Initial Software Architecture Blueprint. |

---

# Document Approval

This document has been reviewed and approved as the official Software Architecture Blueprint for the research project.

The architectural principles, design philosophy, dependency model, and software organization described within this document shall serve as the primary reference throughout the implementation phase.

Any future architectural modification shall follow the governance policy defined in Section 13.

Status: **LOCKED (Version 1.0)**

Approval Date: **2026-07-03**
