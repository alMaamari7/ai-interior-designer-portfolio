# Adaptive Capture for Multimodal AI

## Context

A fixed number of uploaded images does not guarantee that a multimodal AI system has the visual information it needs.

Different rooms, viewpoints and occlusions can expose different amounts of useful information. This led me to treat room capture as a **feedback-driven workflow** rather than a static upload form.

## The Problem

A simple capture flow could require a predetermined set of images:

```text
Upload Images
      ↓
Analyze
```

This is easy to implement, but it assumes that the same capture sequence provides sufficient information in every real-world situation.

That assumption is weak for multimodal applications operating on uncontrolled physical environments.

The number of images and the amount of useful visual information are not equivalent.

## Design Direction

At a public architectural level, the capture process can be represented as:

```text
Capture
   ↓
Technical Quality Gate
   ↓
Visual Understanding
   ↓
Information Sufficiency Check
   ↓
┌───────────────┴───────────────┐
│                               │
Sufficient                  Insufficient
│                               │
↓                               ↓
Continue Analysis       Request Additional View
                                │
                                ↓
                             Capture
                                │
                                └────→ Re-evaluate
```

The key idea is that capture and analysis can form a controlled feedback loop.

The system does not need to assume that one fixed image set works for every room.

## Why Adaptive Capture?

### Real environments vary

Furniture, room geometry, camera position and occlusions can change what is visible.

### More images are not automatically better

Collecting images without a reason can increase user effort and processing cost without guaranteeing useful information.

### Capture can be task-oriented

The workflow can reason at a high level about whether additional visual information is required before downstream processing continues.

### Quality can be checked early

Every newly captured image can still pass through deterministic technical validation before it enters higher-level multimodal processing.

## Stateful Orchestration

Adaptive capture changes the problem from a single model call into a workflow problem.

The application needs to know:

- which capture stage it is in;
- which inputs have already been accepted;
- whether processing can continue;
- whether another user interaction is required.

This is one reason I treat AI orchestration as an application responsibility rather than embedding the entire workflow inside a single prompt.

## Multimodal AI Is More Than Model Inference

The architecture highlights a broader lesson:

```text
User Interaction
      +
Input Acquisition
      +
Quality Gates
      +
Workflow State
      +
Multimodal Inference
      +
Structured Outputs
      =
Multimodal AI System
```

The model is an important component, but reliable application behavior also depends on the software around it.

## Engineering Trade-offs

Adaptive capture can reduce unnecessary input collection and improve the relevance of visual information, but it also introduces complexity:

- workflow state;
- additional orchestration;
- user feedback;
- repeated processing;
- stopping conditions;
- failure handling.

For a simple prototype, a fixed upload sequence can be sufficient. For a system intended to work across varying real-world rooms, a feedback-oriented architecture provides a more flexible foundation.

## Related Public Architecture

The public repository demonstrates parts of the surrounding workflow, including:

- deterministic technical image validation;
- multimodal vision orchestration;
- schema-constrained AI output;
- structured application state;
- human-review boundaries.

The adaptive capture mechanism itself is intentionally represented only at a high architectural level.

## What I Learned

One of the most useful lessons from building a multimodal system is that **data acquisition is part of the AI architecture**.

The quality of downstream reasoning depends not only on the model, but also on whether the application has collected the right information and knows when more information is needed.

## Public Scope

This note deliberately stops at the feedback-loop principle.

The private product contains more detailed mechanisms for determining visual requirements and guiding additional capture. The following are intentionally not published:

- exact evidence requirements;
- evidence consolidation logic;
- readiness rules;
- gap-detection logic;
- deficiency-cause analysis;
- perspective-selection logic;
- detailed capture-recommendation rules;
- internal thresholds and decision policies.

The public goal is to demonstrate the orchestration problem and engineering approach without exposing the product-specific capture intelligence.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
