# Designing Image Storage for a Multimodal AI System

## Context

A multimodal AI application needs more than a model endpoint. Images must move reliably through capture, persistence, frontend display and AI processing while the storage design remains simple enough for an MVP.

For the AI Interior Designer, I therefore treated image persistence as an explicit backend architecture problem rather than storing files as an implementation afterthought.

## Requirements

The storage boundary needs to support:

- persistent room images;
- efficient access from the backend;
- image delivery to the frontend;
- multimodal AI processing;
- simple local and Docker-based development;
- future extension toward cloud/object storage;
- association of future AI-derived artifacts with the same room context.

## Design Decision

The central separation is:

    Database
        ↓
    Image Metadata
    +
    Logical Storage Reference

    File / Object Storage
        ↓
    Binary Image

The binary image itself does not need to live inside the relational database. Instead, the database stores the information the application needs to understand and locate the image.

## Metadata and Binary Storage Have Different Responsibilities

A simplified image record can contain information such as:

    Image
    ├── id
    ├── room relation
    ├── optional domain relation
    ├── semantic role
    ├── storage reference
    └── creation metadata

The storage layer contains the actual file.

This keeps relational data focused on application state and relationships while the binary asset remains in a storage system designed for files.

## Room-Oriented Storage

For the MVP, images are organized around the room they belong to.

    uploads/
    └── rooms/
        └── room_<id>/
            └── images/
                ├── <uuid>.jpg
                ├── <uuid>.jpg
                └── ...

This provides a simple operational boundary for development and debugging. It also makes room-level cleanup, export and later storage management easier than placing every uploaded image into one global directory.

## UUID File Names

The physical file name is intentionally not used as business metadata. Instead of names such as livingroom.jpg, overview.jpg or wall.jpg, the storage layer can generate UUID-based names such as <uuid>.jpg.

This avoids naming collisions and prevents the file system from becoming responsible for domain semantics.

## Storage Should Not Encode Business Meaning

The application already has structured metadata describing what an image represents.

    Physical File Name
            ≠
    Business Meaning

A generic file can be associated with its room and semantic role through the application model. This keeps storage generic while domain behavior remains in the domain and workflow layers.

## Persist Logical References, Not Environment-Specific Paths

Another design decision is to persist a relative storage reference such as:

    rooms/room_<id>/images/<uuid>.jpg

rather than a developer-machine absolute path or an environment-specific URL.

    Database
       ↓
    Logical Storage Reference
       ↓
    Backend Storage Configuration
       ↓
    Physical Location

The backend owns the mapping between the logical reference and the physical storage location. This reduces coupling between persisted application data and the deployment environment.

## Frontend Boundary

The frontend should not need to know where the backend physically stores a file.

For a local MVP, FastAPI can expose the configured upload directory through an application-controlled asset route.

    Frontend
        ↓
    Application Asset URL
        ↓
    FastAPI
        ↓
    Configured Storage
        ↓
    Image

The database reference and backend configuration remain separate from the URL used by the browser.

## MVP First, Migration Path Second

For the current stage, local filesystem storage is intentionally simple.

    MVP
     ↓
    Local Filesystem

A production deployment may later use:

    Application
        ↓
    Storage Abstraction / Configuration
        ↓
    Object Storage

The important architectural decision is not to implement cloud infrastructure prematurely, but to avoid unnecessary assumptions that would make a later migration difficult.

Relative storage references and the separation between metadata and binary assets help preserve that option.

## Future AI Artifacts

Multimodal systems may eventually produce artifacts in addition to the original uploaded images.

    Room Assets
    ├── Source Images
    └── Derived AI Artifacts

Examples could include structured analysis outputs or other derived visual assets.

These are extension points, not claims about features already implemented in the public MVP.

## Engineering Trade-offs

### Local filesystem

Advantages include simple implementation, low infrastructure overhead, convenient local debugging, suitability for early development and straightforward Docker volume usage.

Limitations include additional coordination for distributed deployments, lack of automatic replication/durability and less straightforward horizontal scaling.

### Object storage

Advantages include a better fit for distributed/cloud deployments, scalable asset storage and independent lifecycle management.

Costs include additional infrastructure, credentials/configuration and more operational complexity than an early MVP necessarily needs.

The current architecture therefore optimizes for a simple implementation while preserving a clear migration direction.

## What I Learned

Building a multimodal AI application made it clear that production-oriented AI engineering includes ordinary software architecture decisions as much as model integration.

Image storage affects API boundaries, persistence, frontend delivery, AI input handling, cleanup, deployment and future scalability.

Keeping binary storage, relational metadata and domain semantics separate produced a cleaner architecture and reduced environment-specific coupling.

## Public Scope

This note describes general storage and backend engineering decisions. It does not expose proprietary AI reasoning, evidence assessment or adaptive capture rules.

The public repository focuses on demonstrating the software-engineering boundaries around the AI system while the private repository remains the source of truth for product-specific intelligence.

See [../ip-boundary.md](../ip-boundary.md) for the repository's disclosure policy.
