# From Multimodal Perception to Structured Domain Knowledge

## Context

A multimodal model can describe an image in natural language, but free-form text is a weak interface for the rest of an application.

For the AI Interior Designer, the vision layer is designed around a different goal:

> Transform visual information into structured domain knowledge that downstream software can validate, persist and reuse.

## The Problem with Free-Form Vision Output

A simple integration can look like this:

    Room Images
        ↓
    Multimodal Model
        ↓
    Free-Form Description

That may be useful for a demo, but downstream components then need to interpret prose before they can use the result.

It also makes validation, persistence, testing and human review harder.

## Design Direction

The public architecture instead follows:

    Room Images
        ↓
    Multimodal Perception
        ↓
    Schema-Constrained Output
        ↓
    Validation
        ↓
    Structured Domain Knowledge
        ↓
    Application State

The model is responsible for visual interpretation, while the application remains responsible for the contract around that interpretation.

## Structured Outputs as an Application Boundary

The AI response should map into explicit application schemas rather than become an unstructured blob passed through the system.

A simplified public representation can look like:

    Observation
    ├── category
    ├── value
    └── confidence

This creates a clear boundary between probabilistic inference and deterministic application code.

In the public implementation, Pydantic models are used to validate structured AI results before they continue through the application.

## From Observations to Domain Knowledge

Object recognition alone is not the final product of the vision layer.

The broader transformation is:

    Visual Input
         ↓
    Observations
         ↓
    Entities + Properties
         ↓
    Relationships + Context
         ↓
    Structured Room Knowledge

The purpose is to convert information contained in images into a representation that the application can reason about later.

## Confidence Belongs with AI-Derived Information

A deterministic application value and an AI-derived observation do not necessarily have the same epistemic status.

Instead of treating every model output as an unquestionable fact, structured results can preserve confidence information alongside the interpreted value.

    AI Observation
        ├── structured value
        ├── confidence
        └── traceability metadata

This does not require every downstream component to use the same confidence policy. It simply preserves useful information at the AI boundary.

Production thresholds and decision policies remain implementation-specific.

## Traceability Without Exposing Model Internals

Application-level traceability can help answer questions such as:

- which result came from AI analysis;
- which information has been reviewed;
- where uncertainty exists;
- which structured state is safe for downstream use.

This is different from exposing hidden model chain-of-thought or internal reasoning.

The public architecture focuses on structured result metadata and application state.

## Human Review Before Trusted State

Structured AI output can pass through a review boundary before becoming trusted room state:

    Multimodal Perception
            ↓
    Structured AI Result
            ↓
    Validation
            ↓
    Human Review / Confirmation
            ↓
    Verified Domain State

This is particularly useful when downstream reasoning depends on the quality of the perceived environment.

## Why This Helps the Rest of the System

### Persistence

Structured results can be stored as application data rather than only as model transcripts.

### Validation

Schemas can reject malformed outputs before they propagate.

### Testing

Downstream services can be tested with known structured inputs instead of requiring live multimodal inference.

### Provider isolation

The rest of the application can depend on domain contracts rather than a provider-specific response format.

### Reuse

Verified room knowledge can support multiple downstream requests.

## Relationship to the Digital Twin

The structured vision result is an input to the application's representation of the current room state.

The broader state boundary is described in [structured-state-between-perception-and-reasoning.md](structured-state-between-perception-and-reasoning.md).

The perception/reasoning separation is described in [separating-perception-from-reasoning.md](separating-perception-from-reasoning.md).

Together:

    Images
      ↓
    Perception
      ↓
    Structured Knowledge
      ↓
    Verified Current State
      ↓
    Reasoning

## Engineering Trade-offs

Structured outputs require more work than returning natural-language model responses.

They introduce:

- schema design;
- validation;
- transformation logic;
- versioning concerns;
- error handling when model output does not satisfy the contract.

The benefit is that the AI component becomes easier to integrate into a larger software system.

## What I Learned

One of the main lessons from this project is that integrating multimodal AI is not only about sending images to a model.

The harder engineering question is often:

> How should probabilistic model output become reliable application knowledge?

Explicit schemas, validation, confidence metadata and review boundaries provide a practical bridge between those two worlds.

## Related Public Code

Relevant public examples include:

    backend/app/ai/public_outputs.py
    backend/app/ai/request.py
    backend/app/services/vision_analysis.py

These files demonstrate the public structured-output boundary without exposing the private domain specification.

## Public Scope

This note intentionally excludes the complete domain attribute model, proprietary evidence structures, detailed analysis contracts, experience-report structures, task-specific interpretation rules and internal prompts.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
