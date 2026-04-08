# GITHUB_LABELS_AND_MILESTONES.md

## Purpose

This document provides a practical, copy-friendly checklist for setting up:
- GitHub labels
- GitHub milestones
- issue naming conventions
- phase mapping

It is intended to be used together with:
- `GITHUB_PROJECT_BOARD_STRUCTURE.md`
- `CODEX_IMPLEMENTATION_ROADMAP.md`
- `CODEX_TASKS_PHASE1.md`
- `CODEX_TASKS_PHASE2_PHASE3.md`
- `CODEX_TASKS_PHASE4_PHASE5.md`

---

## Recommended Setup Order

1. Create labels
2. Create milestones
3. Create phase epic issues
4. Create first Codex execution issues
5. Add everything to the GitHub Project board

---

# 1. LABEL SET

Use the following labels.

## A. Phase labels
Create these first:

- `phase-1`
- `phase-2`
- `phase-3`
- `phase-4`
- `phase-5`
- `roadmap`

### Purpose
- identify which roadmap phase an issue belongs to
- make filtering easier in Project views

### Recommended usage
- every roadmap issue should have one phase label
- epic issues should have both `roadmap` and the specific phase label

---

## B. Work type labels

- `epic`
- `enhancement`
- `codex`
- `bug`
- `qa`
- `documentation`

### Purpose
- classify what kind of work the issue represents

### Recommended usage
- use `epic` for phase-level umbrella issues
- use `codex` for issues intended to be executed by Codex
- use `qa` for verification and regression issues

---

## C. Area labels

- `backend`
- `frontend`
- `ml`
- `data`
- `full-stack`
- `ui`
- `api`

### Purpose
- identify the primary implementation area

### Recommended usage
Examples:
- prediction history endpoint → `backend`, `api`
- simulation panel UI → `frontend`, `ui`
- severity model → `ml`
- schedule scoring page with endpoint → `full-stack`

---

## D. Priority labels

- `priority:p0`
- `priority:p1`
- `priority:p2`
- `priority:p3`

### Meaning
- `priority:p0` → critical blocker
- `priority:p1` → high priority current-phase work
- `priority:p2` → medium priority improvement
- `priority:p3` → low priority or later follow-up

### Recommended usage
- use `priority:p1` for most roadmap tasks in the current phase
- reserve `priority:p0` for broken core flows or severe regressions

---

## E. Flow / state helper labels

- `blocked`
- `ready`
- `needs-review`
- `needs-qa`
- `good-first-task`

### Purpose
These are optional but useful if you want lightweight state signaling in addition to Project status fields.

### Recommended usage
- `ready` → clearly defined and ready for execution
- `blocked` → cannot proceed due to dependency or decision
- `needs-review` → implemented and awaiting review
- `needs-qa` → ready for verification

---

# 2. MINIMUM LABEL SET

If you want a minimal setup, create at least these labels:

## Required minimum
- `phase-1`
- `phase-2`
- `phase-3`
- `phase-4`
- `phase-5`
- `epic`
- `enhancement`
- `codex`
- `bug`
- `qa`
- `documentation`
- `backend`
- `frontend`
- `ml`
- `priority:p1`
- `priority:p2`

This is enough to operate the roadmap cleanly.

---

# 3. LABEL APPLICATION RULES

## Rule 1
Every roadmap issue should have:
- exactly one phase label
- at least one type label

## Rule 2
Every Codex-ready issue should have:
- `codex`
- one phase label
- one area label
- one priority label

## Rule 3
Every epic issue should have:
- `epic`
- `roadmap`
- one phase label

## Rule 4
Every QA issue should have:
- `qa`
- related phase label

## Rule 5
Every bug issue should have:
- `bug`
- relevant phase label if known
- one priority label

---

# 4. LABEL EXAMPLES

## Example 1 — Phase epic
Issue:
`Phase 1 - Prediction Experience Upgrade`

Labels:
- `epic`
- `roadmap`
- `phase-1`
- `priority:p1`

## Example 2 — Small Codex backend task
Issue:
`Implement Phase 1 Task 1C - Add prediction history endpoint`

Labels:
- `codex`
- `enhancement`
- `phase-1`
- `backend`
- `api`
- `priority:p1`

## Example 3 — Full-stack feature task
Issue:
`Add route intelligence dashboard section`

Labels:
- `enhancement`
- `phase-2`
- `full-stack`
- `priority:p1`

## Example 4 — Regression bug
Issue:
`Bug - Prediction page crashes when history endpoint returns empty items`

Labels:
- `bug`
- `phase-1`
- `frontend`
- `priority:p0`

## Example 5 — QA check
Issue:
`QA - Verify Phase 3 monitoring and unknown-category warnings`

Labels:
- `qa`
- `phase-3`
- `priority:p1`

---

# 5. MILESTONE SET

Create milestones aligned to roadmap phases.

## Milestone 1
**Title:** `Phase 1 - Prediction Experience Upgrade`

### Scope
- prediction history
- typed responses
- risk band / severity band
- recommendations
- explanations

### Exit criteria
- all Phase 1 target tasks implemented
- QA issue passed
- README updated

---

## Milestone 2
**Title:** `Phase 2 - Analytics and Decision Support`

### Scope
- route intelligence
- airport congestion
- what-if simulation
- executive summary

### Exit criteria
- Phase 2 endpoints and UI working
- no regression in Phase 1
- QA issue passed

---

## Milestone 3
**Title:** `Phase 3 - ML Maturity Upgrade`

### Scope
- severity model
- delay reason prediction
- time-based validation
- unknown-category handling
- model monitoring

### Exit criteria
- training and prediction stable
- monitoring visible
- QA issue passed

---

## Milestone 4
**Title:** `Phase 4 - Aviation Operations Expansion`

### Scope
- turnaround risk
- delay propagation
- schedule scoring
- alerting

### Exit criteria
- operational workflows usable end-to-end
- earlier phases still stable
- QA issue passed

---

## Milestone 5
**Title:** `Phase 5 - External Data and Production Readiness`

### Scope
- weather integration
- dataset validation
- exports
- configuration hardening

### Exit criteria
- fallback logic works
- validation and export features work
- QA issue passed

---

## Optional extra milestone
**Title:** `Stabilization / Regression Hardening`

### Use when
- you want a dedicated cycle for bug fixes and cleanup between phases or before demo/release

---

# 6. MILESTONE CREATION ORDER

Create milestones in this order:

1. `Phase 1 - Prediction Experience Upgrade`
2. `Phase 2 - Analytics and Decision Support`
3. `Phase 3 - ML Maturity Upgrade`
4. `Phase 4 - Aviation Operations Expansion`
5. `Phase 5 - External Data and Production Readiness`
6. Optional: `Stabilization / Regression Hardening`

---

# 7. ISSUE NAMING CONVENTIONS

Use consistent issue titles.

## Epic format
`Phase X - <Phase Name>`

Examples:
- `Phase 1 - Prediction Experience Upgrade`
- `Phase 4 - Aviation Operations Expansion`

## Codex task format
`Implement Phase X Task Y - <Task Name>`

Examples:
- `Implement Phase 1 Task 1C - Add prediction history endpoint`
- `Implement Phase 2 Task 2.3B - Add simulate endpoint`

## QA format
`QA - Verify <scope>`

Examples:
- `QA - Verify Phase 1 prediction experience`
- `QA - Verify Phase 4 schedule scoring workflow`

## Bug format
`Bug - <short description>`

Examples:
- `Bug - Dashboard route intelligence table fails on empty dataset`
- `Bug - Auto-weather fallback not applied when provider fails`

## Docs format
`Docs - <short description>`

Examples:
- `Docs - Update README for prediction history endpoint`
- `Docs - Clarify Phase 3 monitoring workflow`

---

# 8. RECOMMENDED INITIAL EPIC ISSUES

Create these 5 epic issues first.

1. `Phase 1 - Prediction Experience Upgrade`
2. `Phase 2 - Analytics and Decision Support`
3. `Phase 3 - ML Maturity Upgrade`
4. `Phase 4 - Aviation Operations Expansion`
5. `Phase 5 - External Data and Production Readiness`

### Recommended labels for each epic
- `epic`
- `roadmap`
- corresponding phase label
- `priority:p1`

### Recommended milestone
- assign each epic to its matching milestone

---

# 9. RECOMMENDED FIRST TASK ISSUES

After epic creation, create these first task issues:

## Phase 1 starter set
1. `Implement Phase 1 Task 1A - Backend prediction persistence groundwork`
2. `Implement Phase 1 Task 1B - Save single prediction results to DB`
3. `Implement Phase 1 Task 1C - Add prediction history endpoint`
4. `Implement Phase 1 Task 1D - Add frontend types for history`
5. `Implement Phase 1 Task 1E - Render recent prediction history in UI`
6. `QA - Verify Phase 1 prediction history flow`

### Recommended labels for implementation tasks
- `codex`
- `enhancement`
- `phase-1`
- area label (`backend`, `frontend`, `full-stack`, etc.)
- `priority:p1`

### Recommended labels for QA issue
- `qa`
- `phase-1`
- `priority:p1`

---

# 10. PHASE-TO-MILESTONE MAPPING TABLE

| Phase | Milestone Title | Main Focus |
|---|---|---|
| Phase 1 | `Phase 1 - Prediction Experience Upgrade` | prediction UX and structure |
| Phase 2 | `Phase 2 - Analytics and Decision Support` | smarter dashboard and simulation |
| Phase 3 | `Phase 3 - ML Maturity Upgrade` | stronger model quality and trust |
| Phase 4 | `Phase 4 - Aviation Operations Expansion` | airline operations workflows |
| Phase 5 | `Phase 5 - External Data and Production Readiness` | external data, validation, export, config |

---

# 11. COPY CHECKLIST FOR REPO SETUP

Use this checklist when setting up the repo.

## Labels
- [ ] Create phase labels
- [ ] Create type labels
- [ ] Create area labels
- [ ] Create priority labels
- [ ] Create optional flow labels

## Milestones
- [ ] Create Phase 1 milestone
- [ ] Create Phase 2 milestone
- [ ] Create Phase 3 milestone
- [ ] Create Phase 4 milestone
- [ ] Create Phase 5 milestone
- [ ] Optional stabilization milestone

## Issues
- [ ] Create 5 epic issues
- [ ] Create first Phase 1 task issues
- [ ] Create first Phase 1 QA issue

## Project board
- [ ] Add issues to project board
- [ ] Set status fields
- [ ] Set phase fields
- [ ] Set priority and owner type

---

# 12. RECOMMENDED NEXT ACTIONS

1. Read `GITHUB_PROJECT_BOARD_STRUCTURE.md`
2. Create the labels listed in this file
3. Create the 5 phase milestones
4. Open the 5 epic issues
5. Open the first Phase 1 task issues
6. Add them to the GitHub Project board
7. Start execution with Phase 1 only

---

# End State

When this file is applied together with the roadmap and project board structure, the repository will have:
- a consistent label taxonomy
- clear milestone tracking
- cleaner issue naming
- easier phase management
- better Codex execution discipline
