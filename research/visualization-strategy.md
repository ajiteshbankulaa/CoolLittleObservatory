# Visualization Strategy

## Core Direction
- Use one long-lived Cesium viewport as the visual anchor.
- Layer the interface above the scene with a top command bar, left mode rail, right detail drawer, and bottom timeline.
- Keep React responsible for shell and UI state while Cesium is updated imperatively through mode-specific scene controllers.

## Scene Rules
- Earth orbit uses globe, atmosphere, orbit paths, and follow-camera behavior.
- Solar system hides globe and renders scaled Sun-centered entities in a synthetic scene.
- NEO mode reuses the solar-system scene with close-approach emphasis.
- Deep-space mode uses curated points, labels, and context layers with restrained density.

## Performance Rules
- Prefer entity collections and data sources for moderate counts.
- Thin labels and cap dense satellite sets.
- Load secondary adornments after core geometry and selection state.
- Avoid Three.js in v1 unless Cesium proves insufficient for a concrete requirement.

## UX Rules
- The scene is primary; controls should not dominate it.
- Use restrained dark observatory styling, not noisy sci-fi chrome.
- Make freshness and source visible in the detail panel and command/search surfaces.
