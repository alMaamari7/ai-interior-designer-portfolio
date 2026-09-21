# Persisting AI-Derived State for Downstream Reuse

## Context

Many AI integrations treat model output as ephemeral:

    Input
      ↓
    AI Model
      ↓
    Response
      ↓
    Display
      ↓
    Gone

That is appropriate for some tasks, but not for every AI application.

In the AI Interior Designer, visual perception produces structured information about the current room. Once that information has been validated and confirmed, it can become reusable application state rather than being recomputed for every downstream request.

> Not every AI result should disappear after the response. Some AI outputs are better treated as reusable application state.

## From Inference Result to Persistent Knowledge

At a high level:

    Raw Visual Input
          ↓
    Multimodal Perception
          ↓
    Structured AI Result
          ↓
    Validation / Review
          ↓
    Verified Current State
          ↓
       Persistence
          ↓
      ┌───┼───┐
      ↓   ↓   ↓
    Task A B   C

The expensive perception step creates a structured representation that can support multiple later operations.

The downstream application does not need to reinterpret the original images every time the user creates a new request.

## Different Data Has Different Lifecycles

A useful domain-modeling distinction is between long-lived state, request-specific intent and derived results.

    Current Room State
          ↓
       long-lived

    Design Request
          ↓
    request-specific

    Recommendation
          ↓
      derived result

These concepts should not be collapsed into one mutable AI state object.

Changing what the user wants should not automatically rewrite what the application currently knows about the physical room.

This separation is discussed further in [separating-current-state-from-user-intent.md](separating-current-state-from-user-intent.md).

## One State, Multiple Downstream Requests

The reusable-state model enables:

                     ┌→ Design Request A → Result A
                     │
    Verified State ──┼→ Design Request B → Result B
                     │
                     └→ Design Request C → Result C

The current room representation remains the common source of contextual knowledge while each request can express a different desired outcome.

This is useful when the same physical environment should support multiple independent AI tasks.

## Why Not Repeat Perception?

Without persistence, the architecture could repeatedly perform the same expensive work:

    Images → Perception → Task A
    Images → Perception → Task B
    Images → Perception → Task C

That introduces several problems.

### Redundant inference

The same source material may be processed repeatedly even though the physical state has not changed.

### Potential inconsistency

Independent perception runs can produce slightly different interpretations of the same environment.

### Additional latency and cost

Repeated multimodal inference adds unnecessary processing.

### More complicated downstream behavior

Every request must reconstruct its own understanding of the current environment.

Persisting a verified representation changes the pattern:

    Images
      ↓
    Perception
      ↓
    Verified Structured State
      ↓
    Persistence
      ↓
    Multiple Downstream Tasks

## AI Output as Application State

Persisting AI-derived information requires a clear boundary between a raw model response and trusted application state.

Conceptually:

    Model Output
        ↓
    Schema Validation
        ↓
    Review / Confirmation
        ↓
    Trusted State
        ↓
    Persistence

The model response itself is not automatically the source of truth.

The application decides when AI-derived information has reached the state required for downstream use.

This complements the architecture described in [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md).

## Persistence Improves Testability

Once downstream components depend on structured persisted state rather than live multimodal inference, they can be tested independently.

For example:

    Known Room State
          +
    Known User Request
          ↓
    Downstream Service

Tests no longer need to invoke the perception model merely to prepare the input for another component.

This makes responsibility boundaries clearer and reduces coupling between AI stages.

## Persistence Also Creates New Problems

Persistent AI-derived state is not automatically correct forever.

The real environment can change:

    Physical Environment
          ↓
        changes
          ↓
    Persisted Representation
          ↓
       may be stale

This creates important architecture questions:

- When should persisted state be considered stale?
- What event should trigger a refresh?
- Which derived results depend on changed state?
- Which source is authoritative when information conflicts?
- How should updates be versioned or audited?

The public project does not claim to have finalized all of these policies.

They are explicit design considerations created by treating AI output as durable application state.

## Source-of-Truth Boundaries

A stateful AI system benefits from distinguishing between:

    Raw Input
        ↓
    AI-Derived Candidate Information
        ↓
    Reviewed / Verified Information
        ↓
    Persisted Application State
        ↓
    Derived Decisions

This prevents downstream decisions from being confused with observations about the current environment.

It also makes it clearer which information can be reused and which information belongs only to one request.

## Relationship to AI Orchestration

Persistence is part of orchestration rather than an isolated database concern.

The orchestrator must know whether a downstream stage can consume existing state or whether new processing is required.

At a high level:

    Request
      ↓
    Reusable State Available?
       /              \
     yes              no
      ↓                ↓
    Reuse          Acquire / Process
      \                /
       ↓              ↓
       Downstream Task

The exact product-specific refresh and invalidation policies are intentionally outside the public scope.

The broader orchestration design is described in [orchestrating-a-multistage-ai-application.md](orchestrating-a-multistage-ai-application.md).

## Engineering Benefits

Treating selected AI outputs as persistent structured state can provide:

- reuse across multiple downstream requests;
- reduced redundant inference;
- more consistent context;
- clearer domain boundaries;
- easier testing;
- better observability;
- lower coupling between perception and reasoning;
- a stable integration contract for future components.

## Engineering Trade-offs

The approach also introduces:

- state synchronization concerns;
- stale-data risk;
- schema evolution;
- invalidation questions;
- persistence and migration requirements;
- more explicit source-of-truth decisions.

The architecture therefore trades a simpler stateless flow for a more reusable stateful system.

## What I Learned

One of the useful distinctions in AI software engineering is between:

> an AI response

and:

> AI-derived application state.

The first can be temporary.

The second has a lifecycle, ownership, validation requirements and downstream dependencies.

Once AI output becomes application state, database design, domain modeling, versioning, validation and orchestration become part of the AI architecture.

## Related Engineering Notes

- [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md)
- [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md)
- [separating-current-state-from-user-intent.md](separating-current-state-from-user-intent.md)
- [separating-domain-state-from-workflow-state.md](separating-domain-state-from-workflow-state.md)
- [orchestrating-a-multistage-ai-application.md](orchestrating-a-multistage-ai-application.md)

## Public Scope

This note describes the architectural principle of persisting and reusing verified AI-derived state.

The complete Digital Twin schema, exact database relationships, detailed Design Request structure, proprietary reasoning and recommendation logic, refresh/invalidation policies and internal decision rules are intentionally excluded.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
