# INITIAL_GITHUB_ISSUES_SEED.md

## Purpose

This document provides a ready-to-use seed list of GitHub issues for bootstrapping the roadmap execution in this repository.

It is designed to work with:
- `CODEX_IMPLEMENTATION_ROADMAP.md`
- `CODEX_TASKS_PHASE1.md`
- `CODEX_TASKS_PHASE2_PHASE3.md`
- `CODEX_TASKS_PHASE4_PHASE5.md`
- `GITHUB_PROJECT_BOARD_STRUCTURE.md`
- `GITHUB_LABELS_AND_MILESTONES.md`
- `.github/ISSUE_TEMPLATE/*`

Use this file to quickly create:
- phase epic issues
- first implementation issues
- Codex-ready issues
- QA issues
- selected docs issues

---

## Recommended Creation Order

1. Create all 5 epic issues
2. Create Phase 1 implementation issues
3. Create Phase 1 QA issue
4. Start execution with Phase 1 only
5. Create later-phase issues only when the current phase is stable

---

# 1. EPIC ISSUES

Create these first using the **Epic / Phase Work** template.

---

## Epic 1

### Title
`Phase 1 - Prediction Experience Upgrade`

### Suggested labels
- `epic`
- `roadmap`
- `phase-1`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Goal
Upgrade the prediction page into a more useful decision-support experience while preserving all existing functionality.

### In scope
- prediction history
- typed prediction responses
- risk band and severity band
- recommendation engine
- lightweight explanations

### Out of scope
- route intelligence
- simulation
- severity model retraining
- operations workflows

---

## Epic 2

### Title
`Phase 2 - Analytics and Decision Support`

### Suggested labels
- `epic`
- `roadmap`
- `phase-2`
- `priority:p1`

### Suggested milestone
- `Phase 2 - Analytics and Decision Support`

### Goal
Upgrade the dashboard from descriptive analytics into actionable decision support.

### In scope
- route intelligence
- airport congestion indicators
- what-if simulation
- executive summary cards

---

## Epic 3

### Title
`Phase 3 - ML Maturity Upgrade`

### Suggested labels
- `epic`
- `roadmap`
- `phase-3`
- `priority:p1`

### Suggested milestone
- `Phase 3 - ML Maturity Upgrade`

### Goal
Improve model realism, evaluation quality, and trustworthiness.

### In scope
- severity model
- delay reason prediction
- time-based validation
- unknown-category handling
- model monitoring

---

## Epic 4

### Title
`Phase 4 - Aviation Operations Expansion`

### Suggested labels
- `epic`
- `roadmap`
- `phase-4`
- `priority:p1`

### Suggested milestone
- `Phase 4 - Aviation Operations Expansion`

### Goal
Extend the product into airline operations support workflows.

### In scope
- turnaround risk
- delay propagation
- schedule scoring
- alerting

---

## Epic 5

### Title
`Phase 5 - External Data and Production Readiness`

### Suggested labels
- `epic`
- `roadmap`
- `phase-5`
- `priority:p1`

### Suggested milestone
- `Phase 5 - External Data and Production Readiness`

### Goal
Improve realism, validation quality, exports, and configuration handling.

### In scope
- weather integration
- data quality validation
- export reports
- configuration hardening

---

# 2. PHASE 1 STARTER ISSUES

Create these next using the **Codex Execution Task** template.

---

## Issue 1

### Title
`Implement Phase 1 Task 1A - Backend prediction persistence groundwork`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `1A`

### Objective
Prepare backend persistence structures for prediction history without breaking current prediction flow.

### Definition of done
- prediction model/storage is ready
- current prediction behavior is unchanged
- no regression in model training or dashboard

---

## Issue 2

### Title
`Implement Phase 1 Task 1B - Save single prediction results to DB`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `api`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `1B`

### Objective
Persist every successful single prediction result to the database safely.

---

## Issue 3

### Title
`Implement Phase 1 Task 1C - Add prediction history endpoint`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `api`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `1C`

### Objective
Create `GET /api/predict/history` with pagination and safe structured responses.

---

## Issue 4

### Title
`Implement Phase 1 Task 1D - Add frontend types for prediction history`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `frontend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `1D`

### Objective
Add TypeScript types for prediction history payloads.

---

## Issue 5

### Title
`Implement Phase 1 Task 1E - Render recent prediction history in UI`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `frontend`
- `ui`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `1E`

### Objective
Show recent predictions in the Prediction page without breaking the current result panel.

---

## Issue 6

### Title
`Implement Phase 1 Task 2A - Create typed schemas for prediction responses`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `api`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `2A`

### Objective
Introduce reusable backend schemas for prediction-related responses.

---

## Issue 7

### Title
`Implement Phase 1 Task 2B - Replace loose response models in prediction APIs`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `api`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `2B`

### Objective
Apply explicit response models to prediction APIs while keeping behavior backward compatible.

---

## Issue 8

### Title
`Implement Phase 1 Task 3A - Add risk band helper`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `3A`

### Objective
Map delay probability to a readable risk band.

---

## Issue 9

### Title
`Implement Phase 1 Task 3B - Add severity band helper`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `3B`

### Objective
Map estimated delay minutes to a readable severity band.

---

## Issue 10

### Title
`Implement Phase 1 Task 3C - Render risk and severity bands in frontend`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `frontend`
- `ui`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `3C`

### Objective
Display readable risk and severity labels in the Prediction page and history UI.

---

## Issue 11

### Title
`Implement Phase 1 Task 4A - Add recommendation engine`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `4A`

### Objective
Add rule-based recommendation output to prediction responses.

---

## Issue 12

### Title
`Implement Phase 1 Task 4B - Render recommendations in frontend`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `frontend`
- `ui`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `4B`

### Objective
Display a Recommended Actions card in the Prediction page.

---

## Issue 13

### Title
`Implement Phase 1 Task 5A - Add lightweight explanation engine`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `5A`

### Objective
Return simple, useful explanations for why a prediction is high or low risk.

---

## Issue 14

### Title
`Implement Phase 1 Task 5B - Render explanations in frontend`

### Suggested labels
- `codex`
- `enhancement`
- `phase-1`
- `frontend`
- `ui`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Roadmap reference
- `CODEX_TASKS_PHASE1.md`
- Task `5B`

### Objective
Display a Why this prediction card in the Prediction page.

---

## Issue 15

### Title
`Docs - Update README for Phase 1 prediction upgrades`

### Suggested labels
- `documentation`
- `phase-1`
- `priority:p2`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Objective
Document new Phase 1 endpoints and prediction response fields.

---

## Issue 16

### Title
`QA - Verify Phase 1 prediction experience`

### Suggested labels
- `qa`
- `phase-1`
- `priority:p1`

### Suggested milestone
- `Phase 1 - Prediction Experience Upgrade`

### Objective
Verify end-to-end stability for prediction history, typed responses, bands, recommendations, and explanations.

---

# 3. PHASE 2 SEED ISSUES

Create these only after Phase 1 is stable.

---

## Issue 17
`Implement Phase 2 Task 2.1A - Refactor route analytics service foundation`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `data`
- `priority:p1`

## Issue 18
`Implement Phase 2 Task 2.1B - Add route intelligence endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `api`
- `priority:p1`

## Issue 19
`Implement Phase 2 Task 2.1C - Add frontend route intelligence UI`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `frontend`
- `ui`
- `priority:p1`

## Issue 20
`Implement Phase 2 Task 2.2A - Add airport congestion metrics service`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `data`
- `priority:p1`

## Issue 21
`Implement Phase 2 Task 2.2B - Add airport congestion endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `api`
- `priority:p1`

## Issue 22
`Implement Phase 2 Task 2.2C - Render airport congestion section in dashboard`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `frontend`
- `ui`
- `priority:p1`

## Issue 23
`Implement Phase 2 Task 2.3B - Add simulate endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `api`
- `priority:p1`

## Issue 24
`Implement Phase 2 Task 2.3C - Add simulation UI in Prediction page`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `frontend`
- `ui`
- `priority:p1`

## Issue 25
`Implement Phase 2 Task 2.4B - Add executive summary endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `backend`
- `api`
- `priority:p1`

## Issue 26
`Implement Phase 2 Task 2.4C - Render executive summary cards in dashboard`

Suggested labels:
- `codex`
- `enhancement`
- `phase-2`
- `frontend`
- `ui`
- `priority:p1`

## Issue 27
`QA - Verify Phase 2 analytics and simulation`

Suggested labels:
- `qa`
- `phase-2`
- `priority:p1`

---

# 4. PHASE 3 SEED ISSUES

Create these after Phase 2 is stable.

---

## Issue 28
`Implement Phase 3 Task 3.1A - Audit current ML training and prediction pipeline`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `ml`
- `priority:p1`

## Issue 29
`Implement Phase 3 Task 3.1B - Add severity target design and training flow`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `ml`
- `priority:p1`

## Issue 30
`Implement Phase 3 Task 3.1C - Expose severity model output in prediction API`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `backend`
- `api`
- `ml`
- `priority:p1`

## Issue 31
`Implement Phase 3 Task 3.2B - Train delay reason model`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `ml`
- `priority:p1`

## Issue 32
`Implement Phase 3 Task 3.2C - Expose delay reason prediction via API`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `backend`
- `api`
- `ml`
- `priority:p1`

## Issue 33
`Implement Phase 3 Task 3.2D - Render probable delay reason in frontend`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `frontend`
- `ui`
- `priority:p1`

## Issue 34
`Implement Phase 3 Task 3.3A - Replace random split with time-based validation`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `ml`
- `priority:p1`

## Issue 35
`Implement Phase 3 Task 3.4B - Add input warnings to prediction responses`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `backend`
- `api`
- `priority:p1`

## Issue 36
`Implement Phase 3 Task 3.5A - Add model monitoring endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `backend`
- `api`
- `priority:p1`

## Issue 37
`Implement Phase 3 Task 3.5B - Add model monitoring UI page`

Suggested labels:
- `codex`
- `enhancement`
- `phase-3`
- `frontend`
- `ui`
- `priority:p1`

## Issue 38
`QA - Verify Phase 3 model maturity features`

Suggested labels:
- `qa`
- `phase-3`
- `priority:p1`

---

# 5. PHASE 4 SEED ISSUES

Create these after Phase 3 is stable.

---

## Issue 39
`Implement Phase 4 Task 4.1B - Add turnaround risk feature engineering foundation`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `backend`
- `ml`
- `priority:p1`

## Issue 40
`Implement Phase 4 Task 4.1C - Add turnaround risk endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `backend`
- `api`
- `priority:p1`

## Issue 41
`Implement Phase 4 Task 4.1D - Add frontend turnaround risk view`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `frontend`
- `ui`
- `priority:p1`

## Issue 42
`Implement Phase 4 Task 4.2B - Add delay propagation endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `backend`
- `api`
- `priority:p1`

## Issue 43
`Implement Phase 4 Task 4.2C - Render delay propagation chain UI`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `frontend`
- `ui`
- `priority:p1`

## Issue 44
`Implement Phase 4 Task 4.3C - Add schedule scoring endpoint`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `backend`
- `api`
- `priority:p1`

## Issue 45
`Implement Phase 4 Task 4.3D - Add schedule risk UI page`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `frontend`
- `ui`
- `priority:p1`

## Issue 46
`Implement Phase 4 Task 4.4A - Add alert rules engine`

Suggested labels:
- `codex`
- `enhancement`
- `phase-4`
- `backend`
- `priority:p1`

## Issue 47
`QA - Verify Phase 4 operations workflows`

Suggested labels:
- `qa`
- `phase-4`
- `priority:p1`

---

# 6. PHASE 5 SEED ISSUES

Create these after Phase 4 is stable.

---

## Issue 48
`Implement Phase 5 Task 5.1A - Design weather provider abstraction`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `backend`
- `api`
- `priority:p1`

## Issue 49
`Implement Phase 5 Task 5.1B - Add weather integration service`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `backend`
- `data`
- `api`
- `priority:p1`

## Issue 50
`Implement Phase 5 Task 5.1D - Add frontend support for auto-weather enrichment`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `frontend`
- `ui`
- `priority:p1`

## Issue 51
`Implement Phase 5 Task 5.2B - Add upload validation backend logic`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `backend`
- `data`
- `priority:p1`

## Issue 52
`Implement Phase 5 Task 5.2C - Render data quality validation results in UI`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `frontend`
- `ui`
- `priority:p1`

## Issue 53
`Implement Phase 5 Task 5.3B - Add export endpoints`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `backend`
- `api`
- `priority:p1`

## Issue 54
`Implement Phase 5 Task 5.3C - Add export UI actions`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `frontend`
- `ui`
- `priority:p1`

## Issue 55
`Implement Phase 5 Task 5.4B - Refactor configuration management cleanly`

Suggested labels:
- `codex`
- `enhancement`
- `phase-5`
- `backend`
- `frontend`
- `full-stack`
- `priority:p2`

## Issue 56
`QA - Verify Phase 5 external data and readiness features`

Suggested labels:
- `qa`
- `phase-5`
- `priority:p1`

---

# 7. OPTIONAL DOCS AND STABILIZATION ISSUES

## Issue 57
`Docs - Add screenshots and examples for roadmap features`

Suggested labels:
- `documentation`
- `roadmap`
- `priority:p3`

## Issue 58
`Docs - Add contributor workflow for Codex and human reviewers`

Suggested labels:
- `documentation`
- `roadmap`
- `priority:p2`

## Issue 59
`QA - Stabilization and regression hardening pass`

Suggested labels:
- `qa`
- `roadmap`
- `priority:p1`

Milestone:
- `Stabilization / Regression Hardening`

---

# 8. FASTEST PRACTICAL STARTER SET

If you want the smallest useful starting batch, create only these issues first:

1. `Phase 1 - Prediction Experience Upgrade`
2. `Implement Phase 1 Task 1A - Backend prediction persistence groundwork`
3. `Implement Phase 1 Task 1B - Save single prediction results to DB`
4. `Implement Phase 1 Task 1C - Add prediction history endpoint`
5. `Implement Phase 1 Task 1D - Add frontend types for prediction history`
6. `Implement Phase 1 Task 1E - Render recent prediction history in UI`
7. `QA - Verify Phase 1 prediction history flow`

This is the fastest clean entry point for roadmap execution.

---

# 9. RECOMMENDED NEXT ACTIONS

1. Read `GITHUB_PROJECT_BOARD_STRUCTURE.md`
2. Read `GITHUB_LABELS_AND_MILESTONES.md`
3. Create the 5 epic issues from this file
4. Create the Phase 1 starter issues from this file
5. Add them to the GitHub Project board
6. Mark only the first small task as **Ready**
7. Start with Phase 1 Task 1A only

---

# End State

Once these seed issues are created, the repository will have a clean operational starting point for roadmap execution with:
- clear epics
- clearly named implementation tasks
- Codex-ready issue structure
- QA checkpoints
- controlled phase-by-phase delivery
