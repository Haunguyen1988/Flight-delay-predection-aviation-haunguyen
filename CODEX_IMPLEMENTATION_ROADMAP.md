# CODEX_IMPLEMENTATION_ROADMAP.md

## Project Overview

This repository is an existing aviation analytics application built with:

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + Vite
- **ML**: XGBoost + Random Forest ensemble
- **Current capabilities**:
  - Flight analytics dashboard
  - CSV upload and sample data generation
  - Model training
  - Single prediction
  - Batch prediction

## Mission

Upgrade this repository from a **basic flight delay predictor** into an **aviation decision-support platform**.

The final product should provide not only prediction, but also:
- explainability
- operational recommendations
- prediction history
- route intelligence
- scenario simulation
- model monitoring
- aviation operations use cases such as turnaround risk and propagation analysis

---

## Core Execution Rules

### 1. Preserve existing functionality
Do not break the current working flows:
- sample data generation
- CSV upload
- model training
- dashboard loading
- single prediction
- batch prediction

### 2. Implement incrementally
Work phase by phase. Do not attempt a full rewrite.

### 3. Prefer small, reviewable changes
Each task should be implemented in a PR-sized chunk.

### 4. Keep architecture aligned with current repo
Follow the current project structure unless there is a very strong reason to change it.

### 5. Maintain backward compatibility where possible
If existing API responses change, update frontend consumers in the same change set.

### 6. Update all impacted layers together
For any feature, update:
- backend routes
- backend services/models/schemas
- frontend API hooks
- frontend UI
- frontend types
- README documentation

### 7. Fail safely
If model artifacts are not trained or unavailable:
- return safe fallback responses
- show a clear UI message
- do not crash the app

### 8. Prefer MVP first
Implement the simplest correct version first, then improve later.

---

## Definition of Done

A task is complete only if:

- backend starts successfully
- frontend builds successfully
- new API endpoint works
- frontend uses real backend data
- existing flows still work
- README is updated where relevant

---

## Current Repository Structure Assumptions

Use the existing project shape as baseline:

- `backend/app/main.py`
- `backend/app/routers/`
- `backend/app/models/`
- `backend/app/services/`
- `backend/app/ml/`
- `frontend/src/pages/`
- `frontend/src/hooks/`
- `frontend/src/services/`
- `frontend/src/types/`

Do not introduce unnecessary new layers.

---

# PHASED IMPLEMENTATION PLAN

---

## Phase 1 — Prediction Experience Upgrade

### Goal
Turn the prediction page into a more useful decision-support experience.

### Features in this phase
1. Prediction history
2. Typed prediction response
3. Risk band and severity band
4. Recommendation engine
5. Lightweight prediction explanations

### Deliverable
At the end of Phase 1, the app should:
- save prediction history
- show structured prediction results
- display risk/severity bands
- provide recommendations
- explain the main drivers of prediction risk

---

## Phase 2 — Analytics and Decision Support

### Goal
Upgrade the dashboard from descriptive analytics to decision-support analytics.

### Features in this phase
1. Route intelligence
2. Airport congestion indicators
3. What-if simulation
4. Executive summary cards

### Deliverable
At the end of Phase 2, the app should:
- identify risky routes
- show operational pressure by airport/time
- support what-if scenarios
- present executive-style summaries

---

## Phase 3 — ML Maturity Upgrade

### Goal
Improve model realism, quality, and trustworthiness.

### Features in this phase
1. Severity model
2. Delay reason prediction
3. Time-based validation
4. Better unknown-category handling
5. Model monitoring page

### Deliverable
At the end of Phase 3, the app should:
- predict delay severity more realistically
- predict probable delay reason
- use time-aware validation
- warn on out-of-domain inputs
- expose model monitoring information

---

## Phase 4 — Aviation Operations Expansion

### Goal
Introduce airline operations use cases beyond isolated flight prediction.

### Features in this phase
1. Turnaround risk
2. Delay propagation
3. Schedule scoring
4. Alerting

---

## Phase 5 — External Data and Production Readiness

### Goal
Improve realism and make the system more production-like.

### Features in this phase
1. Weather API integration
2. Data quality validation center
3. Exportable reports
4. Configuration hardening

---

# TASK EXECUTION ORDER

Implement in this order unless repository conditions force a change:

1. Phase 1 tasks
2. Phase 2 tasks
3. Phase 3 tasks
4. Phase 4 tasks
5. Phase 5 tasks

Within each phase, prefer backend foundation first, then API, then frontend, then docs.

---

# REQUIRED OUTPUT STYLE FOR EACH TASK

For every implementation task, provide:

1. Summary of what is being changed
2. Files modified
3. Backend changes
4. Frontend changes
5. Any data/model changes
6. Any API contract changes
7. Any migration or compatibility note
8. Test/run instructions
9. README updates

---

# MINIMUM QA CHECKLIST AFTER EACH TASK

After each task:
- run backend locally
- ensure frontend builds
- verify API response manually
- verify UI renders without crashing
- check that existing features still work

---

# PASTE-READY CODEX PROMPT

```text
You are working on an existing FastAPI + React aviation analytics project.

Primary goal:
Upgrade the app from a basic flight delay predictor into an aviation decision-support platform.

Constraints:
- Preserve current working features: data generation, CSV upload, model training, dashboard, single prediction, batch prediction.
- Make changes incrementally by phase.
- Prefer small, reviewable PR-sized changes.
- Keep API backward compatible when possible.
- Update backend, frontend, types, and README together.
- Do not introduce large architectural rewrites unless necessary.

Execution order:
1. Phase 1: prediction history, typed prediction response, risk bands, recommendations, lightweight explanations.
2. Phase 2: route intelligence, airport congestion insights, what-if simulation, executive summary cards.
3. Phase 3: severity model, delay reason model, time-based validation, unknown-category handling, model monitoring.
4. Phase 4: turnaround risk, delay propagation, schedule scoring, alerting.
5. Phase 5: weather API integration, data quality center, export reports, config hardening.

For every task:
- Identify impacted backend files, frontend files, and shared types.
- Implement minimal viable functionality first.
- Add clear API response models.
- Keep code readable and consistent with the current repository structure.
- Update README with new endpoints and screenshots/placeholders when relevant.

Definition of done:
- Backend runs successfully.
- Frontend builds successfully.
- New API endpoints are usable.
- UI is connected to real backend data.
- Existing flows are not broken.
```

---

# END STATE VISION

The final system should feel like:
- an aviation analytics product
- an operations support assistant
- a credible ML + data engineering portfolio project
- a platform that can evolve into schedule risk, disruption analysis, and executive reporting
