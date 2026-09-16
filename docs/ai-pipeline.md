# AI Pipeline

## Overview

The public architecture models AI processing as a sequence of explicit transformations:

```text
Visual Input
    |
    v
Technical Quality Check
    |
    v
Multimodal Perception
    |
    v
Structured AI Output
    |
    v
Human Review
    |
    v
Verified Structured State
    |
    v
Reasoning + User Context
    |
    v
Evaluated Recommendation
```

## 1. Technical image quality

Before multimodal inference, images can be checked for properties such as file integrity, minimum resolution, sharpness and exposure. This stage uses deterministic computer-vision/image-processing techniques and is independent of semantic room understanding.

## 2. Multimodal perception

A multimodal model receives image data and relevant context. Instead of returning free-form text, the AI boundary is designed around structured outputs that can be validated and persisted by the application.

## 3. Structured knowledge

AI observations are transformed into a structured representation of the current room. The complete production ontology and domain-specific attribute model are not included in the public repository.

## 4. Human-in-the-loop verification

Structured AI results can be reviewed before being accepted as verified application state. This creates an explicit distinction between an AI observation and trusted domain knowledge.

## 5. Reasoning and decision support

Downstream reasoning combines verified room state with a design request containing user context such as goals, budget and constraints. The reasoning boundary is public; its production decision policy is private.

## Adaptive capture

The complete system can determine at a high level whether additional visual information is required for downstream analysis and can request additional captures. The domain-specific evidence requirements, sufficiency logic and capture-selection rules are intentionally excluded from this portfolio.

## Structured-output principle

AI responses are treated as application data rather than presentation text. Typed schemas provide validation boundaries between probabilistic model output and deterministic backend processing.
