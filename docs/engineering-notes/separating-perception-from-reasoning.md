# Separating Perception from Reasoning

## Context

A multimodal AI application can ask one model to inspect an image and immediately produce a recommendation. That is attractive for a prototype, but it tightly couples visual interpretation to downstream decision-making.

For the AI Interior Designer, I chose a different architectural direction: **perception and reasoning are separate responsibilities connected through structured domain state**.

## The Problem

A direct pipeline can look like this:

    Room Images
        ↓
    Multimodal Model
        ↓
    Design Recommendation

This makes the recommendation dependent not only on the room itself, but also on the representation and behavior of the perception step.

It becomes difficult to answer:

- What did the system actually understand about the current room?
- Which information belongs to perception and which belongs to the decision?
- Can reasoning be tested without running vision again?
- Can the perception implementation change without rewriting downstream logic?

## Design Decision

The high-level architecture is:

    Room Images
        ↓
    Multimodal Perception
        ↓
    Structured Domain State
        ↓
    Reasoning
        ↓
    Design Decision

The perception layer answers a question such as:

> What is currently present in the environment?

The reasoning layer answers a different question:

> Given the current state and the user's requirements, what should change?

## Structured State as an Architectural Boundary

The structured room state acts as the contract between the two responsibilities.

    Perception
        ↓
    Structured Domain State
        ↓
    Reasoning

Downstream components therefore do not need to depend directly on raw images or the internal implementation details of the vision analysis.

This idea is discussed further in [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md).

## Domain State Instead of Perception Internals

A perception component may need technical information for its own work: model-specific responses, analysis metadata, intermediate evidence or other inference details.

Those artifacts do not automatically belong in the reasoning interface.

The intended boundary is:

    Perception Internals
            ↓
    Structured Domain State
            ↓
    Downstream Reasoning

This reduces coupling between the implementation of visual understanding and the implementation of design decisions.

## Why the Separation Helps

### Clearer responsibilities

Visual understanding and decision-making solve different problems.

### Independent testing

Reasoning can conceptually be tested against known structured room states without requiring image inference for every test.

### Replaceable perception layer

Changing a multimodal provider or improving visual analysis does not necessarily require redesigning the reasoning interface.

### Reusable state

The same verified room state can support more than one downstream request.

### Better debugging

A structured boundary makes it easier to determine whether an unexpected result originated in perception, state representation or reasoning.

## Human Review Boundary

In the broader architecture, AI-generated room information can pass through a human-review boundary before it becomes trusted application state.

Conceptually:

    Multimodal Perception
            ↓
    Proposed Structured State
            ↓
    Human Review / Confirmation
            ↓
    Verified Room State
            ↓
    Reasoning

This prevents downstream decision-making from being unnecessarily coupled to unreviewed model output.

## Engineering Trade-offs

The separation introduces additional architecture:

- structured schemas;
- state persistence;
- transformation between AI output and domain state;
- orchestration across components.

A direct image-to-answer model call is simpler.

The benefit of the additional boundary is modularity, traceability, testability and clearer ownership of information as the system grows.

## What I Learned

One of the most useful architecture questions in this project has been:

> Is this information part of what the AI observed, or part of what the application should decide?

Separating those responsibilities changed the system from a single multimodal call into a pipeline with explicit knowledge and decision boundaries.

## Public Scope

This note describes the high-level separation between perception, structured state and reasoning.

The private product contains the detailed domain specification, perception rules, reasoning contracts, prompts and decision logic. Those mechanisms are intentionally excluded from the public repository.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
