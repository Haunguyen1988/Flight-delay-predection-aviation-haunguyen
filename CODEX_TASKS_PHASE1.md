# CODEX_TASKS_PHASE1.md

## Purpose

This document breaks **Phase 1** into very small, sequential implementation tasks for Codex.

Phase 1 goal:
Upgrade the prediction experience without breaking current functionality.

Phase 1 includes:
1. Prediction history
2. Typed prediction response
3. Risk and severity bands
4. Recommendation engine
5. Lightweight explanation layer

---

## Important Constraints

Before making changes, preserve the following existing flows:
- `/api/predict`
- `/api/predict/batch`
- `/api/predict/train`
- `/api/predict/model/info`
- current Prediction page rendering
- current model training flow

Do not do a large refactor.
Prefer small, safe changes.

For each task:
- identify impacted files
- implement backend first
- then update frontend types/hooks/UI
- then update README
- then verify app still works

---

# Phase 1 Execution Order

Implement tasks in this exact order:

1. Task 1A — Backend prediction persistence groundwork
2. Task 1B — Save single prediction results to DB
3. Task 1C — Add prediction history endpoint
4. Task 1D — Add frontend types for history
5. Task 1E — Render recent prediction history in UI
6. Task 2A — Create typed schemas for prediction responses
7. Task 2B — Replace loose response models in prediction APIs
8. Task 3A — Add risk band helper
9. Task 3B — Add severity band helper
10. Task 3C — Render risk/severity bands in frontend
11. Task 4A — Add recommendation engine
12. Task 4B — Render recommendations in frontend
13. Task 5A — Add lightweight explanation engine
14. Task 5B — Render explanations in frontend
15. Task 5C — Update README for all Phase 1 additions
16. Task 5D — Final Phase 1 QA pass

---

# TASK DETAILS

---

## Task 1A — Backend prediction persistence groundwork

### Objective
Prepare backend structures required to save prediction records.

### Context
There is already a `predictions` table concept in the backend model layer, so reuse it if possible instead of creating a brand new table unless the schema is insufficient.

### Requirements
- Inspect existing prediction-related DB model
- Confirm whether current fields are enough to store:
  - airline
  - origin
  - destination
  - departure datetime
  - delay probability
  - estimated delay minutes
  - confidence
- If missing useful fields, extend minimally

### Preferred behavior
Keep schema changes minimal.

### Suggested backend files to inspect/update
- `backend/app/models/flight.py`
- database/session helper files under `backend/app/services/`
- any DB init file used by app startup

### Deliverable
- prediction persistence is technically ready
- no API contract change yet

### Acceptance criteria
- database model supports storing successful predictions
- no current endpoint behavior is broken

---

## Task 1B — Save single prediction results to DB

### Objective
Persist every successful single prediction.

### Requirements
Update `/api/predict` so that after a successful model prediction:
- the result is saved to DB
- failure to save should not crash the entire prediction if avoidable
- log DB save failures clearly

### Required stored fields
At minimum save:
- airline_code
- origin
- destination
- departure_datetime
- delay_probability
- estimated_delay_min
- confidence
- created_at

### Notes
- Only save when prediction succeeds
- Do not save failed or invalid prediction attempts
- Do not change current output shape yet in this task

### Suggested files
- `backend/app/routers/predict.py`
- create helper service if needed:
  - `backend/app/services/prediction_history.py`

### Acceptance criteria
- calling `/api/predict` creates a DB record
- API still returns success as before
- app still predicts normally

---

## Task 1C — Add prediction history endpoint

### Objective
Allow frontend to retrieve recent predictions.

### Requirements
Create new endpoint:
- `GET /api/predict/history`

### Query parameters
Support at least:
- `page`
- `limit`

Optional if easy:
- `airline`
- `origin`
- `destination`

### Response shape
Return structured data, not raw ORM objects.

Example target shape:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "created_at": "2026-04-07T10:00:00",
        "airline": "AA",
        "origin": "JFK",
        "destination": "LAX",
        "departure_datetime": "2025-12-20 17:30:00",
        "delay_probability": 0.64,
        "estimated_delay_minutes": 73,
        "confidence": "High"
      }
    ],
    "page": 1,
    "limit": 10,
    "total": 25,
    "total_pages": 3
  },
  "message": "OK"
}
```

### Requirements
- order by newest first
- safe pagination
- avoid exposing raw SQLAlchemy internals

### Suggested files
- `backend/app/routers/predict.py`
- helper service file if needed
- schemas file if introduced in later task can start here

### Acceptance criteria
- endpoint returns recent prediction history
- pagination works
- empty state works safely

---

## Task 1D — Add frontend types for history

### Objective
Prepare frontend to consume history data safely.

### Requirements
Add or extend TypeScript types for:
- prediction history item
- prediction history response
- paginated history collection

### Suggested files
- `frontend/src/types/flight.ts`

### Acceptance criteria
- frontend compiles cleanly
- no `any` type is required for history API response

---

## Task 1E — Render recent prediction history in UI

### Objective
Show recent predictions to the user.

### Requirements
Add a “Recent Predictions” section to the Prediction page.

### UI minimum fields
Display:
- route
- airline
- departure datetime
- delay probability
- estimated delay
- confidence
- created at

### UI behavior
- load recent history when page opens
- show loading state
- show empty state if no history exists
- do not break existing prediction result card

### Suggested files
- `frontend/src/pages/Prediction.tsx`
- `frontend/src/hooks/useApi.ts`

### Acceptance criteria
- recent predictions are visible
- existing prediction UI still works
- no crash when history list is empty

---

## Task 2A — Create typed schemas for prediction responses

### Objective
Move prediction APIs away from loose `dict` response models.

### Context
Prediction router currently uses generic response models for key endpoints. Replace this incrementally and safely.

### Requirements
Create Pydantic schemas for:
- single prediction result
- single prediction API response
- batch prediction item
- batch prediction API response
- model info response
- history item
- history list response

### Suggested location
- `backend/app/schemas/predict.py`

### Design guidance
Prefer explicit, readable schemas.

### Acceptance criteria
- schemas exist and are reusable
- no router is broken by introducing them

---

## Task 2B — Replace loose response models in prediction APIs

### Objective
Apply typed schemas to prediction router endpoints.

### Requirements
Update these endpoints to use explicit response models:
- `POST /api/predict`
- `POST /api/predict/batch`
- `GET /api/predict/model/info`
- `GET /api/predict/history`

### Rules
- keep API payload structure backward compatible where possible
- only improve structure, do not redesign everything

### Suggested files
- `backend/app/routers/predict.py`
- `backend/app/schemas/predict.py`

### Acceptance criteria
- endpoints use explicit response models
- frontend remains compatible after corresponding type updates

---

## Task 3A — Add risk band helper

### Objective
Translate delay probability into a readable risk level.

### Rules
Implement stable mapping:
- 0.00–0.19 => Very Low
- 0.20–0.39 => Low
- 0.40–0.59 => Moderate
- 0.60–0.79 => High
- 0.80–1.00 => Very High

### Requirements
- add helper function in backend
- inject `risk_band` into single prediction result
- inject `risk_band` into history records if practical

### Suggested files
- helper/service file under `backend/app/services/`
- prediction router
- optional schema updates

### Acceptance criteria
- every prediction result contains `risk_band`

---

## Task 3B — Add severity band helper

### Objective
Translate estimated delay minutes into a readable severity level.

### Rules
Implement stable mapping:
- 0–14 => On Time / Minimal
- 15–29 => Minor
- 30–59 => Moderate
- 60–119 => Major
- 120+ => Severe

### Requirements
- add helper function in backend
- inject `severity_band` into prediction result
- optionally expose in history payload

### Acceptance criteria
- every prediction result contains `severity_band`

---

## Task 3C — Render risk/severity bands in frontend

### Objective
Display readable classification, not only numbers.

### Requirements
On Prediction page:
- show risk band near probability
- show severity band near estimated delay
- if history includes these fields, show them in history list/table

### Suggested files
- `frontend/src/pages/Prediction.tsx`
- `frontend/src/types/flight.ts`

### Acceptance criteria
- user can interpret prediction at a glance
- UI remains clean and not overcrowded

---

## Task 4A — Add recommendation engine

### Objective
Return short action-oriented recommendations.

### Approach
Use rule-based logic first.

### Required output
Prediction response should include:
- `recommendations: string[]`

### Recommendation examples
- `"Monitor weather-related disruption risk closely"`
- `"Consider additional departure buffer during peak hour"`
- `"Use caution because model confidence is low"`
- `"Review downstream rotation impact if delay occurs"`

### Requirements
- produce at least 1 recommendation
- cap recommendations to a small, readable number
- avoid generic filler text

### Suggested backend files
- create helper:
  - `backend/app/services/prediction_recommendations.py`
- update schemas and router

### Acceptance criteria
- recommendations appear in prediction response
- recommendations change based on context

---

## Task 4B — Render recommendations in frontend

### Objective
Show actionable suggestions to the user.

### Requirements
Add a “Recommended Actions” card in Prediction page.

### UI behavior
- only show when prediction exists
- render as short bullet list
- must not visually dominate the page

### Acceptance criteria
- user sees recommendations after prediction
- no layout break on long or short lists

---

## Task 5A — Add lightweight explanation engine

### Objective
Explain why the predicted risk is high or low.

### Approach
Use simple rule-based explanations derived from input and feature engineering concepts.

### Suggested explanation drivers
- weather condition
- peak-hour departure
- season
- route characteristics
- departure timing

### Required output
Prediction response should include:
- `explanations: ExplanationItem[]`

Example item:
```json
{
  "factor": "Weather",
  "impact": "high",
  "message": "Rain, fog, or snow conditions increase delay risk"
}
```

### Requirements
- return 2–4 explanations when possible
- explanations must be specific enough to be useful
- do not implement SHAP in Phase 1 unless trivial

### Suggested backend files
- helper:
  - `backend/app/services/prediction_explanations.py`
- update schemas and router

### Acceptance criteria
- explanations appear in prediction response
- explanations reflect actual input context

---

## Task 5B — Render explanations in frontend

### Objective
Display “why this prediction” in UI.

### Requirements
Add a “Why this prediction?” card in Prediction page.

### UI behavior
For each explanation, show:
- factor
- impact
- short message

### Acceptance criteria
- explanations are readable
- card is hidden safely when no prediction exists

---

## Task 5C — Update README for Phase 1

### Objective
Document all new Phase 1 capabilities.

### Requirements
Update README sections:
- Features
- API Endpoints
- Prediction output description
- Any new endpoint examples

### Must include
- `/api/predict/history`
- risk band
- severity band
- recommendations
- explanations
- prediction history UI mention

### Acceptance criteria
- README matches implemented behavior

---

## Task 5D — Final Phase 1 QA pass

### Objective
Do a final verification sweep after all Phase 1 work.

### Manual QA checklist
1. backend starts without errors
2. frontend builds without errors
3. generate sample data still works
4. train model still works
5. single prediction still works
6. batch prediction still works
7. prediction is saved to history
8. history endpoint works
9. Prediction page loads history
10. Prediction page shows:
   - probability
   - estimated delay
   - confidence
   - risk band
   - severity band
   - recommendations
   - explanations
11. no obvious regressions in existing pages

### Acceptance criteria
- app is stable
- Phase 1 is complete end-to-end

---

# Implementation Notes for Codex

## Prefer these patterns
- create small helper functions instead of large monolithic logic
- keep router code slim
- keep UI changes additive, not disruptive

## Avoid these mistakes
- do not rewrite the whole prediction page
- do not rename existing endpoints unnecessarily
- do not break current model-info flow
- do not add heavy external dependencies for Phase 1

---

# Expected Phase 1 End State

After completing all tasks, the app should:
- save predictions to DB
- expose prediction history
- use explicit response schemas
- display risk band and severity band
- show recommendation text
- show explanation text
- keep existing dashboard/training/prediction flows working
