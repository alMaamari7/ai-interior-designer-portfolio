# Separating Current State from User Intent

## Context

While modeling the AI Interior Designer, I found that two kinds of information that look closely related should not belong to the same application state:

- what the physical room is like now;
- what the user wants the room to become.

Keeping these concepts separate became an important domain-modeling boundary.

## The Problem

A simple application could store current room information and future design preferences in one object.

That creates ambiguity:

    Room
    ├── current properties
    ├── desired properties
    ├── budget
    ├── design goals
    └── constraints

Now a change in user intent can look like a change in the physical room itself.

For an AI system that reasons about transformations, the distinction matters.

## Design Decision

The architecture separates:

    Current Room State
    "What exists now?"

            ≠

    Design Request
    "What should change?"

At a high level:

    Physical Environment
            ↓
    Structured Current State
            +
       Design Request
            ↓
         Reasoning
            ↓
      Design Solution

The current state describes the known environment. The request describes a particular design intention.

## Intent Should Not Mutate Reality

Changing a design goal should not automatically rewrite the application's representation of the real room.

For example, requesting a different future use for a room does not mean that the room has already changed.

Conceptually:

    Current State
    room type: existing use

    Design Intent
    target: new use

Both can be true at the same time.

This makes the reasoning problem explicit: transform an existing state toward an intended outcome under the applicable requirements and constraints.

## One State, Multiple Requests

Separating state from intent also allows the same room representation to support multiple design requests.

    Current Room State
           │
      ┌────┼────┐
      ↓    ↓    ↓
    Request A  Request B  Request C
      ↓        ↓          ↓
    Reasoning Reasoning  Reasoning

The physical room does not need to be conceptually recreated simply because the user wants to explore another design direction.

This turns structured room state into a reusable knowledge asset rather than a temporary intermediate result for one AI call.

## Why This Helps AI Architecture

### Cleaner inputs

The reasoning layer receives two semantically different inputs: observed/current state and desired intent.

### Reusability

One verified room representation can support multiple downstream requests.

### Better persistence

Long-lived environmental state can evolve independently from shorter-lived design intentions.

### Easier auditing

The application can distinguish whether a value describes reality or a requested future condition.

### Less accidental coupling

Editing a design request does not need to modify the source-of-truth representation of the current room.

## Relationship to Structured State

The structured current state is produced upstream from room capture, multimodal perception and review.

That boundary is described in [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md).

The reasoning layer then combines the verified state with user intent, as described in [reason-before-generating.md](reason-before-generating.md).

Together:

    Perception
        ↓
    Verified Current State
        +
    User Intent
        ↓
    Reasoning
        ↓
    Design Decision

## Engineering Trade-offs

Separating current state and intent introduces more domain objects and relationships.

It requires the application to manage:

- lifecycle differences;
- associations between state and requests;
- request-specific workflow state;
- downstream invalidation when intent changes.

The benefit is a model that more closely represents the real problem: an existing environment can have many possible future intentions.

## What I Learned

A useful domain-modeling question for AI applications is:

> Is this information describing the world, or describing what the user wants the world to become?

Treating those as separate concepts created a cleaner boundary between perception, persistence and reasoning.

## Public Scope

This note describes the general state-versus-intent architecture.

The full Digital Twin schema, complete Design Request model, domain attributes, internal relationships and product-specific reasoning rules remain private.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
