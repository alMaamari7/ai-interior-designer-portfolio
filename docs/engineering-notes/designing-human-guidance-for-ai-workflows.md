# Designing Human Guidance for AI Workflows

## Context

While designing the room-capture experience for the AI Interior Designer, I found an important boundary between the internal AI workflow and the user experience:

> A system result is not automatically a useful user instruction.

The application may know that an input failed, that another action is required or that the workflow can continue. The user, however, needs to know what to do next.

This led me to treat user guidance as a separate application responsibility.

## The Problem

AI and backend components often produce machine-oriented results:

```text
System Result
    ↓
status
reason
next requirement
```

Those results are useful for orchestration, but exposing them directly to a user creates a poor interaction model.

For example:

```text
Technical result:
IMAGE_QUALITY_FAILED

Reason:
MOTION_BLUR
```

The useful user-facing result is not the status code. It is an action:

```text
The image is blurred.
Keep the camera stable and retake the image.
```

The system therefore needs a boundary that translates internal state into understandable next actions.

## Design Principle

At a high level:

```text
System / AI State
        ↓
Interaction Layer
        ↓
Next User Action
        ↓
User
        ↓
Action Result
        ↓
Updated System State
```

The interaction layer does not replace analysis. It consumes the result of analysis and determines how that result should be communicated as an actionable step.

## Separation of Responsibilities

A useful architectural distinction is:

```text
Analysis
   ≠
Decision
   ≠
User Guidance
```

### Analysis

Produces information about the current input or environment.

### Decision / Workflow

Determines what the application needs next.

### User Guidance

Translates the current requirement into an instruction a person can understand and execute.

Keeping these responsibilities separate avoids putting UI wording, domain analysis and workflow logic into one component.

## Stateful Interaction

The capture experience is designed around the current workflow state rather than a fixed sequence of screens.

```text
Current Workflow State
        ↓
Determine Next Required Action
        ↓
Guide User
        ↓
Receive Result
        ↓
Update State
        ↓
Determine Next Action
```

This matters in multimodal workflows because the next interaction may depend on what the system has already learned from previous inputs.

The public architecture describes this state-oriented interaction principle without exposing the product-specific rules that determine detailed capture requirements.

## Progress Is More Than an Interaction Count

A simple interface might measure progress as:

```text
4 / 6 images uploaded
```

But the number of interactions does not necessarily describe whether the workflow has achieved its actual goal.

For an AI-assisted capture process, a more useful conceptual question is:

> Which meaningful workflow requirements have been completed?

This separates **interaction progress** from **task progress**.

The exact completion rules used by the production system remain private, but the architectural principle is useful beyond this project.

## Failure and Recovery

AI-assisted workflows also need to handle cases where the expected next action cannot be completed.

A robust interaction flow should not model only the happy path:

```text
Requested Action
      ↓
Can the user complete it?
    /             \
  yes              no
   ↓                ↓
Continue       Recovery Path
```

Examples can include an input repeatedly failing validation or a requested user action being impractical in the current environment.

Explicit recovery paths help prevent the workflow from leaving the user in an undefined state.

## Relationship to Adaptive Capture

This interaction layer complements the adaptive capture architecture described in [adaptive-capture-for-multimodal-ai.md](adaptive-capture-for-multimodal-ai.md).

The adaptive workflow answers, at a high level:

> Does the system need another user interaction?

The capture experience addresses:

> How should the required next action be communicated and managed?

Keeping these concerns separate creates clearer boundaries between AI processing, workflow orchestration and user interaction.

## Engineering Trade-offs

A dedicated interaction layer introduces additional responsibilities:

- workflow state management;
- synchronization between system state and UI state;
- failure and recovery handling;
- explicit next-action contracts.

In return, it provides:

- clearer separation of concerns;
- more actionable feedback;
- easier frontend/backend boundaries;
- more testable workflow behavior;
- less coupling between AI outputs and UI implementation.

## What I Learned

Building an AI system is not only about producing a correct model output.

The application must also answer:

> What should happen next, and how can the system turn that decision into an action a human can understand and execute?

Treating that translation as an explicit engineering responsibility made the boundary between AI processing, application orchestration and user experience much clearer.

## Public Scope

This note describes the interaction architecture, not the proprietary capture intelligence.

Intentionally excluded are:

- detailed evidence requirements;
- internal readiness and completion rules;
- capture prioritization logic;
- rules for combining multiple missing-information requirements;
- detailed capture-sequence decisions;
- product-specific recommendation-to-guidance mappings;
- perspective and target-selection logic.

The public repository demonstrates the engineering principle while the detailed product-specific capture logic remains private.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
