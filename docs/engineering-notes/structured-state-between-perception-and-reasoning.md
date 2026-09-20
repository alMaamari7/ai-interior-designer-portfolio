# Why I Put Structured State Between Perception and Reasoning

## Context

While designing the AI Interior Designer, I needed a clean boundary between two different responsibilities:

- understanding the current room from visual information; and
- deciding what should change based on user goals and constraints.

Passing raw images or loosely structured model responses directly into every downstream AI component would couple perception and decision-making too tightly.

The architectural decision was to introduce a structured representation of the **current room state** between these stages.

```text
Room Images
    ↓
Multimodal Perception
    ↓
Structured Current State
    ↓
Human Review / Confirmation
    ↓
Verified Room State
    ↓
Downstream AI Components
```

## The Problem

Multimodal models are useful for extracting information from images, but their output should not automatically become the application's shared state.

A larger AI system needs information that can be:

- validated against explicit schemas;
- persisted independently of a model call;
- reviewed or corrected;
- reused by multiple downstream components;
- tested through stable software contracts.

Without that boundary, downstream logic can become dependent on raw images, provider-specific responses or repeated interpretation of the same visual information.

## Design Decision

The vision layer is responsible for **perception**.

It transforms available visual information into a structured description of the existing room.

The structured state then becomes the interface between perception and later processing:

```text
Perception
    ↓
Structured Knowledge
    ↓
Decision Support
```

This means downstream reasoning does not need to perform room recognition again. It can work from an explicit representation of what is currently known about the room.

## What the Structured State Represents

At a public architectural level, the representation can contain:

- room entities;
- relevant properties of those entities;
- relationships between elements;
- room-level context produced by visual analysis.

The production project contains a substantially richer domain model. The complete schema and domain-specific intelligence are intentionally not published in this portfolio.

## Current State vs. User Intent

Another important boundary is the separation between the **existing room** and the **requested future change**.

```text
Verified Current Room State
            +
       Design Request
            ↓
     Decision Support
```

The current state answers:

> What exists now?

The Design Request answers:

> What does the user want to achieve?

Keeping these concepts separate means the same room representation can support different future design requests without redefining the physical room every time.

## Why This Separation Matters

It improves **reuse**, because structured room knowledge can support later application components; **modularity**, because perception and reasoning can evolve behind stable contracts; **persistence**, because the state exists beyond one model request; **human review**, because AI-generated information can be corrected before becoming trusted state; **testability**, because typed boundaries can be tested without live inference; and **provider isolation**, because application logic does not depend directly on one model provider's response format.

## Engineering Trade-offs

Introducing an explicit knowledge layer also adds engineering work: schema and domain modeling, validation, persistence, synchronization between AI-generated and confirmed information, and handling uncertain or incomplete observations.

For a small prototype, passing one model response directly into another prompt may be faster. For a system with multiple AI responsibilities, the structured boundary makes responsibilities easier to reason about, test and evolve.

## Public Implementation

The public repository demonstrates selected parts of this architecture:

- `backend/app/ai/public_outputs.py` — reduced typed output contracts for AI-generated observations;
- `backend/app/services/vision_analysis.py` — orchestration from accepted image input to structured analysis;
- `backend/app/models/ai_analysis.py` — persistence boundary for AI-generated analysis;
- `backend/app/models/confirmed_ai_analysis.py` — separate persistence for reviewed information;
- `backend/app/services/analysis_review.py` — public human-review boundary.

Together these components demonstrate the engineering pattern without exposing the complete production Digital Twin.

## What I Learned

One of the most important design questions in an AI application is not only:

> Which model should perform this task?

It is also:

> What information should cross the boundary between AI components?

For this project, separating perception, structured knowledge and decision support created a clearer architecture than treating the multimodal model response itself as the application state.

## Public Scope

This note describes the architecture principle, not the proprietary implementation.

Intentionally excluded are:

- the complete production Digital Twin schema;
- the complete domain specification;
- internal AI-specific attributes;
- detailed relationship and evidence structures;
- evidence/readiness and capture-decision rules;
- internal validation policies;
- detailed reasoning contracts and decision policies.

The public repository demonstrates the engineering boundary while the full product-specific intelligence remains private.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
