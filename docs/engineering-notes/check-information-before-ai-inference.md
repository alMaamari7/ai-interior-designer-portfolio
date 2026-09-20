# Check Information Before AI Inference

## Context

While designing the multimodal analysis pipeline for the AI Interior Designer, I ran into a failure mode that is easy to overlook:

> A model can be asked to infer something even when the input does not expose the information needed to support that inference.

A technically valid image is not automatically informative enough for every downstream task. This led me to introduce a conceptual boundary between **available input** and **task-specific inference**.

## The Problem

A simple AI pipeline often looks like this:

```text
Input
  ↓
Model
  ↓
Prediction
```

But this assumes that the input actually contains the information required by the task.

A multimodal model may still produce an answer when relevant details are missing, too distant, occluded or otherwise unavailable.

The engineering question therefore becomes:

> Should the system attempt this inference at all?

## Design Principle

At a high architectural level:

```text
Task
  ↓
Information Requirements
  ↓
Available Input
  ↓
Readiness Check
  ↓
┌───────────────┴───────────────┐
│                               │
Ready                       Not Ready
│                               │
↓                               ↓
Inference               Do Not Infer Yet
```

The goal is to separate the decision that enough relevant information is available from the later interpretation of that information.

## Observation Is Not Interpretation

A useful distinction is:

```text
What needs to be observable?
            ≠
What does the observation mean?
```

The first question concerns whether the input exposes the information required by the task.

The second is the actual inference problem.

Keeping them separate reduces the temptation to turn missing information into an unsupported prediction.

## Why Domain Knowledge Matters

Some tasks require domain-aware knowledge about which information must be available before an inference is meaningful.

This suggests another useful separation:

```text
Domain Knowledge
      ↓
Information Requirements
      ↓
Runtime Input
      ↓
Readiness
      ↓
Inference
```

The important point is not to hard-code every requirement into one prompt. The architecture can treat task knowledge, runtime input and inference as separate responsibilities.

This complements the ideas described in [separating-domain-knowledge-from-ai-instructions.md](separating-domain-knowledge-from-ai-instructions.md).

## Missing Information Should Be a Valid Outcome

An AI system should not be forced to produce a domain prediction when the available information cannot support one.

Conceptually:

```text
Relevant information available
        ↓
      infer

Relevant information unavailable
        ↓
report insufficient information
or request more input
```

Treating insufficient information as an explicit workflow state creates a cleaner boundary for uncertainty handling and downstream orchestration.

## Three Different Questions

In a multimodal pipeline, I found it useful to distinguish three responsibilities:

### 1. Technical Input Quality

Can the application reliably process the input?

Examples include integrity, resolution, sharpness and exposure.

### 2. Information Availability

Does the available input expose the information required by the intended task?

### 3. Interpretation

What does the available information mean?

```text
Technical Quality
        ↓
Information Availability
        ↓
Interpretation
```

These stages solve different problems and can fail independently.

The distinction between the first two is discussed further in [technical-quality-vs-information-sufficiency.md](technical-quality-vs-information-sufficiency.md).

## Why This Matters

### Fewer unsupported predictions

The system can avoid treating unavailable information as if it had actually been observed.

### Clearer uncertainty boundaries

Missing information becomes different from low confidence in an interpretation.

### Better orchestration

The application can react differently depending on whether an input is technically invalid, informationally insufficient or simply uncertain.

### Reusable task knowledge

Information requirements can conceptually belong to domain/task knowledge rather than being rediscovered independently for every model request.

## Engineering Trade-offs

Introducing an information-readiness boundary adds complexity:

- additional domain modeling;
- readiness state;
- more orchestration;
- coordination between task knowledge and runtime input;
- additional failure paths.

For simple AI demos, directly invoking a model may be enough.

For larger multimodal systems, however, explicitly deciding whether the input supports the requested inference can create a more reliable foundation.

## What I Learned

One of the most useful questions I started asking while building this project was not:

> Can the model answer this?

but:

> Does the input actually contain the information required to support the answer?

That shifts part of AI engineering from prompt construction toward information architecture and workflow design.

## Public Scope

This note describes the general engineering principle only.

The production system contains domain-specific mechanisms for defining information requirements and determining analysis readiness. Those mechanisms are intentionally not published.

Excluded from the public repository are:

- detailed domain-specific visual requirements;
- attribute-level information requirements;
- production readiness rules;
- internal evidence-assessment mechanisms;
- gap-detection logic;
- rules connecting missing information to additional capture;
- product-specific thresholds and decision policies.

The public portfolio demonstrates the architecture boundary without exposing the proprietary information-requirement and adaptive-capture logic.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
