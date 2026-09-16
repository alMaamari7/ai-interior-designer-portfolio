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
    +-------------------+
    |                   |
    v                   v
Design Request     Room Knowledge
    |                   |
    +---------+---------+
              |
              v
         AI Reasoning
              |
              v
      Solution Evaluation
              |
              v
        Recommendation
```

The complete private system contains additional domain intelligence and orchestration logic that is not required to understand the engineering architecture shown here.

## Engineering principle

The project deliberately separates **perception from decision-making**. The vision layer converts visual information into structured knowledge. Downstream reasoning works with structured room state, user goals, budget and constraints instead of treating raw images as the decision model.

This makes the application an orchestrated AI system rather than a direct image-to-answer LLM wrapper.

## Public implementation highlights

`backend/app/services/image_quality.py` contains a deterministic pre-inference quality gate using Pillow, NumPy and OpenCV. It checks image integrity, minimum resolution, Laplacian-based sharpness and exposure before multimodal processing.

`backend/app/ai/gemini_client.py` demonstrates a multimodal provider adapter that combines contextual text and image bytes while constraining model responses with a Pydantic-compatible JSON schema.

`backend/app/ai/public_outputs.py` demonstrates typed boundaries between probabilistic AI output and deterministic application code. The schema is deliberately reduced and is **not** the private production Digital Twin.

## Repository structure

```text
backend/
  app/
    ai/
      gemini_client.py
      request.py
      public_outputs.py
    schemas/
      image.py
    services/
      image_quality.py
    main.py
  tests/
  requirements.txt

docs/
  architecture.md
  ai-pipeline.md
  ip-boundary.md

.env.example
.gitignore
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

## Run locally

```bash
git clone https://github.com/alMaamari7/ai-interior-designer-portfolio.git
cd ai-interior-designer-portfolio/backend

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is then available locally and FastAPI exposes its interactive OpenAPI documentation at `/docs`.

To run the public tests:

```bash
cd backend
pytest
```

A provider API key is only needed when directly using the multimodal Gemini adapter. Copy `.env.example` to `.env` and provide your own credentials. `.env` files are ignored by Git.

## Project status

This is an actively developed project. The private repository is the source of truth for the full product. This public repository is maintained as an engineering portfolio and therefore contains selected real implementations and deliberately abstracted interfaces.

The public portfolio currently demonstrates the system boundaries and selected implemented components; it does not claim that every element in the high-level product workflow is included in this repository.

## Disclosure policy

Public code demonstrates **how the software is engineered**. Product-specific intelligence remains private.

Excluded are production prompts and prompt chains, complete domain-AI specifications, internal evidence/readiness rules, targeted capture decision policies, proprietary prioritization/conflict-resolution logic, internal reasoning policies, private credentials, user data, and production configuration.

See [`docs/ip-boundary.md`](docs/ip-boundary.md) for the public/private boundary.

## Author

Asaad Al-Maamari  
B.Sc. Wirtschaftsinformatik — HTW Berlin
