# Development Phases

This document describes the AI Interior Designer workflow at a **public architectural level**.

It is derived from the larger private project specification but intentionally omits product-specific evidence rules, prompts, detailed domain schemas and decision policies.

Status labels distinguish between the full product roadmap and what is demonstrable in this public repository.

- **Public implementation available** — representative executable code exists in this repository.
- **Private / partially represented** — the larger project contains work in this area, while the public repository exposes only safe interfaces or selected components.
- **Planned / evolving** — the architecture is defined at a high level but remains under development.

---

## Phase 1 — Foundation & Domain Modeling

### Goal

Establish the software foundation and a structured domain representation that can support room capture, AI analysis and later design requests.

### Main responsibilities

- backend/API architecture;
- typed request and response contracts;
- persistence boundaries;
- room ownership and room state;
- separation between persistent room information and later AI processing.

### Engineering focus

```text
FastAPI
  +
Pydantic
  +
SQLAlchemy
  +
Domain Models
  +
Service Boundaries
```

### Public status

**Public implementation available.**

The portfolio includes selected FastAPI, Pydantic and SQLAlchemy components. The complete private domain model is deliberately reduced.

---

## Phase 2 — Create & Capture Room

### Goal

Create the room context and collect technically usable visual information for later AI analysis.

The phase is not simply an image uploader. It establishes the visual basis required by downstream perception.

### Public workflow

```text
Room Context
     ↓
Image Capture
     ↓
Technical Image Quality
     ↓
Accepted Visual Input
     ↓
Initial Visual Understanding
     ↓
Additional Capture when required
```

### Technical quality gate

Each captured image can be checked before expensive multimodal processing.

The public implementation evaluates:

- file integrity;
- image resolution;
- sharpness;
- exposure.

Failed images can be rejected before they reach the multimodal model.

### Adaptive capture concept

The larger system can determine at a high level whether more visual information is required and request additional capture when needed.

The private mechanisms that determine exactly **what evidence is required, whether it is sufficient, why it is missing and which view should be requested** are intentionally not published.

### Public status

**Public implementation available for the technical image-quality path. Private / partially represented for adaptive capture.**

---

## Phase 3 — Multimodal Vision Analysis

### Goal

Transform captured images and room context into structured, machine-readable knowledge about the current room.

### Public workflow

```text
Accepted Image
     +
Room Context
     ↓
Multimodal AI Request
     ↓
Schema-constrained Model Output
     ↓
Pydantic Validation
     ↓
Structured Room Analysis
```

### Engineering focus

The vision layer separates probabilistic model inference from deterministic application code through typed structured outputs.

At a conceptual level, the complete system analyzes both individual room elements and room-level context/relationships.

The full private output schema and domain-specific analysis rules are not published.

### Public status

**Public implementation available.**

The repository contains an executable `POST /vision/analyze` path, multimodal Gemini adapter, reduced public output schema and tests.

---

## Phase 4 — Structured Current Room State / Digital Twin

### Goal

Consolidate room information into a structured representation of the existing state that downstream components can reuse.

### Architectural role

```text
Visual Information
      ↓
Vision Analysis
      ↓
Structured Current Room State
      ↓
Shared Knowledge for downstream AI
```

The important boundary is that later decision components work with structured room knowledge instead of depending directly on raw room images.

### Public status

**Private / partially represented.**

The public repository demonstrates selected persistence and structured-output patterns, but the complete Digital Twin schema, internal attributes and domain relationships remain private.

---

## Phase 5 — Human Review & Confirmation

### Goal

Allow AI-generated information to be reviewed or corrected before it becomes trusted downstream state.

### Workflow

```text
AI-generated Analysis
        ↓
Human Review
   ┌────┴────┐
   ↓         ↓
Accept     Correct
   └────┬────┘
        ↓
Confirmed Analysis
        ↓
Trusted Room State
```

This keeps probabilistic model output distinct from confirmed application state.

### Public status

**Public implementation available at the architectural boundary.**

The portfolio includes separate AI-analysis and confirmed-analysis persistence models, review schemas, a review service and tests.

---

## Phase 6 — Design Request

### Goal

Describe what the user wants to achieve without mutating the verified current room state.

At a public level, a Design Request can provide:

- user goals;
- functional requirements;
- budget;
- constraints;
- desired improvements.

### Architectural role

```text
Verified Room State
       +
Design Request
       ↓
Reasoning Input
```

Because the room state and request are separated, one room can support multiple redesign scenarios.

### Public status

**Private / partially represented.**

A reduced reasoning-context interface is public. The complete private Design Request model is not published.

---

## Phase 7 — AI Reasoning & Decision Support

### Goal

Interpret the verified room state in relation to user requirements and develop a suitable design solution before visual generation.

### Public abstraction

```text
Current Room Knowledge
        +
User Goals
        +
Budget
        +
Constraints
        ↓
Reasoning / Decision Support
        ↓
Design Strategy / Candidate Solution
```

This phase is deliberately separated from vision analysis:

- perception determines what the current room contains;
- reasoning determines what changes make sense for the requested outcome.

### Engineering significance

This separation prevents the product from collapsing into a single image-to-answer prompt and creates explicit contracts between perception, knowledge representation and decision-making.

### Public status

**Private / partially represented.**

The repository exposes only generic reasoning boundaries. Detailed internal reasoning stages, prompts, policies, prioritization and conflict-resolution logic remain private.

---

## Phase 8 — Solution Evaluation & Recommendation

### Goal

Evaluate a proposed solution against the relevant goals and constraints and present an understandable recommendation.

### Public abstraction

```text
Candidate Solution
        ↓
Evaluation
        ↓
Recommendation
        ↓
User Decision
```

The product architecture treats evaluation as a separate responsibility rather than assuming that the first generated solution is automatically suitable.

### Public status

**Planned / evolving in the public portfolio; private logic excluded.**

A generic recommendation contract is included, while domain-specific evaluation criteria, scoring, optimization and trade-off policies remain private.

---

## Phase 9 — Design Generation / Presentation

### Goal

Turn the selected design decision into a user-facing representation.

This may include visual presentation and other downstream product experiences.

The engineering principle remains:

> **Think before create:** visual generation should consume an already reasoned and evaluated design direction rather than replace the reasoning process.

### Public status

**Planned / evolving.**

This repository currently focuses on the upstream AI-engineering architecture rather than final image generation.

---

# End-to-end view

```text
Foundation & Domain Modeling
          ↓
Create & Capture Room
          ↓
Multimodal Vision Analysis
          ↓
Structured Current Room State
          ↓
Human Review & Confirmation
          ↓
Verified Room State
          +
     Design Request
          ↓
AI Reasoning / Decision Support
          ↓
Solution Evaluation
          ↓
Recommendation
          ↓
Design Generation / Presentation
```

## Deliberately omitted details

The public phase model explains **what each system responsibility does and how components interact at a high level**.

It does not disclose the private mechanisms that provide product-specific intelligence, including:

- production prompts;
- complete domain-AI schemas;
- detailed evidence requirements;
- evidence readiness/sufficiency logic;
- evidence-gap diagnosis;
- targeted capture-selection rules;
- detailed internal reasoning sequence and contracts;
- prioritization and conflict-resolution policies;
- evaluation weights, scoring or optimization logic.

For the disclosure rationale, see [ip-boundary.md](ip-boundary.md).
