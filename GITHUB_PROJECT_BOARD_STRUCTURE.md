# GITHUB_PROJECT_BOARD_STRUCTURE.md

## Purpose

This document defines a recommended **GitHub Project board structure** for managing the roadmap in this repository.

It is designed to work together with:
- `CODEX_IMPLEMENTATION_ROADMAP.md`
- `CODEX_TASKS_PHASE1.md`
- `CODEX_TASKS_PHASE2_PHASE3.md`
- `CODEX_TASKS_PHASE4_PHASE5.md`
- `.github/ISSUE_TEMPLATE/*`

The goal is to make roadmap execution easier for:
- the repository owner
- human contributors
- Codex
- reviewers and QA

---

## Recommended Project Name

Use one of these names:

- `Flight Delay Predictor Roadmap`
- `Aviation Decision Support Roadmap`
- `Flight Delay Platform Delivery Board`

Recommended default:

**`Aviation Decision Support Roadmap`**

---

## Recommended Board Type

Use a **GitHub Project (table + board views)**.

Recommended views:
1. **Roadmap Board** — Kanban-style execution tracking
2. **Roadmap Table** — full issue inventory with metadata
3. **Current Sprint** — filtered active work
4. **QA / Verification** — testing-focused view
5. **Codex Queue** — tasks ready to hand to Codex

---

# 1. BOARD COLUMNS

Use this column structure for the main board view:

## 1) Backlog
Use for:
- approved work not yet started
- future phase issues
- parked tasks waiting for prioritization

Typical items:
- future features
- low-priority tasks
- docs improvements not yet scheduled

## 2) Ready
Use for:
- clearly defined issues
- issues with acceptance criteria
- tasks that Codex or a developer can start immediately

Rule:
An issue should only move to **Ready** if:
- objective is clear
- scope is bounded
- dependency status is known
- roadmap reference is included

## 3) In Progress
Use for:
- work actively being implemented
- only one assignee or execution owner ideally

Rule:
Avoid putting too many issues here at once.
Prefer finishing small tasks.

## 4) In Review
Use for:
- work implemented and awaiting review
- PR open or code ready for review
- documentation and acceptance criteria being checked

## 5) QA / Validation
Use for:
- manual verification
- regression testing
- UI / API confirmation
- release-readiness checks for that task/phase

## 6) Blocked
Use for:
- dependency issues
- missing data/model/schema decision
- external service blockers
- unresolved bug blocking progress

Rule:
Blocked items should always have a note describing the blocker.

## 7) Done
Use for:
- implemented
- reviewed
- QA verified
- docs updated where needed

Definition:
Only move to **Done** when the issue truly meets definition of done.

---

# 2. RECOMMENDED CUSTOM FIELDS

In the GitHub Project, create these custom fields if possible:

## Status
Single select:
- Backlog
- Ready
- In Progress
- In Review
- QA / Validation
- Blocked
- Done

## Phase
Single select:
- Phase 1
- Phase 2
- Phase 3
- Phase 4
- Phase 5
- Cross-phase

## Work Type
Single select:
- Epic
- Feature
- Task
- Codex Task
- Bug
- QA
- Docs

## Priority
Single select:
- P0 Critical
- P1 High
- P2 Medium
- P3 Low

## Area
Single select:
- Backend
- Frontend
- ML
- Data
- Docs
- QA
- Full Stack

## Owner Type
Single select:
- Human
- Codex
- Shared

## Sprint
Text or single select:
- Sprint 1
- Sprint 2
- Sprint 3
- Future

## Dependency
Text field
Use to note parent issue, blocking task, or required milestone.

## Phase Order
Number field
Useful for sorting execution order.

Suggested values:
- 101, 102, 103 for Phase 1
- 201, 202, 203 for Phase 2
- 301, 302, 303 for Phase 3
- 401, 402, 403 for Phase 4
- 501, 502, 503 for Phase 5

---

# 3. RECOMMENDED LABELS

Use these GitHub labels.

## Roadmap / Phase labels
- `phase-1`
- `phase-2`
- `phase-3`
- `phase-4`
- `phase-5`
- `roadmap`

## Type labels
- `epic`
- `enhancement`
- `codex`
- `bug`
- `qa`
- `documentation`

## Area labels
- `backend`
- `frontend`
- `ml`
- `data`
- `full-stack`
- `ui`
- `api`

## Priority labels
- `priority:p0`
- `priority:p1`
- `priority:p2`
- `priority:p3`

## State / flow helper labels
- `blocked`
- `ready`
- `needs-review`
- `needs-qa`
- `good-first-task`

---

# 4. RECOMMENDED MILESTONES

Create milestones aligned to roadmap phases.

## Milestone 1 — Phase 1: Prediction Experience Upgrade
Scope:
- prediction history
- typed responses
- risk/severity bands
- recommendations
- explanations

## Milestone 2 — Phase 2: Analytics and Decision Support
Scope:
- route intelligence
- airport congestion
- simulation
- executive summary

## Milestone 3 — Phase 3: ML Maturity Upgrade
Scope:
- severity model
- reason prediction
- time-based validation
- unknown-category handling
- monitoring

## Milestone 4 — Phase 4: Aviation Operations Expansion
Scope:
- turnaround risk
- propagation
- schedule scoring
- alerting

## Milestone 5 — Phase 5: External Data and Production Readiness
Scope:
- weather integration
- data quality validation
- exports
- configuration hardening

Optional extra milestone:
- **`Stabilization / Regression Hardening`**

---

# 5. ISSUE MAPPING STRATEGY

## Epic issues
Create one epic issue per phase using:
- `.github/ISSUE_TEMPLATE/01_epic_phase.md`

Recommended epic issues:
- `Phase 1 - Prediction Experience Upgrade`
- `Phase 2 - Analytics and Decision Support`
- `Phase 3 - ML Maturity Upgrade`
- `Phase 4 - Aviation Operations Expansion`
- `Phase 5 - External Data and Production Readiness`

## Feature / task issues
Create one issue per roadmap task using:
- `.github/ISSUE_TEMPLATE/02_feature_task.md`
- `.github/ISSUE_TEMPLATE/03_codex_execution_task.md`

## Bug issues
Use:
- `.github/ISSUE_TEMPLATE/04_bug_report.md`

## QA issues
Use:
- `.github/ISSUE_TEMPLATE/05_qa_regression_check.md`

## Docs issues
Use:
- `.github/ISSUE_TEMPLATE/06_docs_improvement.md`

---

# 6. RECOMMENDED ISSUE HIERARCHY

Use this hierarchy:

## Level 1: Epic
One per phase.
Example:
- `Phase 1 - Prediction Experience Upgrade`

## Level 2: Task / Feature
Direct children or linked subtasks under the phase.
Examples:
- `Implement Phase 1 Task 1C - Add prediction history endpoint`
- `Implement Phase 1 Task 3A - Add risk band helper`

## Level 3: QA / Bug / Follow-up
Support issues created during validation.
Examples:
- `QA - Verify Phase 1 prediction history flow`
- `Bug - Prediction history list fails on empty state`

---

# 7. RECOMMENDED VIEW FILTERS

## View A — Roadmap Board
Layout:
- Board
Grouped by:
- Status

Filter:
- `is:open`

Use case:
- main execution dashboard

## View B — Roadmap Table
Layout:
- Table
Fields:
- Title
- Status
- Phase
- Work Type
- Priority
- Area
- Owner Type
- Sprint
- Dependency

Use case:
- master planning and triage

## View C — Current Sprint
Filter example:
- `Status:"Ready" OR Status:"In Progress" OR Status:"In Review" OR Status:"QA / Validation"`
- `Sprint:"Sprint 1"`

Use case:
- active short-term execution

## View D — Codex Queue
Filter example:
- `label:codex`
- `Status:"Ready"`

Use case:
- tasks safe to hand over directly to Codex

## View E — QA / Validation
Filter example:
- `label:qa OR Status:"QA / Validation"`

Use case:
- regression and acceptance tracking

## View F — Bugs
Filter example:
- `label:bug`
- `is:open`

Use case:
- defect triage and stabilization

---

# 8. RECOMMENDED PRIORITIZATION RULES

## Priority P0 Critical
Use only when:
- core app flow is broken
- model training is broken
- prediction is broken
- dashboard is unusable
- major regression blocks roadmap execution

## Priority P1 High
Use when:
- required current-phase task
- strong dependency for next steps
- significant user-facing value

## Priority P2 Medium
Use when:
- useful improvement
- non-blocking feature
- follow-up enhancement

## Priority P3 Low
Use when:
- docs polish
- minor UX improvement
- future optimization

---

# 9. RECOMMENDED EXECUTION RULES FOR THE BOARD

## Rule 1
Only move an issue into **Ready** when:
- scope is clear
- roadmap reference exists
- acceptance criteria are written

## Rule 2
Only one small implementation task should be assigned to Codex at a time when possible.

## Rule 3
Do not move an issue to **Done** unless:
- feature is implemented
- review complete
- QA complete
- docs updated if needed

## Rule 4
If a task creates regressions, open a bug issue and link it back to the parent task.

## Rule 5
Use QA issues at the end of each phase before closing the milestone.

---

# 10. RECOMMENDED INITIAL ISSUE SET

Create these issues first:

## Epics
1. `Phase 1 - Prediction Experience Upgrade`
2. `Phase 2 - Analytics and Decision Support`
3. `Phase 3 - ML Maturity Upgrade`
4. `Phase 4 - Aviation Operations Expansion`
5. `Phase 5 - External Data and Production Readiness`

## First operational tasks
6. `Implement Phase 1 Task 1A - Backend prediction persistence groundwork`
7. `Implement Phase 1 Task 1B - Save single prediction results to DB`
8. `Implement Phase 1 Task 1C - Add prediction history endpoint`
9. `Implement Phase 1 Task 1D - Add frontend types for history`
10. `Implement Phase 1 Task 1E - Render recent prediction history in UI`

## QA issue
11. `QA - Phase 1 verification`

---

# 11. EXAMPLE MAPPING TABLE

| Issue Type | Example Title | Phase | Label Suggestions | Status Start |
|---|---|---|---|---|
| Epic | Phase 1 - Prediction Experience Upgrade | Phase 1 | `epic`, `roadmap`, `phase-1` | Backlog |
| Codex Task | Implement Phase 1 Task 1C - Add prediction history endpoint | Phase 1 | `codex`, `enhancement`, `backend`, `phase-1` | Ready |
| Feature | Add route intelligence dashboard section | Phase 2 | `enhancement`, `frontend`, `phase-2` | Backlog |
| Bug | Bug - Simulation panel crashes on empty response | Phase 2 | `bug`, `frontend`, `priority:p1` | Ready |
| QA | QA - Verify Phase 3 monitoring page | Phase 3 | `qa`, `phase-3` | QA / Validation |
| Docs | Docs - Update README for weather enrichment flow | Phase 5 | `documentation`, `phase-5` | Ready |

---

# 12. SUGGESTED SPRINT BREAKDOWN

## Sprint 1
- Phase 1 tasks only

## Sprint 2
- Remaining Phase 1 QA
- Start Phase 2 route intelligence

## Sprint 3
- Complete Phase 2
- Begin Phase 3 severity model

## Sprint 4
- Complete Phase 3
- Begin Phase 4 turnaround and propagation

## Sprint 5
- Complete Phase 4
- Start Phase 5 weather/data quality/export work

---

# 13. CODEx-FRIENDLY PROJECT WORKFLOW

When creating an issue intended for Codex:
- use `03_codex_execution_task.md`
- include exact roadmap task reference
- keep issue scoped to one small implementation unit
- add labels:
  - `codex`
  - phase label
  - area label
  - priority label
- move to **Ready** only when details are sufficient

Recommended issue format:
- one task
- one acceptance target
- one reviewable code change set

---

# 14. MINIMUM OPERATING MODEL

If you want the simplest possible operating setup, use:

## Columns
- Backlog
- Ready
- In Progress
- In Review
- QA / Validation
- Done

## Labels
- `phase-1` to `phase-5`
- `codex`
- `bug`
- `qa`
- `documentation`
- `backend`
- `frontend`
- `ml`
- `priority:p1`
- `priority:p2`

## Milestones
- one milestone per phase

This minimal setup is enough to manage the whole roadmap.

---

# 15. RECOMMENDED NEXT ACTIONS

1. Create a new GitHub Project called **`Aviation Decision Support Roadmap`**
2. Add the status columns listed above
3. Create the recommended labels
4. Create milestones for Phase 1 through Phase 5
5. Open epic issues using the epic template
6. Open the first 5 Phase 1 tasks as Codex execution issues
7. Start with Phase 1 only
8. Use QA issue at the end of each phase before closing the milestone

---

# End State

When this board structure is applied, the repository should have:
- a clear roadmap execution system
- clean issue intake for Codex and humans
- visible phase progress
- controlled QA gates
- a scalable workflow for growing the aviation decision-support platform
