# Provider Landscape

## Cadence Model
- `near-live`: orbit objects from recent orbital elements, propagated locally
- `refreshed`: solar-system ephemerides, NEO feeds, and NASA media
- `curated`: deep-space catalogs, featured tours, and Milky Way context

## Recommended Provider Strategy
| Domain | Primary | Fallback | Notes |
| --- | --- | --- | --- |
| Orbit and stations | Space-Track GP or GP history in OMM or JSON | CelesTrak GP JSON feeds + cached last-known-good elements | Prefer modern OMM style fields and local propagation over raw provider-specific views |
| ISS and crewed stations | Orbit pipeline filtered to ISS and station classes | CelesTrak space stations group | Treat position as propagated state, not direct telemetry |
| Solar system | JPL Horizons | Cached ephemeris snapshots | Computed state with explicit epoch and refresh metadata |
| NEOs | NASA NeoWs | JPL SBDB details + cached feed | Use close-approach windows and hazard metadata carefully |
| NASA imagery/content | APOD, EPIC, images API | Local metadata cache | Refreshed or curated, not live |
| Deep space | SIMBAD, Gaia snapshots, NASA Exoplanet Archive, VizieR | Local curated snapshot | Heavy schema normalization and identity reconciliation required |

## Key Risks
- Space-Track requires credentials and throttles usage.
- CelesTrak is public but not truly real-time; aggressive polling is inappropriate.
- Horizons is authoritative but should be cached and queried with discipline.
- NeoWs demo keys are quota-limited.
- Deep-space catalogs have heterogeneous names, epochs, and units.

## Implementation Implications
- Always attach source, fetched time, epoch, and freshness class to normalized objects.
- Preserve raw provider IDs in metadata to support re-fetch and cross-identification.
- Keep demo datasets aligned with the same canonical schema used by live providers.
