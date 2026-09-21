# Separating AI Evidence from Domain State

## Context

A multimodal AI system can produce many useful intermediate signals, but not every AI-derived result belongs in the application's persistent domain model.

While designing the AI domain architecture for the AI Interior Designer, an important distinction emerged:

> AI-derived information and domain state serve different responsibilities.

The domain model should represent information that has lasting business meaning. Intermediate AI knowledge can support the creation of that state without becoming domain state itself.

## Three Different Layers

At a high level, the architecture distinguishes:

    Model Internals
          ↓
    AI-Derived Information
          ↓
    Domain Knowledge
          ↓
    Application Decisions

These layers should not be treated as interchangeable.

### Model internals

Provider- or model-specific representations used internally by an AI system.

### AI-derived information

Application-relevant observations or intermediate knowledge produced through AI processing.

### Domain knowledge

Information with explicit meaning in the application's business domain and lifecycle.

This distinction helps prevent the domain model from becoming a mirror of one particular AI provider or model implementation.

## Not Every AI Result Belongs in the Domain Model

A tempting design is:

    AI produces something
           ↓
    store it in the domain model

That can create unnecessary coupling.

Instead:

    AI Processing
          ↓
    Intermediate AI Knowledge
          ↓
    Domain Interpretation
          ↓
    Structured Domain State

Intermediate information can contribute to a domain value without becoming a first-class persistent domain attribute itself.

A useful rule is:

> **Persist business meaning, not every intermediate AI signal.**

## AI Evidence Should Be Model-Independent

Application architecture should not depend unnecessarily on representations such as:

- tensors;
- model activations;
- provider-specific response structures;
- internal embeddings;
- other implementation details of a particular model.

Those representations may be useful inside an AI implementation, but they are poor contracts for the wider application.

The application instead benefits from model-independent AI-derived information that expresses what was learned in terms meaningful to the system.

Conceptually:

    Provider-Specific Model
            ↓
    Provider Adapter / AI Layer
            ↓
    Model-Independent AI Information
            ↓
    Domain Mapping
            ↓
    Domain State

This creates a cleaner provider boundary.

## AI Tasks Need Information Contracts

An AI task should not simply receive whatever context happens to be available.

At an architectural level, a task can have an explicit contract:

    AI Task
    ├── allowed inputs
    ├── required dependencies
    └── structured result

The distinction matters:

### Inputs

Information the task is allowed to use.

### Dependencies

Information that must already exist before the task can run correctly.

### Result

Structured information produced by the task.

This makes orchestration more explicit and reduces hidden dependencies inside prompts.

The exact product-specific task contracts remain private.

## Traceability from AI Information to Domain State

Separating intermediate AI information from persistent domain knowledge does not mean losing the relationship between them.

The architecture can preserve application-level traceability:

    Source Input
         ↓
    AI Processing
         ↓
    AI-Derived Information
         ↓
    Domain State
         ↓
    Downstream Usage

This allows the system design to answer questions such as:

- where did a domain value originate?
- what kind of AI-derived information contributed to it?
- which downstream components depend on the resulting domain state?

This is application-level traceability. It is not an attempt to expose hidden model chain-of-thought.

## Different Information Has Different Lifecycles

Intermediate AI knowledge and domain state can also have different lifecycles.

    AI-Derived Information
          ↓
    supports interpretation
          ↓
    Domain State
          ↓
    review / persistence / reuse
          ↓
    Downstream Systems

Some intermediate information may exist only during AI processing.

Domain information, by contrast, can become part of the persistent representation of the current environment and be reused by later components.

This complements the persistence principles described in [persisting-ai-derived-state-for-downstream-reuse.md](persisting-ai-derived-state-for-downstream-reuse.md).

## Confidence Is Metadata, Not the Domain Meaning Itself

AI-derived information can carry confidence or uncertainty metadata.

Conceptually:

    AI-Derived Result
        ├── value
        └── confidence metadata

The domain architecture can preserve such metadata where useful without confusing it with the semantic meaning of the domain value.

How confidence affects acceptance, review, recapture or other workflow decisions is product-specific policy and is intentionally outside the public scope.

## Why This Separation Helps

### Provider independence

Domain concepts do not need to change because an AI provider changes its internal representation.

### Maintainability

AI implementation details remain inside the AI layer instead of spreading through business models.

### Testability

Domain behavior can be tested with known structured state without reproducing model internals.

### Traceability

The relationship between AI-derived information and persistent domain knowledge can remain explicit.

### Reuse

Intermediate AI information can support more than one downstream interpretation without duplicating model calls unnecessarily.

### Clearer ownership

The architecture can distinguish what belongs to perception, what belongs to the domain and what belongs to downstream reasoning.

## Relationship to Structured Perception

The broader perception pipeline is described in [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md).

Together, the concepts form:

    Visual Input
         ↓
    Multimodal Perception
         ↓
    Structured AI-Derived Information
         ↓
    Domain Mapping
         ↓
    Structured Current State

The current-state representation can then be reviewed, persisted and reused by downstream AI components.

## Relationship to Domain Knowledge and Prompts

Domain knowledge should also remain distinct from task instructions.

A prompt may tell a model what to do, but it should not become the only place where the application's domain semantics live.

That separation is discussed in [separating-domain-knowledge-from-ai-instructions.md](separating-domain-knowledge-from-ai-instructions.md).

Combined:

    Domain Semantics
         +
    AI Task Contract
         +
    Runtime Input
         ↓
    AI Processing
         ↓
    Structured AI Information
         ↓
    Domain State

## Engineering Trade-offs

Introducing an intermediate AI-information layer adds architectural work.

It requires:

- explicit schemas;
- mapping between AI results and domain state;
- lifecycle decisions;
- traceability boundaries;
- careful ownership of confidence metadata;
- versioning when contracts evolve.

For a small prototype, storing model output directly may be simpler.

The separation becomes more valuable when the AI system must remain maintainable as providers, prompts, models and downstream features evolve.

## What I Learned

A useful AI-engineering question is not only:

> What should the model return?

It is also:

> Which parts of that result have lasting domain meaning, and which parts exist only to help the AI system derive that meaning?

That distinction prevents AI implementation details from becoming accidental business concepts.

The resulting principle is:

> **Not every AI output belongs in the domain model.**

## Related Engineering Notes

- [separating-domain-knowledge-from-ai-instructions.md](separating-domain-knowledge-from-ai-instructions.md)
- [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md)
- [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md)
- [persisting-ai-derived-state-for-downstream-reuse.md](persisting-ai-derived-state-for-downstream-reuse.md)
- [orchestrating-a-multistage-ai-application.md](orchestrating-a-multistage-ai-application.md)

## Public Scope

This note describes the architectural separation between model internals, AI-derived intermediate information and persistent domain state.

The complete Domain AI Specification, concrete domain attributes, AI-evidence catalog, evidence-to-attribute mappings, attribute-specific AI inputs and dependencies, image requirements, confidence thresholds, evidence weightings, aggregate confidence calculations, validation policies, review policies and workflow decision rules are intentionally excluded.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
