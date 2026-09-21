# Orchestrating a Multi-Stage AI Application

## Context

An AI application is not the same thing as an API call to an AI model.

While designing the AI Interior Designer, the system evolved into a set of specialized processing stages that combine deterministic software, multimodal perception, structured application state, human interaction and AI reasoning.

The important engineering problem became not only:

> Which model should perform this task?

but also:

> Which component should run, with which input, at which point in the workflow, and what state should it produce for the next component?

That is an orchestration problem.

## From Model Call to AI System

A minimal AI integration might look like:

    Images + Prompt
          ↓
      AI Model
          ↓
    Recommendation

That is useful for experimentation, but it tightly couples perception, interpretation and decision-making.

The broader architecture instead separates responsibilities:

    Input Acquisition
           ↓
    Deterministic Quality Gates
           ↓
    Multimodal Perception
           ↓
    Structured Domain State
           ↓
    Human Verification
           ↓
    User Intent
           ↓
    AI Reasoning
           ↓
    Decision / Recommendation
           ↓
    Presentation

Not every box needs to be an AI model. The application combines probabilistic and deterministic components according to the responsibility being solved.

## Specialized Responsibilities

Different stages answer different questions.

### Input acquisition

What information has the user provided?

### Technical validation

Is the input technically usable?

### Perception

What can be understood about the existing environment?

### Structured state

How should that understanding be represented for the application?

### Human verification

Which AI-derived information has been reviewed or confirmed?

### User intent

What does the user want to achieve?

### Reasoning

What follows from the current state, goals and constraints?

### Decision and recommendation

What solution should the application propose?

### Presentation

How should the result be communicated or visualized?

This avoids placing unrelated responsibilities inside one large prompt.

## Structured State as a Contract Between Stages

AI stages should not need to communicate only through free-form prose.

A more explicit architecture is:

    Perception
        ↓
    Structured State
        ↓
    Reasoning
        ↓
    Structured Decision
        ↓
    Downstream Processing

Structured state becomes an application-level contract.

This provides several advantages:

- components can evolve independently;
- downstream services can be tested without live upstream inference;
- model-provider details remain localized;
- state can be persisted and reviewed;
- failures can be isolated more easily;
- AI results can be reused across requests.

The perception-to-state boundary is discussed in [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md).

## Deterministic and Probabilistic Components Should Coexist

An AI system does not benefit from using AI for every operation.

For example:

    Image Upload
         ↓
    Deterministic Technical Validation
         ↓
    Multimodal Semantic Analysis

Technical checks such as file integrity, image dimensions or measurable sharpness can be handled with ordinary software and computer vision.

Semantic interpretation belongs to the multimodal layer.

The corresponding quality-gate design is described in [deterministic-image-quality-before-multimodal-ai.md](deterministic-image-quality-before-multimodal-ai.md).

A useful principle is:

> Use AI where probabilistic semantic inference adds value and deterministic software where deterministic behavior is sufficient.

## Human Review as a State Transition

Human-in-the-loop behavior is more useful when it is part of the workflow architecture rather than an isolated UI feature.

Conceptually:

    AI Inference
        ↓
    Candidate State
        ↓
    Human Review
        ↓
    Confirmed State
        ↓
    Downstream Processing

This makes the trust boundary explicit.

The downstream reasoning layer can depend on reviewed application state rather than treating every raw model output as confirmed reality.

## AI Workflows Are Not Always Linear

A multi-stage AI application may contain feedback loops.

At a public architectural level:

    Processing
        ↓
    State Evaluation
        ↓
     ┌───────────────┐
     ↓               ↓
    Ready       More Input Needed
     ↓               ↓
    Continue       User Action
                     ↓
                  Re-evaluate

This is particularly relevant when input quality or information availability cannot be guaranteed in advance.

The exact product-specific evidence and capture decision rules remain private. The public adaptive-capture principle is described in [adaptive-capture-for-multimodal-ai.md](adaptive-capture-for-multimodal-ai.md).

## Orchestration Belongs to the Application

A large prompt can hide workflow logic inside model instructions.

That may be convenient initially, but it makes important application behavior harder to inspect, test and evolve.

Instead, the application should own decisions such as:

- which stage runs next;
- which structured input is passed to it;
- whether deterministic validation is required first;
- whether user interaction is needed;
- which state is persisted;
- which downstream component receives the result.

AI models then operate inside explicit responsibility boundaries.

## Perception and Reasoning Remain Separate

The system also maintains a semantic boundary between understanding the current environment and deciding what should change.

    Visual Input
        ↓
    Perception
        ↓
    Current State
        +
    User Intent
        ↓
    Reasoning
        ↓
    Decision

This separation is discussed in [separating-perception-from-reasoning.md](separating-perception-from-reasoning.md).

The reasoning architecture itself is intentionally documented only at a high level in [reason-before-generating.md](reason-before-generating.md).

## Why This Architecture Helps

### Testability

Individual services and transitions can be tested with controlled inputs.

### Observability

Failures can be associated with a particular processing responsibility rather than one opaque AI call.

### Replaceability

A model or provider can change without forcing every downstream component to understand the new provider response.

### Human control

Review and correction become explicit workflow states.

### Cost control

Deterministic checks can reject unusable input before expensive inference.

### Reusability

Structured state can support multiple downstream AI tasks and user requests.

### Maintainability

Responsibilities remain visible in application architecture rather than being embedded in a growing prompt.

## Engineering Trade-offs

Orchestration adds complexity.

A multi-stage architecture requires:

- explicit schemas;
- state management;
- service boundaries;
- transition handling;
- failure and retry behavior;
- additional tests;
- careful ownership of responsibilities.

For a small prototype, a single model call may be faster to build.

The additional structure becomes valuable when the AI feature needs to become a maintainable software system rather than remain an isolated experiment.

## What I Learned

The project changed how I think about AI engineering.

The model is only one component.

The application around the model determines how inputs are validated, how probabilistic outputs become structured state, where humans can intervene, how different AI responsibilities are separated and how downstream decisions are made.

A useful summary is:

> **AI engineering is not only model integration. It is the orchestration of models, deterministic software, state and human interaction into a reliable application workflow.**

## Related Engineering Notes

- [deterministic-image-quality-before-multimodal-ai.md](deterministic-image-quality-before-multimodal-ai.md)
- [adaptive-capture-for-multimodal-ai.md](adaptive-capture-for-multimodal-ai.md)
- [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md)
- [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md)
- [separating-perception-from-reasoning.md](separating-perception-from-reasoning.md)
- [separating-current-state-from-user-intent.md](separating-current-state-from-user-intent.md)
- [designing-human-guidance-for-ai-workflows.md](designing-human-guidance-for-ai-workflows.md)
- [reason-before-generating.md](reason-before-generating.md)

## Public Scope

This note describes the high-level orchestration architecture.

The exact reasoning decomposition, phase contracts, evidence/readiness logic, capture recommendation rules, private domain specifications, detailed decision policies and production prompts are intentionally excluded.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
