# Separating Domain State from Workflow State

## Context

AI applications often have two different kinds of state at the same time:

1. the state of the domain data;
2. the state of the process operating on that data.

While designing the room workspace for the AI Interior Designer, keeping these dimensions separate became important for both backend modeling and user experience.

## The Problem

It is tempting to use one status field to answer every question about an entity.

But these questions are different:

> What do we currently know about the room?

and:

> Where is the room in the AI workflow?

A room may already contain useful structured information while still waiting for review. It may also exist as an entity while its structured representation is incomplete.

## Design Principle

The conceptual separation is:

    Domain State
    What do we know?

            ≠

    Workflow State
    What processing stage are we in?

For example:

    Room
    ✓ exists

    Structured State
    ⚠ incomplete

    Workflow
    ● capture / processing

Or:

    Domain Data
    ✓ information available

    Workflow
    ● awaiting review

Neither example is contradictory. The values describe different dimensions.

## Why One Status Is Not Enough

If domain completeness and workflow progress are represented as the same concept, states quickly become ambiguous.

A value such as "in progress" could mean:

- data is still missing;
- AI processing is running;
- human review is pending;
- the entity exists but a downstream request has not started.

Separating these concerns gives each state a clearer meaning.

## Missing Data Is Not Automatically an Error

This distinction is especially useful in AI-assisted systems.

A missing value may mean different things:

    Unknown
    Not yet observed
    Not yet processed
    Awaiting confirmation
    Not applicable
    Failed

These states should not be invented as a universal enum for every application. The important principle is that absence of information and system failure are not necessarily equivalent.

A workflow can therefore continue to represent partial knowledge without treating every unknown field as an exception.

## Application State as Multiple Dimensions

A more useful mental model is:

    Application State
    ├── Domain State
    ├── Workflow State
    └── Interaction State

Each dimension answers a different question.

### Domain state

What facts or structured information are currently available?

### Workflow state

Which processing step is active, completed or pending?

### Interaction state

What should the user see or do next?

The interaction boundary is discussed further in [designing-human-guidance-for-ai-workflows.md](designing-human-guidance-for-ai-workflows.md).

## Why This Helps the UI

The user interface should not interpret incomplete data as a broken workflow automatically.

For example, a room can be displayed while some information is still unavailable, and the workflow can independently communicate that capture, analysis or review is still in progress.

This creates clearer feedback than collapsing all incomplete situations into an error state.

## Why This Helps the Backend

Explicit state boundaries make it easier to:

- validate transitions;
- test workflow behavior independently from domain data;
- represent partial AI results;
- handle asynchronous processing;
- avoid overloaded status fields;
- expose clearer API contracts.

The exact production state model depends on implementation needs and is intentionally not specified here.

## UI Should Follow Domain Concepts, Not Database Tables

This separation also influenced the room workspace.

The backend may contain several related entities, but users think in terms of a room and its meaningful parts rather than database tables.

A useful principle is:

> The domain model should structure the application without forcing the user to navigate the persistence model.

The room workspace can therefore present a coherent room profile while the backend maintains the normalized data structures required by the application.

## Engineering Trade-offs

Explicit state dimensions add modeling work:

- more state definitions;
- transition rules;
- synchronization between backend and frontend;
- additional test cases.

The alternative is simpler initially, but overloaded states become harder to reason about as AI processing, human review and domain persistence interact.

## What I Learned

One of the useful lessons from this project was that "state" is not one thing.

For an AI-assisted application, it can be useful to ask separately:

> What does the system know?

> What is the system currently doing?

> What should the user do next?

Those questions lead to cleaner domain, workflow and interaction boundaries.

## Public Scope

This note describes general application-state modeling principles.

The complete room domain model, detailed workflow phases, internal state transitions, entity relationships and product-specific AI decision logic remain private.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
