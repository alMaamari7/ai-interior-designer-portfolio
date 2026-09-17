# AI Interior Designer

[![CI](https://github.com/alMaamari7/ai-interior-designer-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/alMaamari7/ai-interior-designer-portfolio/actions/workflows/ci.yml)

> Public engineering portfolio for a larger private AI project.

AI Interior Designer is a multimodal AI system that analyzes visual information about real rooms, builds a structured representation of the current room state, and uses that representation together with user requirements and constraints to support AI-assisted interior-design decisions.

This repository contains a **curated, non-proprietary subset** of the engineering work. It demonstrates AI engineering, multimodal processing, backend architecture, structured outputs, persistence, domain modeling, human-in-the-loop workflows, automated testing and CI. Proprietary prompts, domain-specific decision rules, evidence-selection logic, internal reasoning policies, and the complete production domain model are intentionally excluded.

## What this project demonstrates

- **Multimodal AI** — room images are processed as inputs to structured AI analysis rather than used only for image generation.
- **End-to-end AI engineering** — a public API path connects image upload, deterministic quality validation, multimodal inference and schema-validated structured output.
- **Structured room representation** — visual observations are transformed into machine-readable domain knowledge reusable by downstream AI components.
- **AI orchestration** — perception, structured knowledge, human review, reasoning and recommendation are separated into explicit system responsibilities.
- **Human-in-the-loop AI** — AI-generated information can be reviewed or corrected before becoming trusted downstream state.
- **Computer vision quality gates** — image integrity, resolution, sharpness and exposure are checked before multimodal analysis.
- **Backend engineering** — Python, FastAPI, Pydantic, SQLAlchemy and REST APIs are used to separate API, service, AI and persistence responsibilities.
- **Engineering quality** — public components are covered by automated tests executed through GitHub Actions.

## Implemented public AI path

The strongest implementation path in this portfolio is executable end to end:

```text
POST /vision/analyze
        |
        v
FastAPI UploadFile
        |
        v
Technical Image Quality Gate
  - integrity
  - resolution
  - sharpness
  - exposure
        |
        v
Multimodal AI Request
  - contextual text
  - image bytes
  - MIME type
  - response schema
        |
        v
Gemini 2.5 Flash
        |
        v
Schema-constrained JSON
        |
        v
Pydantic Validation
        |
        v
Structured Room Analysis
```

The public implementation deliberately stops before proprietary evidence assessment and domain-specific capture decisions.

## High-level product architecture

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

The complete private system contains additional domain intelligence and orchestration logic. The diagram communicates the product-level component boundaries; it does not imply that every private component is published here.

## Engineering principle

The project deliberately separates **perception from decision-making**. The vision layer converts visual information into structured knowledge. Downstream reasoning works with structured room state, user goals, budget and constraints instead of treating raw images as the decision model.

This makes the application an orchestrated AI system rather than a direct image-to-answer LLM wrapper.

## Public implementation highlights

### Computer vision quality gate

`backend/app/services/image_quality.py` contains deterministic pre-inference validation using Pillow, NumPy and OpenCV. It checks image integrity, minimum resolution, Laplacian-based sharpness and exposure before an image reaches the multimodal model.

### Multimodal model adapter

`backend/app/ai/gemini_client.py` provides a thin provider boundary that combines contextual text with image bytes and constrains the model response using a Pydantic-compatible JSON schema.

### Structured outputs

`backend/app/ai/public_outputs.py` demonstrates typed boundaries between probabilistic AI output and deterministic application code. The published schema is deliberately reduced and is **not** the private production Digital Twin schema.

### Vision orchestration

`backend/app/services/vision_analysis.py` connects technical validation, multimodal request construction, model inference, JSON parsing and Pydantic validation into one application service.

### Human-in-the-loop boundary

AI analysis and confirmed analysis are represented separately. The public review service demonstrates how an AI proposal can be accepted or corrected before promotion to trusted downstream information.

### Persistence

Selected SQLAlchemy models demonstrate persistence relationships between users, rooms, AI analyses and human-confirmed analyses without exposing the full private domain model.

## Repository structure

```text
.github/
  workflows/
    ci.yml

backend/
  app/
    ai/
      gemini_client.py
      public_outputs.py
      request.py
    api/
      analysis.py
      vision.py
    db/
      base.py
    models/
      ai_analysis.py
      confirmed_ai_analysis.py
      room.py
      user.py
    schemas/
      analysis.py
      image.py
      vision.py
    services/
      analysis_review.py
      image_quality.py
      vision_analysis.py
    main.py
  tests/
    test_analysis_review.py
    test_health.py
    test_public_outputs.py
    test_vision_analysis.py
  requirements.txt

docs/
  architecture.md
  ai-pipeline.md
  ip-boundary.md

.env.example
.gitignore
README.md
```

## Technology stack

**AI & Vision**  
Multimodal AI · LLMs · Computer Vision · Structured Outputs · AI Orchestration · Human-in-the-Loop

**Backend**  
Python · FastAPI · Pydantic · SQLAlchemy · REST API

**Image Processing**  
OpenCV · Pillow · NumPy

**AI Provider**  
Google Gemini 2.5 Flash via `google-genai`

**Data & Infrastructure**  
PostgreSQL · environment-based configuration · GitHub Actions CI

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

FastAPI exposes the interactive OpenAPI documentation at `/docs`.

### Run tests

From the `backend` directory:

```bash
python -m pytest -q
```

The same test suite is executed automatically by GitHub Actions on pushes and pull requests to `main`.

### Configure multimodal inference

A provider API key is only required for calls that execute the Gemini adapter. Copy the example configuration and supply your own credential:

```bash
cp ../.env.example ../.env
```

Set `AI_API_KEY` in `.env`. Environment files are excluded from version control.

## Public vs. private scope

The private repository remains the source of truth for the full product. This portfolio contains selected real implementations plus deliberately abstracted interfaces.

**Public:** backend/API patterns, multimodal provider integration, technical image-quality validation, structured-output handling, selected persistence models, human-review boundaries, tests and CI.

**Abstracted:** Digital Twin, design-request context, reasoning, solution evaluation and recommendation interfaces.

**Private:** production prompts, complete Domain AI Specification, full Digital Twin schema, evidence/readiness logic, evidence-gap diagnosis, targeted capture policies, detailed reasoning contracts, prioritization/conflict-resolution rules, optimization policies and other product-specific decision intelligence.

See [`docs/ip-boundary.md`](docs/ip-boundary.md) for the detailed publication boundary.

## Project status

**Active development.** The public repository demonstrates selected implemented engineering components and architectural boundaries. It intentionally does not represent the complete production system.

## Author

Asaad Al-Maamari  
B.Sc. Wirtschaftsinformatik — HTW Berlin
