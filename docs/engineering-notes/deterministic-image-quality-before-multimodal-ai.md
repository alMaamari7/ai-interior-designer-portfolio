# Deterministic Image Quality Before Multimodal AI

## Context

Multimodal models are useful for semantic visual understanding, but not every image-processing problem requires AI.

Before an uploaded room image reaches multimodal inference, the AI Interior Designer applies a deterministic technical quality gate. The purpose is simple:

> Reject technically unusable inputs before asking an AI model to interpret them.

This keeps technical validation separate from semantic analysis.

## Pipeline Boundary

At a high level:

    Image Upload
         ↓
    Technical Quality Gate
         ↓
      PASS / FAIL
       /       \
    FAIL       PASS
      ↓          ↓
    Retake    Store / Continue
                 ↓
          Multimodal AI

The quality gate answers:

> Is this image technically suitable for further visual processing?

It does not answer what objects are present or what domain attributes they have.

## Independent Quality Checks

The technical gate evaluates several concerns independently:

    Image
      ↓
    Integrity
      ↓
    Resolution
      ↓
    Sharpness
      ↓
    Exposure
      ↓
    Structured Quality Result

Keeping the checks separate makes failures easier to understand, test and communicate.

## Image Integrity

The first question is whether the uploaded file can actually be decoded as a valid image.

A lightweight image library such as Pillow can verify that the file is readable before later processing begins.

This prevents corrupt or invalid files from reaching downstream computer-vision or multimodal components.

## Resolution

Resolution validation uses the image dimensions to determine whether the input satisfies the configured minimum spatial size.

This is intentionally separate from sharpness.

A high-resolution image can still be blurred, while a sharp image can still have insufficient dimensions.

That is why both properties deserve independent checks.

## Sharpness with Variance of Laplacian

For the MVP, sharpness is measured deterministically using the **Variance of Laplacian**.

The processing flow is:

    Image
      ↓
    Grayscale Conversion
      ↓
    Laplacian Operator
      ↓
    Variance
      ↓
    Sharpness Score
      ↓
    Threshold Comparison
      ↓
    PASS / FAIL

With OpenCV, this can be implemented without invoking an AI model.

A higher variance generally indicates stronger edge structure, while a low value can indicate blur.

The metric is a technical indicator, not a universal definition of image quality.

## Thresholds Are Configuration, Not Universal Constants

A threshold-based heuristic should not be treated as a magic number that is correct for every environment.

The intended model is:

    Metric
      ↓
    Configurable Threshold
      ↓
    Calibration with Representative Inputs
      ↓
    Decision

Thresholds belong in configuration and should be calibrated against representative images from the application's actual capture conditions.

The public repository intentionally does not publish production calibration values.

## Exposure

Exposure is another deterministic concern.

The implementation can inspect grayscale intensity statistics and the proportion of pixels near dark or bright extremes to identify images where useful visual information may be lost through severe under- or overexposure.

The goal is not to infer room semantics. It is only to determine whether the image remains technically usable for downstream analysis.

## Structured Results Instead of One Opaque Score

Rather than returning a single unexplained quality number, each technical criterion can produce its own result.

For example:

    Resolution  → PASS
    Sharpness   → FAIL
    Exposure    → PASS
    Integrity   → PASS

    Overall     → FAIL
    Reason      → insufficient sharpness

This provides clearer observability than an opaque overall quality score.

It also creates an explicit contract for downstream workflow behavior.

## From Failure Reason to User Action

Structured failure information can be passed to the interaction layer:

    Deterministic Check
            ↓
    Structured Failure Reason
            ↓
    Interaction Layer
            ↓
    Actionable User Feedback

The quality service should not need to own UI wording. It should communicate what failed; another layer can determine how that result is presented to the user.

This boundary is discussed further in [designing-human-guidance-for-ai-workflows.md](designing-human-guidance-for-ai-workflows.md).

## Technical Quality Is Not Information Sufficiency

Passing the quality gate only means the image is technically usable.

It does not mean that the image exposes every piece of information required by a later semantic task.

    Technical Quality
          ↓
         PASS
          ↓
    Semantic / Task Analysis
          ↓
    May still need more information

The distinction is described in [technical-quality-vs-information-sufficiency.md](technical-quality-vs-information-sufficiency.md).

## Why Deterministic Checks Come First

Using deterministic validation before multimodal inference provides several benefits:

- predictable behavior;
- low-cost execution;
- straightforward unit testing;
- explainable failure reasons;
- less unnecessary model inference;
- cleaner separation between technical and semantic responsibilities.

A useful principle from this work is:

> Use deterministic software for deterministic problems and reserve AI inference for semantic problems.

## Reusable Quality Boundary

The technical gate is intentionally independent from the later semantic role of an image.

Conceptually:

                 ┌→ Overview processing
    Image        ├→ Wall processing
      ↓          ├→ Detail processing
    Quality Gate └→ Other visual processing

The same technical validation can therefore protect multiple downstream visual workflows without duplicating quality logic for each image type.

## Engineering Trade-offs

Deterministic heuristics are simple and testable, but they also require calibration.

A metric such as Variance of Laplacian does not understand the scene semantically, and the useful threshold depends on the capture environment and application requirements.

This is why the quality gate is treated as technical preprocessing rather than as a substitute for multimodal understanding.

## What I Learned

Building the visual pipeline reinforced a useful AI-engineering lesson:

> Adding another model is not always the best way to improve an AI system.

Some problems are better solved with ordinary software and computer vision.

Using Pillow and OpenCV for technical validation keeps multimodal inference focused on the part of the problem where semantic AI is actually useful.

## Related Public Code

The public implementation can be found in:

    backend/app/services/image_quality.py

It demonstrates the deterministic quality boundary used before multimodal processing.

## Public Scope

This note describes the public technical-quality architecture and standard computer-vision methods used by the project.

Production threshold values, calibration data and proprietary downstream evidence/readiness logic are intentionally excluded.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
