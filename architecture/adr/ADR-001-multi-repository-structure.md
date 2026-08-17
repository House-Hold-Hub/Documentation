# ADR-001: Multi-Repository Architecture

**Date:** August 16, 2026  
**Status:** Superseded  
**Author:** Product/Engineering Team  
**Owner:** Documentation repository; Architecture/Engineering stewardship  
**Last reviewed:** August 16, 2026  
**Canonical for:** Historical multi-repository decision provenance only  
**Superseded by:** [ADR-009: Five-repository topology](ADR-009-five-repository-topology.md)

> **Historical scope:** This record is preserved as the original multi-repository decision. Its three-repository topology, repository trees, API-specification location, and implementation examples are non-normative.

---

## Context

HouseHoldHub consists of three application components:
- Backend API (Python/Django)
- Frontend web application (React/TypeScript)
- Infrastructure/deployment configuration

We must decide whether to use:
1. **Monorepo:** Single repository with Backend/, Frontend/, Infrastructure/ subdirectories
2. **Multi-repo:** Separate repositories for each component

---

## Decision

Use a **multi-repository architecture** with separate repositories for Backend and Frontend, with a separate Infrastructure/DevOps repository.

```
HouseHoldHub/
├── Backend/              (separate git repo)
├── Frontend/             (separate git repo)
└── Infrastructure/       (separate git repo)
```

---

## Rationale

### Benefits of Multi-Repo
1. **Separate CI/CD pipelines:** Backend and Frontend can be tested/deployed independently
2. **Clear ownership:** Teams own their specific repository; easier code review process
3. **Decoupled release cycles:** Backend and Frontend can release at different cadences
4. **Repository size:** Smaller repos are easier to clone, faster git operations
5. **Language separation:** Backend (Python) and Frontend (Node.js) can have separate tooling
6. **Clear interfaces:** REST API defines contract; repositories communicate via HTTP
7. **Future flexibility:** Can swap implementations (e.g., replace React with Vue) without touching Backend repo

### Risks of Multi-Repo
1. **Coordination overhead:** Changes may span Backend and Frontend; requires coordination
2. **API versioning:** Must manage API contracts carefully; versioning essential
3. **Testing:** Integration tests require spinning up both services

### Mitigations
1. **API versioning:** REST API versioned (/api/v1/, /api/v2/, etc.); 6-month deprecation window
2. **Integration tests:** Docker Compose environment runs both services; integration tests verify contract
3. **Shared documentation:** API specification (OpenAPI/Swagger) shared between repos

---

## Alternatives Considered

### Monorepo (Single Repository)
- **Pros:** Single clone; atomic commits across services
- **Cons:** Slower git operations; coupled CI/CD; one failure blocks all deployments
- **Not chosen:** Multi-repo better for team independence and MVP simplicity

---

## Consequences

### Positive
- ✓ Backend team can work independently on API
- ✓ Frontend team can work independently on UI
- ✓ Separate build/test/deploy pipelines
- ✓ Cleaner git history (no cross-service commits)
- ✓ Easy to understand each repo's scope

### Negative
- ✗ Requires API specification (OpenAPI) to define contract
- ✗ Integration testing must spin up both services
- ✗ Release coordination needed for major API changes
- ✗ Must version API endpoints (/api/v1/, /api/v2/, etc.)

### Migration Path
- Monorepo to multi-repo is easy: split at directory level
- Multi-repo to monorepo: merge histories (more complex but doable)
- **Recommended:** Start with multi-repo; move to monorepo only if team velocity suffers

---

## Implementation

Each repository is independently cloned, versioned, tested, and deployed:

```
# Backend repository structure
Backend/
├── householdhub/        (Django project)
├── api/                 (Django app)
├── tests/
├── requirements.txt
├── manage.py
├── docker-compose.yml   (includes PostgreSQL)
└── Dockerfile

# Frontend repository structure
Frontend/
├── src/
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   ├── api/
│   ├── context/
│   └── types/
├── package.json
├── Dockerfile
└── .env.example

# Infrastructure repository
Infrastructure/
├── docker-compose.yml   (full stack)
├── .env.production      (production config)
├── nginx.conf           (if deploying to nginx)
└── deploy.sh            (deployment script)
```

### Integration Points

1. **API Specification:** OpenAPI/Swagger document defines REST contract
   - Located in Backend repo or shared documentation repo
   - Frontend codegen tools can auto-generate types from spec

2. **Docker Compose:** Full-stack development environment
   - Brings up PostgreSQL, Backend, Frontend
   - Located in root HouseHoldHub directory or Infrastructure repo

3. **CI/CD Pipelines:** Separate workflows per repository
   - Backend: runs tests, lints, builds Docker image, pushes to registry
   - Frontend: runs tests, lints, builds static assets, pushes to registry
   - Infrastructure: triggers deployments when both images updated

---

## Related ADRs

- ADR-002: Django + Django REST Framework backend
- ADR-006: API-based synchronization without real-time transport

---
