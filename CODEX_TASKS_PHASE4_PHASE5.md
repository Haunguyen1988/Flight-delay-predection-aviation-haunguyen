# CODEX_TASKS_PHASE4_PHASE5.md

## Purpose

This document defines detailed, sequential Codex tasks for:
- **Phase 4 — Aviation Operations Expansion**
- **Phase 5 — External Data and Production Readiness**

These tasks assume:
- **Phase 1 is complete and stable**
- **Phase 2 is complete and stable**
- **Phase 3 is complete and stable**

---

## Global Constraints

Before starting Phase 4 or Phase 5, the following must still work:
- dashboard pages
- prediction page
- prediction history
- route intelligence
- airport congestion
- simulation
- model info and monitoring
- severity model behavior
- delay reason prediction
- existing upload / sample data / training flows

Do not do a large rewrite.
Prefer additive implementation.

For every task:
- identify impacted files
- add backend/service foundation first
- then add API endpoints
- then add frontend types/hooks/UI
- then update docs
- then verify no regressions

---

# Phase 4 — Aviation Operations Expansion

## Goal
Extend the product from flight-level prediction into airline operations support use cases.

## Phase 4 Features
1. Turnaround risk prediction
2. Delay propagation analysis
3. Next-day schedule scoring
4. Alerting rules

---

## Phase 4 Execution Order

1. Task 4.1A — Design operational data assumptions and minimal schema extensions
2. Task 4.1B — Add turnaround risk feature engineering foundation
3. Task 4.1C — Add turnaround risk endpoint
4. Task 4.1D — Add frontend turnaround risk view
5. Task 4.2A — Add delay propagation service foundation
6. Task 4.2B — Add delay propagation endpoint
7. Task 4.2C — Render delay propagation chain UI
8. Task 4.3A — Design schedule scoring ingestion contract
9. Task 4.3B — Add schedule scoring backend workflow
10. Task 4.3C — Add schedule scoring endpoint
11. Task 4.3D — Add schedule risk UI/page
12. Task 4.4A — Add alert rules engine
13. Task 4.4B — Expose alerts through relevant endpoints
14. Task 4.4C — Render alerts in frontend
15. Task 4.4D — Update README and perform Phase 4 QA

---

## Task 4.1A — Design operational data assumptions and minimal schema extensions

### Objective
Introduce the minimum data structures needed for operational analysis without overcomplicating the existing app.

### Requirements
Define how the app will represent operational linkage concepts such as:
- aircraft rotation linkage
- inbound flight reference
- outbound flight reference
- turnaround buffer or turn time

### Guidance
If the current dataset does not have real aircraft tail numbers, use a simplified or synthetic linkage approach first.
A minimal MVP is acceptable.

### Suggested deliverables
- design note in code comments or implementation summary
- minimal DB/schema additions only if truly needed
- avoid major migrations unless essential

### Suggested files
- `backend/app/models/flight.py`
- service/helper files in `backend/app/services/`
- any sample data or ingestion helpers if needed later

### Acceptance criteria
- turnaround logic has a clear data model assumption
- existing flight records and analytics are not broken

---

## Task 4.1B — Add turnaround risk feature engineering foundation

### Objective
Create logic that estimates outbound delay risk based on inbound conditions and available turnaround buffer.

### Requirements
Implement feature logic for at least:
- inbound delay minutes
- scheduled turnaround buffer
- route continuity or linked leg concept
- risk of insufficient turnaround time

### Guidance
The first version can be rule-based or hybrid ML + rule-based.
Do not block implementation on a perfect aircraft rotation model.

### Acceptance criteria
- backend can derive turnaround-related risk features from input data or linked schedule rows
- logic is reusable by endpoint layer

---

## Task 4.1C — Add turnaround risk endpoint

### Objective
Expose turnaround risk calculation via API.

### Requirements
Create endpoint:
- `POST /api/predict/turnaround-risk`

### Input should support
- inbound flight context
- outbound flight context
- optional explicit turnaround minutes

### Output should include
- outbound risk score
- estimated disruption severity
- turnaround sufficiency assessment
- top turnaround risk drivers
- recommendations

### Acceptance criteria
- endpoint returns useful turnaround assessment
- graceful handling when some optional fields are missing

---

## Task 4.1D — Add frontend turnaround risk view

### Objective
Allow users to run turnaround risk checks in the UI.

### Requirements
Add a dedicated section or page for turnaround risk.
Display:
- inbound summary
- outbound summary
- turnaround buffer
- risk band
- operational recommendations

### UI guidance
Keep it simple and task-focused.
Do not overload the existing Prediction page unless it fits cleanly.

### Acceptance criteria
- user can evaluate an inbound/outbound turn from the frontend
- UI is understandable and stable

---

## Task 4.2A — Add delay propagation service foundation

### Objective
Estimate how an initial delay can affect downstream flights.

### Requirements
Create backend logic that can model a simple disruption chain.
At minimum support:
- initial delayed leg
- linked subsequent legs
- cumulative impacted delay minutes
- number of impacted legs

### Guidance
The first version can assume a simple sequential chain rather than a full network graph.
Keep the model understandable.

### Acceptance criteria
- propagation service can produce a downstream impact summary
- logic does not depend on a perfect real-world network model

---

## Task 4.2B — Add delay propagation endpoint

### Objective
Expose disruption chain analysis via API.

### Requirements
Create endpoint:
- `POST /api/predict/propagation`

### Input should support
- initial flight or disrupted leg
- downstream linked flights or a simplified chain
- optional initial delay override

### Output should include
- impacted flights list
- cumulative impact
- max downstream delay
- propagation severity
- summary narrative

### Acceptance criteria
- endpoint returns a useful multi-leg impact assessment
- response is structured and frontend-friendly

---

## Task 4.2C — Render delay propagation chain UI

### Objective
Show downstream impact visually in frontend.

### Requirements
Add a page or section to render:
- ordered impacted legs
- delay carried forward
- total propagation impact
- major bottleneck point

### UI options
- simple vertical chain timeline
- compact table
- card sequence

### Acceptance criteria
- user can understand the delay chain without reading raw JSON

---

## Task 4.3A — Design schedule scoring ingestion contract

### Objective
Define how next-day schedule scoring data will be uploaded or passed to backend.

### Requirements
Design a simple, stable contract for schedule input.
Possible approaches:
- CSV upload with required columns
- JSON payload for batch schedule scoring

### Required minimum fields per schedule row
- flight number or flight identifier
- airline
- origin
- destination
- departure datetime
- optional aircraft or inbound linkage
- optional weather or operational metadata

### Acceptance criteria
- schedule scoring input contract is explicit and documented

---

## Task 4.3B — Add schedule scoring backend workflow

### Objective
Score an entire operating schedule instead of one flight at a time.

### Requirements
Create reusable backend workflow to:
- parse schedule input
- score each flight
- rank flights by risk
- aggregate risk by airport/time window
- identify top hot spots

### Output should support
- high-risk flights
- risky stations
- risky departure windows
- overall schedule risk snapshot

### Acceptance criteria
- backend can process multi-flight schedule scoring efficiently enough for MVP

---

## Task 4.3C — Add schedule scoring endpoint

### Objective
Expose schedule risk scoring via API.

### Requirements
Create endpoint such as:
- `POST /api/predict/schedule-risk`

### Response should include
- ranked flight risk list
- airport risk summary
- time-window hot spots
- overall summary metrics

### Acceptance criteria
- endpoint successfully scores a schedule batch
- output is structured for frontend display

---

## Task 4.3D — Add schedule risk UI/page

### Objective
Allow users to upload or submit a schedule and review ranked operational risk.

### Requirements
Create a new page or section showing:
- highest-risk flights
- top risky airports
- busiest risky time windows
- summary KPIs

### UI guidance
Focus on usability and prioritization.
The goal is to help the user know what to look at first.

### Acceptance criteria
- user can score a schedule and see prioritized results end-to-end

---

## Task 4.4A — Add alert rules engine

### Objective
Surface important operational warnings automatically.

### Requirements
Create a simple rule engine supporting rules such as:
- high delay risk above threshold
- severe turnaround insufficiency
- high propagation severity
- airport congestion spike
- deteriorating route conditions

### Guidance
Implement deterministic rules first.
Keep configuration simple.

### Acceptance criteria
- backend can generate alert objects consistently from risk outputs

---

## Task 4.4B — Expose alerts through relevant endpoints

### Objective
Attach alerts to the workflows that need them.

### Requirements
Expose alerts in relevant API responses where appropriate, for example:
- schedule scoring output
- turnaround risk output
- propagation output
- executive-style summaries if useful

### Acceptance criteria
- API responses include structured alert objects where useful
- alerts are not noisy or redundant

---

## Task 4.4C — Render alerts in frontend

### Objective
Make alerts visible and actionable in UI.

### Requirements
Render alerts using clear severity hierarchy.
Possible UI surfaces:
- alert panel on schedule risk page
- warning badges in turnaround view
- highlighted disruptions in propagation view

### Acceptance criteria
- user can identify urgent issues quickly
- alerts are readable and not overwhelming

---

## Task 4.4D — Update README and perform Phase 4 QA

### Objective
Document Phase 4 and verify operational workflows end-to-end.

### README updates
Must document:
- turnaround risk endpoint/page
- propagation endpoint/page
- schedule scoring endpoint/page
- alert rules concept

### Manual QA checklist
1. existing prediction still works
2. dashboard still works
3. simulation still works
4. turnaround risk endpoint works
5. turnaround UI works
6. propagation endpoint works
7. propagation UI works
8. schedule scoring endpoint works
9. schedule scoring UI/page works
10. alerts display correctly
11. no major regressions in earlier phases

### Acceptance criteria
- Phase 4 is stable and documented

---

# Phase 5 — External Data and Production Readiness

## Goal
Increase realism, data trustworthiness, and production-readiness patterns.

## Phase 5 Features
1. Weather API integration
2. Data quality validation center
3. Export reports
4. Configuration hardening

---

## Phase 5 Execution Order

1. Task 5.1A — Design weather provider abstraction
2. Task 5.1B — Add weather integration service
3. Task 5.1C — Expose weather-enriched prediction workflow
4. Task 5.1D — Add frontend support for auto-weather enrichment
5. Task 5.2A — Design dataset validation contract
6. Task 5.2B — Add upload validation backend logic
7. Task 5.2C — Render data quality validation results in UI
8. Task 5.3A — Design export formats and report scope
9. Task 5.3B — Add export endpoints
10. Task 5.3C — Add export UI actions
11. Task 5.4A — Audit current configuration handling
12. Task 5.4B — Refactor configuration management cleanly
13. Task 5.4C — Update README and perform Phase 5 QA

---

## Task 5.1A — Design weather provider abstraction

### Objective
Prepare the app to use external weather data without tightly coupling business logic to one provider.

### Requirements
Define a weather service abstraction that can:
- accept airport + datetime context
- return normalized weather features
- fail gracefully

### Guidance
Keep the first version provider-agnostic.
Support easy fallback to manual weather input or existing dataset weather values.

### Acceptance criteria
- there is a clear weather integration abstraction
- implementation is ready for one concrete provider

---

## Task 5.1B — Add weather integration service

### Objective
Integrate one weather data source in a safe MVP form.

### Requirements
Implement backend service that:
- queries weather for a given airport/date-time context
- normalizes the result into app-friendly weather fields
- handles API failure gracefully
- optionally caches or short-circuits if needed for MVP

### Constraints
Do not make external weather mandatory for prediction to work.
Fallback behavior must remain available.

### Acceptance criteria
- app can enrich predictions with external weather when available
- failures do not crash the app

---

## Task 5.1C — Expose weather-enriched prediction workflow

### Objective
Allow prediction to use automatic weather lookup when enabled.

### Requirements
Add support for prediction flow where weather can be:
- explicitly provided by user
- auto-fetched if not provided
- reported back in response metadata

### Response enhancements may include
- weather source used
- resolved weather condition
- fallback notice if manual/default weather was used

### Acceptance criteria
- prediction works with or without external weather enrichment
- behavior is transparent to users

---

## Task 5.1D — Add frontend support for auto-weather enrichment

### Objective
Let users choose between manual weather input and automatic enrichment.

### Requirements
Update Prediction UI to support:
- auto weather option
- clear display of resolved weather used in prediction
- fallback messaging if external weather is unavailable

### Acceptance criteria
- user can run enriched prediction from frontend
- UI remains clear and not confusing

---

## Task 5.2A — Design dataset validation contract

### Objective
Define what makes an uploaded dataset acceptable or problematic.

### Requirements
Create explicit validation rules for CSV/data upload, including:
- required columns
- optional columns
- type expectations
- duplicate handling
- null handling
- invalid airline or airport code behavior
- outlier detection strategy if included

### Acceptance criteria
- validation rules are explicit and implementable

---

## Task 5.2B — Add upload validation backend logic

### Objective
Validate uploaded datasets before or during ingestion.

### Requirements
Implement backend validation that can report:
- missing required columns
- invalid data types
- null counts
- duplicate rows
- invalid codes
- row-level issues summary

### Output should include
- validation status
- issues list
- warnings list
- safe summary counts

### Acceptance criteria
- invalid uploads are reported clearly
- upload does not fail silently

---

## Task 5.2C — Render data quality validation results in UI

### Objective
Show validation results clearly in Data Management UI.

### Requirements
Add UI support for:
- validation passed / warning / failed states
- issue summaries
- warnings summaries
- row counts and data quality metrics

### Acceptance criteria
- user can understand upload quality before trusting the data

---

## Task 5.3A — Design export formats and report scope

### Objective
Define useful exportable reports.

### Requirements
Choose at least one MVP export format first, preferably:
- CSV

Optional later:
- Excel
- PDF

### Candidate report scopes
- prediction history
- route intelligence
- executive summary
- schedule risk summary

### Acceptance criteria
- export scope is clear and tied to useful workflows

---

## Task 5.3B — Add export endpoints

### Objective
Allow users to download useful analytics outputs.

### Requirements
Create backend export endpoints for at least one of:
- prediction history export
- route intelligence export
- schedule risk export
- executive summary export

### Guidance
Start with CSV export.
Design endpoints so additional formats can be added later.

### Acceptance criteria
- user can successfully download at least one useful report

---

## Task 5.3C — Add export UI actions

### Objective
Expose export functionality in frontend.

### Requirements
Add export buttons in relevant pages or sections.
Examples:
- export prediction history
- export route intelligence
- export schedule risk summary

### Acceptance criteria
- export action is clear and functional from the UI

---

## Task 5.4A — Audit current configuration handling

### Objective
Understand how settings and environment variables are currently handled.

### Requirements
Review configuration usage for:
- backend env values
- frontend API base URL
- model paths
- feature toggles if needed
- weather integration configuration

### Deliverable
Implementation note or code summary identifying what should be centralized or cleaned up.

### Acceptance criteria
- current config usage is understood before refactor

---

## Task 5.4B — Refactor configuration management cleanly

### Objective
Improve maintainability of environment/config handling.

### Requirements
Refactor toward:
- centralized backend configuration pattern
- clear frontend API config usage
- safe defaults
- documented env variables

### Constraints
Do not introduce a large architectural framework just for config.
Keep it lightweight.

### Acceptance criteria
- config handling is cleaner and easier to maintain
- app behavior remains backward compatible

---

## Task 5.4C — Update README and perform Phase 5 QA

### Objective
Document external data and production-readiness improvements, then validate end-to-end stability.

### README updates
Must document:
- weather enrichment flow
- upload validation behavior
- export endpoints/actions
- configuration requirements
- any new environment variables

### Manual QA checklist
1. existing app startup still works
2. prediction still works without weather API
3. enriched prediction works when weather integration is available
4. fallback works when weather API fails
5. upload validation reports issues correctly
6. Data Management page displays validation results
7. export endpoints work
8. export UI works
9. configuration changes do not break local setup
10. no major regressions in earlier phases

### Acceptance criteria
- Phase 5 is stable and documented

---

# Guidance for Codex During Phase 4 and 5

## Prefer these patterns
- additive workflows
- deterministic MVP rules before advanced optimization
- clear schemas and typed responses
- graceful fallbacks for external dependencies
- frontend UX that prioritizes readability and actionability

## Avoid these mistakes
- do not make external weather a hard dependency
- do not overcomplicate rotation/network modeling in the first version
- do not mix all operational workflows into one overloaded page
- do not break earlier-phase prediction and dashboard features
- do not add excessive dependencies for exports or config unless truly justified

---

# Expected End State After Phase 5

The application should now support:
- turnaround risk analysis
- delay propagation analysis
- schedule-wide risk scoring
- operational alerting
- optional external weather enrichment
- data upload validation and quality reporting
- exportable reports
- cleaner configuration handling

At this point, the project should feel much closer to a practical aviation operations support platform rather than just a basic prediction demo.
