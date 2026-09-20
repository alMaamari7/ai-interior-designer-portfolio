# Technical Image Quality Is Not Information Sufficiency

## Context

While building the room-capture workflow for the AI Interior Designer, I found that two different questions can easily be mixed together:

1. **Is this image technically usable?**
2. **Does the available visual information support the intended downstream analysis?**

They are not the same problem.

A sharp, correctly exposed image can pass every technical check and still fail to show the information needed by a multimodal AI task.

## The Problem

A simple image pipeline might treat successful image validation as proof that the input is ready for AI analysis.

```text
Image
  ↓
Technical Validation
  ↓
PASS
  ↓
AI Analysis
```

But technical validity only tells us whether the image satisfies technical requirements. It does not tell us whether the relevant information is actually visible.

For example, an image may be:

- readable and correctly encoded;
- large enough;
- sufficiently sharp;
- acceptably exposed;

while still missing a useful view of the subject required by the downstream task.

## Design Decision

I separated the two responsibilities.

```text
Image Capture
      ↓
Technical Image Quality
      ↓
Accepted Visual Input
      ↓
Task-specific Information Sufficiency
      ↓
Downstream Analysis
```

### Technical Image Quality

This layer answers:

> Is the image technically suitable for processing?

The public implementation checks properties such as:

- image integrity;
- resolution;
- sharpness;
- exposure.

These checks are intentionally independent from domain-specific visual interpretation.

### Information Sufficiency

This layer answers a different question:

> Does the available visual information support the analysis the system intends to perform?

That decision belongs to the multimodal workflow rather than the low-level image-quality validator.

The production system contains richer task-specific mechanisms for this responsibility. Their detailed rules are intentionally private.

## Why This Separation Matters

### Different failure modes

A blurred image and a sharp image that does not show the needed information fail for different reasons.

### Better feedback

Separating the responsibilities allows the application to distinguish between a technical retake and the need for additional visual information.

### Cleaner architecture

The technical validator does not need to understand interior-design semantics, and the higher-level AI workflow does not need to reimplement basic image checks.

### Testability

Technical checks can be tested deterministically and independently from multimodal inference.

### Cost control

Rejecting clearly unusable images before model inference avoids sending inputs to a multimodal model when deterministic software can already identify the problem.

## Deterministic Checks Before AI

An important engineering principle behind this boundary is:

> Do not use AI for a problem that deterministic software can solve reliably.

In the public portfolio, basic technical checks are handled with ordinary image-processing logic before multimodal inference.

```text
Image
  ↓
Deterministic Quality Gate
  ↓
Multimodal AI
  ↓
Structured Output
```

This keeps AI focused on tasks that actually require semantic interpretation.

## Engineering Trade-offs

Separating the two quality dimensions introduces another workflow boundary and additional state.

However, combining them would make it harder to understand why an input failed and which component should respond.

The separation therefore trades some orchestration complexity for clearer responsibilities, more targeted feedback and independently testable components.

## Related Public Implementation

Relevant public files include:

- `backend/app/services/image_quality.py` — deterministic technical image checks;
- `backend/app/services/vision_analysis.py` — orchestration between accepted image input and multimodal analysis;
- `backend/app/schemas/image.py` — typed quality results.

## What I Learned

In multimodal AI systems, **input quality is multidimensional**.

Technical quality is a prerequisite for useful visual input, but it is not proof that the input contains enough information for the task.

Treating these as separate responsibilities produced a cleaner boundary between conventional software engineering and AI-specific processing.

## Public Scope

The public repository demonstrates the technical quality gate and the architectural distinction described above.

The production rules used to determine task-specific visual requirements, missing evidence and additional capture decisions are intentionally excluded.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
