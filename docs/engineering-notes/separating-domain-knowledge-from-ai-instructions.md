# Separating Domain Knowledge from AI Instructions

## Context

While designing higher-level analysis for the AI Interior Designer, I ran into an architecture question that becomes increasingly important as AI systems grow:

> Where should domain knowledge live?

A prompt can contain task instructions, examples, domain definitions, output requirements and decision guidance. That is convenient at the beginning, but it can also turn the prompt into a tightly coupled knowledge base.

I started treating these concerns as separate architectural responsibilities rather than one large prompt.

> **Note:** This document describes an architecture direction explored during development. It should not be read as a claim that every described separation is already implemented in the public portfolio.

## The Problem

A domain model can define **what information exists** without fully defining **how an AI component should interpret domain concepts**.

At the same time, putting all interpretation knowledge directly into task prompts creates another problem:

```text
Prompt
 ├── Task instructions
 ├── Domain definitions
 ├── Interpretation knowledge
 ├── Output requirements
 └── Application-specific rules
```

As the system evolves, these responsibilities become harder to change independently.

The issue is therefore not simply how to write a better prompt. It is how to structure knowledge and responsibilities around the model.

## Design Direction

A useful separation is to think in terms of distinct inputs to an AI task:

```text
Runtime Data ───────────┐
                        │
Domain Knowledge ───────┼──→ AI Task
                        │
Task Instructions ──────┤
                        │
Output Contract ────────┘
```

Each answers a different question.

### Runtime Data

What does the system know about this specific case right now?

For the AI Interior Designer, that can include structured information about the current room.

### Domain Knowledge

How should relevant concepts in the problem domain be understood?

This is knowledge that may be reused across multiple executions rather than recreated for every request.

### Task Instructions

What responsibility should the AI perform in this specific processing step?

The instruction should describe the task instead of becoming the only place where all domain knowledge lives.

### Output Contract

What structured result must cross the boundary back into deterministic application code?

Typed output contracts make this responsibility explicit.

## Why This Matters

### Separation of concerns

Changing task instructions should not necessarily require redefining the domain model or rewriting all domain knowledge.

### Maintainability

Smaller responsibilities are easier to inspect and evolve than a single prompt containing the complete application logic.

### Reuse

Domain knowledge can potentially support more than one AI task instead of being duplicated across prompt templates.

### Testability

Explicit inputs and outputs create clearer boundaries for testing orchestration around probabilistic model behavior.

### Model flexibility

When application responsibilities are separated from provider-specific prompting, replacing or comparing models becomes easier.

## Example in This Project

The public repository already demonstrates some of these boundaries:

```text
Image + Context
      ↓
Application Service
      ↓
AI Request
 ├── instruction
 ├── context
 ├── image data
 └── output schema
      ↓
Multimodal Model
      ↓
Schema-constrained Result
      ↓
Pydantic Validation
```

The production project contains richer domain knowledge and analysis specifications than the reduced public example.

Those private specifications are deliberately not published here.

## Domain Model Is Not Domain Knowledge

One useful distinction from this architecture work is:

> A data model describes the information the application can represent. It does not automatically contain all knowledge required to interpret that information.

For example, defining a structured field tells the application that a concept exists and how it should be represented. It does not necessarily define every domain rule required for an AI system to derive or evaluate that concept.

Keeping this distinction explicit helps prevent persistence models, prompts and domain intelligence from becoming one tightly coupled layer.

## Engineering Trade-offs

Separating these responsibilities introduces additional architecture:

- more explicit interfaces;
- versioning considerations;
- coordination between knowledge and output schemas;
- more components to maintain.

For a small experiment, a single prompt may be entirely appropriate.

The separation becomes more valuable when the system contains multiple AI responsibilities, shared domain concepts, persistent application state and independently evolving components.

## What I Learned

A recurring lesson from building this project is that AI engineering decisions often happen **around** the model.

The question is not only:

> What should I tell the model?

It is also:

> Which knowledge belongs to the prompt, which belongs to the domain layer, which belongs to runtime state, and which should be enforced by application code?

That distinction becomes increasingly important as an AI prototype develops into a larger software system.

## Content Angles

This engineering decision can support several public discussions without exposing the private implementation:

- **Technical Insight:** Why prompts should not become the domain knowledge base.
- **Build:** An architecture problem discovered while designing higher-level multimodal analysis.
- **Problem / Solution:** Separating runtime data, reusable domain knowledge, task instructions and output contracts.
- **Learning:** Moving from prompt-centric prototypes toward explicit AI-system architecture.

## Public Scope

This note intentionally discusses the architecture principle rather than the product-specific knowledge.

Not published here:

- the complete domain AI specification;
- detailed global-analysis definitions;
- domain-specific interpretation rules;
- evidence specifications;
- scoring or evaluation logic;
- production prompts and prompt chains;
- internal reasoning policies;
- proprietary decision rules.

The goal of the public portfolio is to demonstrate the engineering decision without making the private intelligence reconstructable.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
