# Project Overview

## Purpose

AI Interior Designer explores how multimodal AI can support interior-design decisions for an existing real-world room.

Instead of generating a design directly from one image, the system first builds a structured understanding of the current room. This room state can then be combined with user requirements, budget and constraints to support downstream reasoning and design recommendations.

The public portfolio focuses on the engineering architecture behind this approach. Product-specific decision intelligence remains private.

## Problem

Interior-design decisions depend on more than visual style. A useful solution has to account for the existing room, spatial limitations, furniture and architectural elements, intended use, user goals, budget and constraints.

A direct image-to-design workflow makes these concerns difficult to represent explicitly and reuse across multiple design requests.

The project therefore treats the problem as a sequence of separate responsibilities:

```text
Capture the real room
        ↓
Understand visual information
        ↓
Represent the current room as structured knowledge
        ↓
Review / confirm AI-generated information
        ↓
Combine room state with a Design Request
        ↓
Reason about possible changes
        ↓
Evaluate and present a design recommendation
```

## Core system idea

The central architectural principle is:

> **Perceive and structure the current state before reasoning about the target state.**

This creates a boundary between three major concerns.

### 1. Perception

Room images and user-provided context are processed to extract structured information about the existing room.

The public implementation demonstrates part of this path through:

```text
Image Upload
    ↓
Technical Image Quality
    ↓
Multimodal Vision Model
    ↓
Schema-constrained Output
    ↓
Structured Room Analysis
```

### 2. Structured room state

Visual analysis is converted into a structured representation of the current room.

In the complete project this representation acts as a Digital Twin / shared knowledge layer for downstream processing. The full production schema is intentionally not published.

### 3. Decision support

A Design Request describes what the user wants to achieve. At a high level it can contain goals, functional requirements, budget and constraints.

The reasoning layer combines this request with the verified current room state and develops an evaluated design solution.

The private decision policies, reasoning contracts and domain rules are not part of this repository.

## Why separate the current room from the Design Request?

The existing room is relatively persistent, while design intentions can change.

```text
Verified Room State
      │
      ├── Design Request A
      │       └── Recommendation A
      │
      ├── Design Request B
      │       └── Recommendation B
      │
      └── Design Request C
              └── Recommendation C
```

This allows the same structured room state to support multiple redesign scenarios without requiring the room to be captured again for every request.

## High-level workflow

```text
Create & Capture Room
        ↓
Vision Analysis
        ↓
Structured Current Room State
        ↓
Human Review / Confirmation
        ↓
Verified Room State
        +
Design Request
        ↓
AI Reasoning / Decision Support
        ↓
Evaluated Solution
        ↓
Recommendation
```

The complete private project contains additional workflow logic around capture, evidence assessment and domain-specific reasoning. Those mechanisms are intentionally abstracted here.

## Adaptive capture

Room capture is designed as more than a fixed image-upload form.

At a public architectural level, the workflow can evaluate whether the available visual information is sufficient for downstream analysis and request additional views when necessary.

```text
Capture
   ↓
Technical Quality
   ↓
Visual Analysis
   ↓
Is enough relevant visual information available?
   │
   ├── Yes → continue
   │
   └── No  → request additional capture
                    ↓
                re-analyze
```

The concrete evidence requirements, sufficiency rules, gap-diagnosis mechanisms and capture-selection policies are proprietary and therefore excluded.

## Vision architecture

The vision layer converts captured visual information into structured domain knowledge.

Conceptually, it handles both:

- information about individual room elements; and
- room-level context and relationships.

Downstream components work with the resulting structured room state rather than repeatedly reasoning over the original images.

The public repository deliberately uses a reduced output model so that this engineering boundary can be inspected without publishing the full private knowledge model.

## Human-in-the-loop

AI-generated room information is treated as a proposal rather than unquestioned ground truth.

The architecture separates an AI analysis from its human-reviewed or corrected version:

```text
AI Analysis
     ↓
Review / Correction
     ↓
Confirmed Analysis
     ↓
Trusted downstream state
```

Selected SQLAlchemy models, API contracts and tests for this boundary are included in the repository.

## Reasoning and decision support

The reasoning layer is separated from visual perception.

Its responsibility is not to answer *what is visible in the image*, but to use structured room knowledge together with the Design Request to determine what changes could satisfy the user's goals and constraints.

Publicly, this can be summarized as:

```text
Verified Room State
        +
User Goals
        +
Budget
        +
Constraints
        ↓
Reasoning / Decision Support
        ↓
Candidate Solution
        ↓
Evaluation
        ↓
Recommendation
```

The detailed reasoning stages, prompts, prioritization logic, conflict-resolution policies, evaluation criteria and optimization rules remain private.

## Engineering architecture

The project uses explicit software boundaries for API, application services, AI integration, schemas and persistence.

Current public technologies include:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL-oriented persistence
- OpenCV
- Pillow
- NumPy
- Google Gemini multimodal API
- pytest
- GitHub Actions

## Public portfolio vs. private product

This repository is not intended to reproduce the complete private application.

It is a curated engineering portfolio that publishes enough real implementation to demonstrate:

- multimodal AI integration;
- computer-vision preprocessing;
- structured outputs;
- backend/API engineering;
- domain modeling;
- persistence;
- human-in-the-loop architecture;
- AI orchestration;
- automated testing and CI.

The following remain private:

- production prompts and prompt chains;
- complete Digital Twin / Domain AI Specification;
- detailed visual-evidence requirements;
- evidence sufficiency and readiness rules;
- evidence-gap diagnosis;
- targeted capture decision logic;
- detailed reasoning stages and contracts;
- prioritization and conflict-resolution logic;
- evaluation and optimization policies.

See [ip-boundary.md](ip-boundary.md) for the repository's disclosure policy.
