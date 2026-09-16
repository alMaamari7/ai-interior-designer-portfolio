# AI Interior Designer

> Public engineering portfolio for a larger private AI project.

AI Interior Designer is a multimodal AI system that analyzes visual information about real rooms, builds a structured representation of the current room state, and uses that representation together with user requirements and constraints to support AI-assisted interior-design decisions.

This repository contains a **curated, non-proprietary subset** of the engineering work. It demonstrates AI engineering, multimodal processing, backend architecture, structured outputs, domain modeling, and human-in-the-loop workflows. Proprietary prompts, domain-specific decision rules, evidence-selection logic, internal reasoning policies, and the complete production domain model are intentionally excluded.

## What this project demonstrates

- **Multimodal AI** — room images are processed as inputs to structured AI analysis rather than used only for image generation.
- **Structured room representation** — visual observations are transformed into machine-readable domain knowledge reusable by downstream AI components.
- **AI orchestration** — perception, structured knowledge, human review, reasoning, and recommendation are separated into explicit system responsibilities.
- **Human-in-the-loop AI** — AI-generated information can be reviewed and confirmed before becoming trusted downstream state.
- **Computer vision quality gates** — image integrity, resolution, sharpness, and exposure can be checked before multimodal analysis.
- **Backend engineering** — Python, FastAPI, Pydantic, SQLAlchemy and REST APIs.

## High-level architecture

```text
User
  |
  v
Room Capture
  |
  v
Technical Image Quality
  |
  v
Multimodal Vision Analysis
  |
  v
Structured Room Representation
  |
  v
Human Review / Confirmation
  |
  v
Verified Room State
  |
  +--------------------+
  |                    |
  v                    v
Design Request     Existing Room Knowledge
  |                    |
  +---------+----------+
            |
            v
       AI Reasoning
            |
            v
     Candidate Solution
            |
            v
        Evaluation
            |
            v
      Recommendation
```

The complete private system contains additional domain intelligence and orchestration logic that is not required to understand the engineering architecture shown here.

## Engineering principle

The project deliberately separates **perception from decision-making**. The vision layer converts visual information into structured knowledge. Downstream reasoning works with structured room state, user goals, budget and constraints instead of treating raw images as the decision model.

This makes the application an orchestrated AI system rather than a direct image-to-answer LLM wrapper.

## Public repository scope

```text
backend/
  app/
    ai/             # public AI interfaces and structured-output examples
    api/            # selected FastAPI endpoints
    core/           # configuration and shared infrastructure
    db/             # database infrastructure
    models/         # curated public domain model
    schemas/        # public API/data contracts
    services/       # selected application and image-quality services

docs/
  architecture.md
  ai-pipeline.md
  ip-boundary.md

tests/
```

## Technology stack

**AI & Vision**  
Multimodal AI · LLMs · Computer Vision · Structured Outputs · AI Orchestration · Human-in-the-Loop

**Backend**  
Python · FastAPI · Pydantic · SQLAlchemy · REST API

**Image Processing**  
OpenCV · Pillow · NumPy

**Data & Infrastructure**  
PostgreSQL · Alembic · environment-based configuration

## Project status

This is an actively developed project. The private repository is the source of truth for the full product. This public repository is maintained as an engineering portfolio and therefore contains selected implementations and deliberately abstracted interfaces.

## Disclosure policy

Public code demonstrates **how the software is engineered**. Product-specific intelligence remains private.

Excluded are production prompts and prompt chains, complete domain-AI specifications, internal evidence/readiness rules, targeted capture decision policies, proprietary prioritization/conflict-resolution logic, internal reasoning policies, private credentials, user data, and production configuration.

See [`docs/ip-boundary.md`](docs/ip-boundary.md) for the public/private boundary.

## Author

Asaad Al-Maamari  
B.Sc. Wirtschaftsinformatik — HTW Berlin
