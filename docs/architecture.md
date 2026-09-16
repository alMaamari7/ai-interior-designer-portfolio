# Architecture

## System view

The system is organized around explicit boundaries between visual perception, structured knowledge, human verification and downstream decision support.

```text
                 +------------------+
                 |      Client      |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 |   FastAPI API    |
                 +--------+---------+
                          |
            +-------------+-------------+
            |                           |
            v                           v
 +----------------------+     +----------------------+
 | Room / Image Domain  |     | Application Services |
 +----------+-----------+     +----------+-----------+
            |                           |
            +-------------+-------------+
                          |
                          v
               +---------------------+
               | Capture & Quality   |
               +----------+----------+
                          |
                          v
               +---------------------+
               | Multimodal Vision   |
               +----------+----------+
                          |
                          v
               +---------------------+
               | Structured Room     |
               | Representation      |
               +----------+----------+
                          |
                          v
               +---------------------+
               | Human Review        |
               +----------+----------+
                          |
                          v
               +---------------------+
               | Verified Room State |
               +----------+----------+
                          |
                 +--------+--------+
                 |                 |
                 v                 v
          Design Request      Room Knowledge
                 |                 |
                 +--------+--------+
                          |
                          v
                 +----------------+
                 | AI Reasoning   |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 | Evaluation /   |
                 | Recommendation |
                 +----------------+
```

## Architectural responsibilities

### API layer

FastAPI endpoints expose application capabilities while keeping business and AI logic outside HTTP handlers.

### Domain and persistence

SQLAlchemy models represent persistent application state. Public models are intentionally curated; the complete private domain model is not mirrored here.

### Schemas

Pydantic models define explicit boundaries for incoming requests, outgoing responses and structured AI results.

### Capture and quality

Image processing is separated from semantic AI analysis. Technical quality checks can reject unusable inputs before invoking more expensive multimodal models.

### Multimodal perception

The vision component receives images and contextual information and produces structured results rather than unstructured prose. The complete production schema and domain-specific analysis rules are private.

### Human verification

AI-generated observations are not automatically treated as trusted domain truth. A review/confirmation boundary allows verified information to become downstream state.

### Reasoning

Reasoning consumes structured state and user requirements. Its public interface demonstrates separation of concerns; product-specific reasoning policies and decision rules are intentionally not published.

## Why this architecture

The architecture avoids coupling image recognition directly to final design generation. Each stage has an explicit responsibility and data contract, making the system easier to validate, test and evolve independently.
