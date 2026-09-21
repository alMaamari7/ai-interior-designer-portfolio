# Reason Before Generating

## Context

Many generative AI experiences move directly from user input to generated output.

For the AI Interior Designer, I wanted the architecture to answer a different question first:

> What design decision should the system make before anything is generated?

This led to a simple principle:

> **Think before create.**

## The Problem

A direct generative flow can look like this:

    Room Image
        +
    User Prompt
        ↓
    Generation
        ↓
    Proposed Design

This can produce visually plausible results, but it leaves several responsibilities mixed together.

The same step may implicitly need to understand the existing room, interpret the user's goals, respect constraints, decide what should change and generate the result.

For a decision-oriented application, those concerns benefit from explicit boundaries.

## Design Direction

At a public architectural level:

    Current Room State
            +
    User Goals
            +
    Functional Requirements
            +
    Budget / Constraints
            ↓
    Reasoning
            ↓
    Candidate Solution
            ↓
    Evaluation
            ↓
    Design Decision
            ↓
    Generation / Presentation

Generation becomes a downstream concern rather than the place where every design decision must first emerge.

## Interior Design as a Decision Problem

The system is not only asked to create something visually attractive.

A proposed solution may also need to account for:

- the current physical state;
- user goals;
- functional requirements;
- existing elements;
- budget;
- constraints;
- spatial feasibility.

This changes the abstraction from:

    Prompt → Image

toward:

    State + Intent + Constraints
                ↓
          Decision System
                ↓
          Design Solution

The public repository describes this architecture without publishing the product-specific decision rules.

## Generate and Evaluate Are Different Responsibilities

Creating a candidate solution and evaluating whether it satisfies the problem are not the same operation.

    Candidate Solution
            ↓
        Evaluation
            ↓
    Accepted / Revised Decision

A candidate may appear plausible while still violating a requirement or failing to address the user's goals.

Making evaluation an explicit architectural responsibility creates a place to verify solution quality before downstream generation.

## Structured Decision Output

The useful result of reasoning is not only free-form prose.

At an application level, the system can produce:

    Design Decision
          +
    Structured Rationale
          +
    Evaluation Result

This supports downstream processing while making the recommendation easier to inspect and reason about at the application layer.

The term "rationale" here refers to application-level justification and evaluation information, not exposure of hidden model chain-of-thought.

## Decision vs State Transformation

A further architecture question appears after a design decision has been evaluated:

> Does the next component still make a new decision, or does it only transform an already approved decision into another structured representation?

Conceptually:

    Reasoning
        ↓
    Structured Decision
        ↓
    State Transformation?
        ↓
    Target Representation?

This boundary is currently under architectural evaluation.

One possible direction is to stop reasoning once the design decision is complete and let a separate responsibility transform that decision into a future-state representation. That could improve separation of concerns and make the decision output an explicit contract between components.

However, this is intentionally documented as a **proposal rather than a finalized implementation**. The architecture still needs to determine whether the transformation introduces additional design decisions or is purely a representation step.

A useful responsibility heuristic is:

> **If a component still decides what should happen, it belongs to decision-making. If it only materializes an already approved decision, it may deserve a separate transformation boundary.**

This question is kept explicit rather than prematurely turning an architectural option into an implementation claim.

## Why Reasoning Uses Domain State

The reasoning layer is designed to consume structured knowledge about the room rather than depend directly on raw perception internals.

    Multimodal Perception
            ↓
    Structured Room State
            ↓
    Reasoning
            ↓
    Design Decision

This boundary is described in more detail in [separating-perception-from-reasoning.md](separating-perception-from-reasoning.md).

## Why This Architecture Matters

### More explicit constraints

Requirements can become first-class inputs to decision-making rather than suggestions embedded in a generation prompt.

### Better separation of concerns

Understanding the environment, deciding what should change and presenting the result can evolve independently.

### Testable decision behavior

Structured inputs and outputs make it easier to test the reasoning boundary without requiring the entire visual pipeline.

### Multiple downstream representations

A design decision can potentially support different downstream representations instead of being tied immediately to one generated image.

## Engineering Trade-offs

A staged decision architecture is more complex than direct generation.

It requires:

- structured state;
- explicit requirements;
- reasoning orchestration;
- solution representation;
- evaluation boundaries;
- additional schemas and tests.

For a lightweight image-generation demo, this may be unnecessary.

For an AI system intended to support explainable, constraint-aware decisions, the additional structure provides a stronger foundation.

## What I Learned

Generative AI made it easy to think of the generated artifact as the product of the model.

Building this system pushed me toward a different view:

> The generated artifact should represent a decision the system has already reasoned about.

That makes generation one component of a larger AI decision system rather than the entire application.

## Public Scope

This note intentionally describes only the public reasoning architecture.

The private product contains the detailed internal reasoning decomposition, phase-specific inputs and outputs, domain rules, prioritization, conflict handling, evaluation policies, prompts and other product-specific decision logic.

The public portfolio demonstrates the engineering principle without exposing that proprietary reasoning intelligence.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
