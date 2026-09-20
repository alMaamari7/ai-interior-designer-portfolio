# Entity-Level vs Scene-Level Visual Understanding

## Context

Detecting individual objects is useful, but a scene is more than a list of detected entities.

While designing the vision architecture for the AI Interior Designer, I separated two kinds of visual understanding:

> What can be understood about individual entities?

and:

> What can be understood about the scene as a whole?

## Two Levels of Understanding

At a high level:

    Visual Understanding
    │
    ├── Entity Level
    │     ├── entities
    │     └── properties
    │
    └── Scene Level
          ├── relationships
          └── global context

These levels solve different problems and can produce different forms of structured knowledge.

## Entity-Level Knowledge

Entity-level analysis focuses on identifiable elements in the visual environment.

Conceptually:

    Image Evidence
         ↓
    Entity
         ↓
    Structured Properties

The exact domain attributes are intentionally private, but the architectural role is public: turn visual observations about individual elements into structured application data.

## Scene-Level Knowledge

A room cannot be fully represented by analyzing every entity independently.

The system also needs information that only makes sense when several elements or the complete scene are considered together.

Conceptually:

    Entities
       +
    Spatial Relationships
       +
    Scene Context
       ↓
    Room-Level Understanding

This layer can describe relationships and broader characteristics without forcing them into one individual entity.

## Why Relationships Matter

Consider two representations.

The first contains only entities:

    Room
    ├── Entity A
    ├── Entity B
    └── Entity C

The second also represents relationships:

    Entity A ── relationship ──> Entity B
    Entity B ── relationship ──> Entity C

The second representation contains information about how the scene is organized, not only what is present.

That distinction matters for downstream systems that need to reason about space rather than merely count objects.

## A Scene Is More Than Object Detection

The architecture therefore moves beyond:

    Image
      ↓
    Object Labels

toward:

    Image Set
       ↓
    Multimodal Perception
       ↓
    Entity-Level Knowledge
       +
    Scene-Level Knowledge
       ↓
    Structured Scene Representation

This is closer to the information required by a domain application than a flat list of detections.

## Why Keep the Levels Separate?

### Clear ownership

Properties that belong to one entity do not need to be mixed with properties of the whole room.

### Better schemas

Different knowledge types can use contracts appropriate to their scope.

### Easier evolution

Entity analysis and scene analysis can improve independently.

### Better downstream reasoning

The reasoning layer can consume both local facts and broader context without reconstructing the entire scene from object labels.

## Structured Results

Both levels are intended to produce structured outputs rather than only prose.

At a public level, an AI-derived result may preserve:

    Structured Value
         +
    Confidence
         +
    Traceability Metadata

The exact internal schemas and evidence structures are product-specific and remain private.

The broader structured-output approach is described in [from-multimodal-perception-to-structured-domain-knowledge.md](from-multimodal-perception-to-structured-domain-knowledge.md).

## Architecture, Not an Implementation Claim

This document describes the vision architecture and responsibility boundaries.

It should not be read as a claim that every planned scene-level analysis task is already implemented in the public MVP.

The public repository contains selected real implementation for multimodal requests, structured outputs and validation, while the broader architecture continues to evolve.

## Relationship to Reasoning

Scene understanding still belongs to perception.

It describes the existing environment rather than deciding how the environment should change.

    Entity-Level Knowledge
             +
    Scene-Level Knowledge
             ↓
    Structured Current State
             ↓
         Reasoning
             ↓
       Design Decision

This preserves the boundary between understanding the world and deciding what to do with that understanding.

## Engineering Trade-offs

Separating entity-level and scene-level analysis introduces additional orchestration and schema design.

A single model call returning one description is simpler.

The separation becomes useful when the application needs:

- explicit domain state;
- relationships;
- confidence-aware information;
- persistence;
- human review;
- downstream reasoning;
- independent evolution of analysis responsibilities.

## What I Learned

A useful question in multimodal system design is:

> Does this fact belong to one object, or does it only exist because of the relationship between objects or the scene as a whole?

That question led to a cleaner separation between entity knowledge and scene knowledge.

The broader lesson is simple:

> **A scene is more than a list of detected objects.**

## Public Scope

The public repository describes the architectural distinction only.

The complete global-analysis task catalog, domain-specific attributes, evidence requirements, experience reports, interpretation strategies, aggregation rules and prompts remain private.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
