# Universe Visualizer Agent Workflow

## Purpose
This project is built through a documented multi-agent workflow. The workflow is operational, not decorative: research and architecture outputs are written first, implementation agents must follow them, and review agents must critique completed work before a phase is considered done.

## Phase Order
1. Product definition
2. Data and provider research
3. Astronomy credibility review
4. Cesium and visualization strategy
5. Backend architecture
6. Frontend architecture
7. Data pipeline design
8. Backend implementation
9. Frontend implementation
10. Integration review
11. QA review
12. Performance review
13. Documentation and final polish

## Required First Movers
- `orchestrator` starts the workflow, opens the communication log, and assigns the first phase.
- `product_architect` defines scope boundaries and user journeys before any subsystem design is approved.
- `api_researcher`, `data_researcher`, and `astronomy_researcher` establish what data is live, refreshed, or curated before schemas are frozen.
- `cesium_specialist`, `backend_architect`, `frontend_architect`, and `ux_system_designer` turn research into technical designs.

## Handoff Rules
- All major updates go into [agents/communication.md](/C:/Users/ajite/OneDrive/Desktop/iss-tracker/agents/communication.md).
- Research agents hand off to `orchestrator`.
- `orchestrator` resolves gaps and hands off to architecture agents.
- Architecture agents hand off to implementation agents only after shared decisions are documented.
- Implementation agents must read the workflow, their own agent file, and the latest communication log before changing code.
- Review agents may block a phase by logging a concrete defect, drift, or missing coverage.

## Implementation Gates
- No implementation starts until:
  - product scope is defined
  - data classes are labeled `near-live`, `refreshed`, or `curated`
  - Cesium is confirmed as the primary visualization engine
  - backend and frontend response contracts are aligned
- Backend implementation must expose stable internal endpoints before frontend integration is considered complete.
- Frontend implementation must consume normalized backend contracts and must not encode provider-specific schemas.
- Documentation is incomplete until setup, architecture, demo-mode behavior, and provider caveats are written down.

## Review Checkpoints
- After backend implementation: `integration_reviewer` and `qa_reviewer`
- After frontend implementation: `integration_reviewer`, `qa_reviewer`, and `performance_reviewer`
- Before final delivery: `docs_writer` validates setup, environment, architecture, and workflow docs

## Conflict Resolution
1. Agents record the disagreement in the communication log with the affected subsystem and tradeoff.
2. `orchestrator` requests the smallest additional research needed to break the tie.
3. If the conflict is technical, the relevant architect owns the recommendation.
4. If the conflict affects scope or scientific honesty, `product_architect` and `astronomy_researcher` have veto priority.
5. The final decision is logged before the next phase begins.

## Escalation Path
- Provider uncertainty: `api_researcher` -> `data_researcher` -> `backend_architect` -> `orchestrator`
- Scientific credibility risk: `astronomy_researcher` -> `product_architect` -> `orchestrator`
- Rendering or performance risk: `cesium_specialist` -> `frontend_architect` -> `performance_reviewer`
- Schema drift: `integration_reviewer` -> `backend_architect` + `frontend_architect` -> `orchestrator`

## Communication Contract
Each meaningful entry in the communication log should include:
- `Date/Step`
- `Agent`
- `Goal`
- `Findings`
- `Decisions`
- `Dependencies`
- `Questions/Blockers`
- `Next Handoff`

## Working Agreement
- ISS tracking remains a feature inside a broader universe visualizer.
- CesiumJS is the primary visualization engine.
- Deep-space content must never be mislabeled as live telemetry.
- Demo mode must preserve the same API contracts as live mode.
- Reviewers critique work; they do not simply restate it.
