# CODEX_TASKS_PHASE2_PHASE3.md

## Purpose

This document defines detailed, sequential Codex tasks for:
- **Phase 2 — Analytics and Decision Support**
- **Phase 3 — ML Maturity Upgrade**

These tasks assume **Phase 1 is already complete and stable**.

---

## Global Constraints

Before starting Phase 2 or Phase 3:
- prediction history must still work
- typed prediction responses must still work
- risk/severity bands must still work
- recommendations and explanations must still work
- dashboard must still load correctly
- current analytics endpoints must remain usable unless intentionally superseded

Do not rewrite the app.
Prefer additive changes.

For each task:
- identify impacted files
- implement backend/service logic first
- expose API second
- update frontend types/hooks/UI third
- update docs last

---

# Phase 2 — Analytics and Decision Support

## Goal
Upgrade the app from descriptive dashboarding into actionable decision support.

## Phase 2 Features
1. Route intelligence
2. Airport congestion indicators
3. What-if simulation
4. Executive summary cards

---

## Phase 2 Execution Order

1. Task 2.1A — Refactor route analytics service foundation
2. Task 2.1B — Add route intelligence endpoint
3. Task 2.1C — Add frontend route intelligence types and UI
4. Task 2.2A — Add airport congestion metrics service
5. Task 2.2B — Add airport congestion endpoint
6. Task 2.2C — Render airport congestion section in dashboard
7. Task 2.3A — Design simulation request/response schema
8. Task 2.3B — Add simulate endpoint using current prediction engine
9. Task 2.3C — Add simulation UI in Prediction page
10. Task 2.4A — Add executive summary service
11. Task 2.4B — Add executive summary endpoint
12. Task 2.4C — Render executive summary cards in dashboard
13. Task 2.4D — Update README and perform Phase 2 QA

---

## Task 2.1A — Refactor route analytics service foundation

### Objective
Create a stronger route intelligence foundation from existing route analytics.

### Requirements
Inspect current route analytics implementation and extend it to support:
- total flights
- delayed flights
- delay rate
- avg delay minutes
- volume-aware risk score
- optional route stability score

### Guidance
Do not remove the existing route analytics behavior if it is already used by current dashboard charts.
Instead, build reusable aggregation logic that can support both old and new outputs.

### Suggested files
- `backend/app/services/data_processor.py`
- helper under `backend/app/services/` if needed

### Acceptance criteria
- backend has reusable route intelligence calculation logic
- existing route analytics are not broken

---

## Task 2.1B — Add route intelligence endpoint

### Objective
Expose richer route insights through a dedicated endpoint.

### Requirements
Create endpoint:
- `GET /api/flights/route-intelligence`

### Query parameters
Support at least:
- `top`
- optional `airline`
- optional `date_from`
- optional `date_to`

### Response fields per route
- route
- origin
- destination
- total_flights
- delayed_flights
- delay_rate
- avg_delay_minutes
- risk_score
- stability_score (optional)

### Acceptance criteria
- endpoint returns useful ranked route insights
- response is structured and frontend-friendly

---

## Task 2.1C — Add frontend route intelligence types and UI

### Objective
Display route intelligence on the dashboard.

### Requirements
Add frontend types and hook support for route intelligence.
Add a new dashboard section showing:
- top risky routes
- top unstable routes if available
- sortable route table or ranked cards

### UI notes
Keep existing dashboard intact and additive.
Do not remove current charts unless necessary.

### Suggested files
- `frontend/src/pages/Dashboard.tsx`
- `frontend/src/hooks/useApi.ts`
- `frontend/src/types/flight.ts`

### Acceptance criteria
- route intelligence is visible on dashboard
- empty/loading states are safe

---

## Task 2.2A — Add airport congestion metrics service

### Objective
Calculate operational pressure metrics by airport and time window.

### Requirements
Create reusable backend logic to compute metrics such as:
- airport code
- flights volume
- delayed flights
- delayed rate
- avg delay minutes
- departures per hour or grouped period
- congestion_score

### Guidance
Keep the first version simple and deterministic.
A formula-based congestion score is acceptable in Phase 2.

### Acceptance criteria
- congestion metrics can be computed from current dataset
- service logic is reusable by API layer

---

## Task 2.2B — Add airport congestion endpoint

### Objective
Expose airport congestion insights via API.

### Requirements
Create endpoint:
- `GET /api/flights/airport-congestion`

### Query parameters
Support at least:
- optional `group` (`hour`, `day`, or summary)
- optional `airport`
- optional `top`

### Response should support
- top congested airports
- top congested airport-time windows if grouped by time

### Acceptance criteria
- endpoint works on current data model
- response is structured and safe for UI consumption

---

## Task 2.2C — Render airport congestion section in dashboard

### Objective
Show airport pressure in the dashboard.

### Requirements
Add a dashboard section for airport congestion.
Possible UI choices:
- ranked table
- bar chart
- compact heatmap-like grouped display

### Acceptance criteria
- user can identify which airports/time windows are operationally pressured
- UI is readable and does not clutter the page

---

## Task 2.3A — Design simulation request/response schema

### Objective
Define a stable API contract for what-if simulation.

### Requirements
Create backend schemas for:
- base flight input
- scenario list input
- per-scenario output
- simulation API response

### Preferred behavior
Each scenario should allow one or more changes such as:
- departure time offset
- weather change
- custom label

### Acceptance criteria
- schemas are explicit and easy to use from frontend

---

## Task 2.3B — Add simulate endpoint using current prediction engine

### Objective
Allow users to compare alternate scenarios using the current predictor.

### Requirements
Create endpoint:
- `POST /api/predict/simulate`

### Behavior
- accept one base flight
- generate prediction for base case
- generate predictions for scenario cases
- return side-by-side output including deltas

### Example scenario presets to support
- depart 2 hours earlier
- depart 2 hours later
- improve weather
- worsen weather

### Output should include
- scenario label
- modified input summary
- delay probability
- estimated delay
- risk band
- delta vs base

### Acceptance criteria
- endpoint returns base + scenario comparisons
- endpoint safely reuses current prediction engine

---

## Task 2.3C — Add simulation UI in Prediction page

### Objective
Expose what-if analysis in the Prediction page.

### Requirements
Add simulation panel after or near prediction result.
Allow quick preset scenarios.
Render:
- base case
- scenario cards/table
- delta risk
- delta delay

### Acceptance criteria
- user can compare at least 3 scenarios visually
- no break to existing prediction workflow

---

## Task 2.4A — Add executive summary service

### Objective
Generate concise business-facing summary insights from current flight data.

### Requirements
Create backend service that produces at least:
- top disrupted route
- current delay trend insight
- dominant weather impact summary
- key operational message

### Guidance
Use deterministic summary rules derived from current analytics.
Do not generate vague or generic text.

### Acceptance criteria
- service returns short, useful executive-readable insights

---

## Task 2.4B — Add executive summary endpoint

### Objective
Expose dashboard summary insights.

### Requirements
Create endpoint:
- `GET /api/flights/executive-summary`

### Response should include
- summary cards or summary items
- concise labels and values
- optional short narrative text

### Acceptance criteria
- endpoint returns business-readable analytics summary

---

## Task 2.4C — Render executive summary cards in dashboard

### Objective
Add executive-friendly summary section to dashboard.

### Requirements
Render top-level summary cards such as:
- highest-risk route
- dominant disruption factor
- current delay trend
- high-level action cue

### UI notes
Keep language concise and management-friendly.

### Acceptance criteria
- dashboard becomes easier to read for non-technical users

---

## Task 2.4D — Update README and perform Phase 2 QA

### Objective
Document all Phase 2 additions and verify end-to-end stability.

### README updates
Must document:
- route intelligence
- airport congestion endpoint
- simulation endpoint
- executive summary endpoint
- dashboard enhancements

### Manual QA checklist
1. dashboard still loads
2. old route/weather/time analytics still work
3. route intelligence endpoint works
4. airport congestion endpoint works
5. executive summary endpoint works
6. simulation endpoint works
7. Prediction page still supports normal prediction
8. simulation UI renders correctly
9. no obvious regressions in existing pages

### Acceptance criteria
- Phase 2 is stable and documented

---

# Phase 3 — ML Maturity Upgrade

## Goal
Improve model realism, evaluation quality, and trustworthiness.

## Phase 3 Features
1. Severity model
2. Delay reason prediction
3. Time-based validation
4. Better unknown-category handling
5. Model monitoring

---

## Phase 3 Execution Order

1. Task 3.1A — Audit current ML training and prediction pipeline
2. Task 3.1B — Add severity target design and training flow
3. Task 3.1C — Expose severity model output in prediction API
4. Task 3.1D — Render severity model output in frontend
5. Task 3.2A — Add delay reason target preparation
6. Task 3.2B — Train delay reason model
7. Task 3.2C — Expose delay reason prediction via API
8. Task 3.2D — Render probable delay reason in frontend
9. Task 3.3A — Replace random split with time-based validation
10. Task 3.3B — Expose validation methodology and metrics in model info
11. Task 3.4A — Improve unknown-category handling
12. Task 3.4B — Add input warnings to prediction responses
13. Task 3.5A — Add model monitoring endpoint
14. Task 3.5B — Add model monitoring UI/page
15. Task 3.5C — Update README and perform Phase 3 QA

---

## Task 3.1A — Audit current ML training and prediction pipeline

### Objective
Understand the current ML pipeline before extending it.

### Requirements
Inspect and document current pipeline behavior for:
- feature engineering
- target variable
- train/test split
- saved artifacts
- prediction output fields
- model info endpoint usage

### Deliverable
A short implementation note in code comments or task summary describing how severity modeling will fit into the current architecture.

### Acceptance criteria
- extension plan is aligned with current predictor structure
- no code changes that break current training flow

---

## Task 3.1B — Add severity target design and training flow

### Objective
Train a dedicated model for delay severity instead of relying only on heuristic delay estimation.

### Requirements
Choose one of these approaches:
- regression for delay minutes, or
- classification into delay severity bands

### Preferred option
For simplicity and product clarity, classification into delay bands is acceptable if easier and more stable.

### Requirements
- prepare severity target from existing delay data
- train dedicated severity model
- save artifacts separately
- store severity metrics in model metadata

### Suggested outputs
- `predicted_delay_minutes` or
- `predicted_delay_band`
- optionally both if feasible

### Acceptance criteria
- severity model artifacts are saved and loadable
- training still completes successfully

---

## Task 3.1C — Expose severity model output in prediction API

### Objective
Return dedicated severity model output in prediction results.

### Requirements
Update prediction response to include one or both:
- `predicted_delay_band`
- `predicted_delay_minutes`

If severity model is not available, use safe fallback and return warning or graceful degrade behavior.

### Acceptance criteria
- prediction endpoint returns dedicated severity information when available
- API remains stable even if severity model is missing

---

## Task 3.1D — Render severity model output in frontend

### Objective
Display improved severity information in the Prediction page.

### Requirements
Update UI to show dedicated severity output distinctly from the earlier heuristic display.
If both heuristic and model-driven outputs exist temporarily, present one as primary and avoid confusion.

### Acceptance criteria
- severity output is understandable to users
- UI remains clean

---

## Task 3.2A — Add delay reason target preparation

### Objective
Prepare training data for delay reason prediction.

### Requirements
Inspect how `delay_reason` exists in current dataset and determine:
- valid class labels
- missing values handling
- whether to filter only delayed flights for reason training

### Acceptance criteria
- delay reason target preparation is well-defined and robust

---

## Task 3.2B — Train delay reason model

### Objective
Train a model that predicts likely delay reason.

### Requirements
- train dedicated reason model
- save artifacts separately
- store metrics in metadata

### Guidance
Keep first version simple.
Predicting among a manageable number of reason classes is enough.

### Acceptance criteria
- reason model can be trained and loaded
- training still completes without breaking current model pipeline

---

## Task 3.2C — Expose delay reason prediction via API

### Objective
Return probable delay reason in prediction output.

### Requirements
Add fields such as:
- `predicted_delay_reason`
- `top_reason_candidates` (optional if feasible)

If no reason model is available, fail gracefully.

### Acceptance criteria
- prediction endpoint can return reason information safely

---

## Task 3.2D — Render probable delay reason in frontend

### Objective
Show likely delay reason in the Prediction page.

### Requirements
Add UI component for:
- primary predicted delay reason
- optional top alternatives
- reason-aware action hint if available

### Acceptance criteria
- user can see probable reason without cluttering page

---

## Task 3.3A — Replace random split with time-based validation

### Objective
Make model evaluation more realistic for time-dependent flight data.

### Requirements
Replace or supplement random split with time-aware split.
Examples:
- older months for training
- newer months for validation/test

### Requirements
- avoid temporal leakage
- save validation setup metadata
- keep implementation understandable

### Acceptance criteria
- model evaluation reflects temporal ordering
- training still works with current dataset shape

---

## Task 3.3B — Expose validation methodology and metrics in model info

### Objective
Make evaluation methodology visible to users.

### Requirements
Update model info API to include:
- validation strategy
- train/test time ranges if available
- updated metrics
- model artifact readiness indicators

### Acceptance criteria
- model info is more trustworthy and transparent

---

## Task 3.4A — Improve unknown-category handling

### Objective
Handle unseen airline/airport values more safely.

### Requirements
Replace silent or weak fallback behavior with a safer strategy such as:
- explicit unknown token
- controlled fallback mapping
- domain warning generation

### Constraints
Do not make prediction fail just because an unknown category appears unless absolutely necessary.

### Acceptance criteria
- prediction remains robust for unseen inputs
- out-of-domain behavior is safer

---

## Task 3.4B — Add input warnings to prediction responses

### Objective
Inform users when input values are outside the trained domain.

### Requirements
Add `input_warnings` or similar field to prediction output.
Examples:
- unknown airline code
- unknown origin airport
- unknown destination airport
- untrained category fallback used

### Acceptance criteria
- warnings are user-visible and informative
- no breaking API behavior

---

## Task 3.5A — Add model monitoring endpoint

### Objective
Expose model health and readiness in one place.

### Requirements
Create endpoint:
- `GET /api/predict/monitoring`

### Response should include
- trained_at
- dataset size
- model versions or artifact names if available
- metrics summary
- severity model status
- reason model status
- validation strategy
- training duration if available

### Acceptance criteria
- users can inspect model readiness without reading files manually

---

## Task 3.5B — Add model monitoring UI/page

### Objective
Render monitoring information in frontend.

### Requirements
Add a new page or panel for model monitoring.
Show:
- model readiness
- key metrics
- validation method
- available artifacts
- trained timestamp

### Acceptance criteria
- model monitoring is readable and useful
- page does not interfere with current navigation patterns

---

## Task 3.5C — Update README and perform Phase 3 QA

### Objective
Document Phase 3 changes and validate end-to-end behavior.

### README updates
Must document:
- severity model
- delay reason prediction
- time-based validation
- unknown-category warnings
- monitoring endpoint/page

### Manual QA checklist
1. model training still works
2. prediction still works when only base models are available
3. prediction returns severity output when severity model exists
4. prediction returns reason output when reason model exists
5. model info reflects updated metrics
6. monitoring endpoint works
7. monitoring UI renders safely
8. unknown airline/airport inputs do not crash the app
9. warnings appear when appropriate
10. no regression in dashboard or prediction history flows

### Acceptance criteria
- Phase 3 is stable and documented

---

# Guidance for Codex During Phase 2 and 3

## Prefer these patterns
- additive API endpoints
- explicit schemas
- small helper modules
- thin routers
- frontend type safety

## Avoid these mistakes
- do not rebuild the entire dashboard
- do not hide old metrics without replacement
- do not tightly couple UI to unstable response fields
- do not make advanced model features mandatory for basic prediction to work

---

# Expected End State After Phase 3

The application should now support:
- richer route intelligence
- airport pressure insights
- what-if scenario comparison
- executive summary cards
- dedicated severity modeling
- probable delay reason prediction
- time-aware validation
- safer handling of unseen categories
- model monitoring and transparency
