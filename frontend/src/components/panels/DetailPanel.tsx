import type {
  FeaturedTour,
  FreshnessInfo,
  Mode,
  UniverseEntity,
} from "@/types/api";


type DetailPanelState = "open" | "minimized" | "closed";


function isFeaturedTour(entity: UniverseEntity | null, activeTour: FeaturedTour | null): activeTour is FeaturedTour {
  return Boolean(activeTour && (!entity || "stops" in activeTour));
}

function renderMetric(label: string, value: string | number | null | undefined) {
  if (value === undefined || value === null || value === "") {
    return null;
  }
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

interface DetailPanelProps {
  activeMode: Mode;
  entity: UniverseEntity | null;
  activeTour: FeaturedTour | null;
  freshness: FreshnessInfo;
  isFavorite: boolean;
  onToggleFavorite: () => void;
  panelState: DetailPanelState;
  onClose: () => void;
  onMinimize: () => void;
  onExpand: () => void;
}


export function DetailPanel({
  activeMode,
  entity,
  activeTour,
  freshness,
  isFavorite,
  onToggleFavorite,
  panelState,
  onClose,
  onMinimize,
  onExpand,
}: DetailPanelProps) {
  if (panelState === "closed") {
    return null;
  }

  const minimizedTitle = isFeaturedTour(entity, activeTour)
    ? activeTour.title
    : entity
      ? ("title" in entity ? entity.title : entity.name)
      : activeMode === "featured-tours"
        ? "Choose a guided tour"
        : "Select an object";

  if (panelState === "minimized") {
    return (
      <aside className="detail-panel detail-panel--minimized panel-shell">
        <button type="button" className="detail-panel__peek" onClick={onExpand}>
          <span className="eyebrow">Inspector</span>
          <strong>{minimizedTitle}</strong>
          <span>{freshness.label}</span>
        </button>
      </aside>
    );
  }

  if (isFeaturedTour(entity, activeTour)) {
    return (
      <aside className="detail-panel detail-panel--full panel-shell">
        <div className="detail-panel__toolbar">
          <div>
            <span className="eyebrow">Featured Tour</span>
            <h2>{activeTour.title}</h2>
          </div>
          <div className="panel-actions">
            <button type="button" className="ghost-button" onClick={onMinimize}>
              Minimize
            </button>
            <button type="button" className="ghost-button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
        <p>{activeTour.summary}</p>
        <div className="metric-grid">
          {renderMetric("Duration", `${activeTour.duration_minutes} min`)}
          {renderMetric("Stops", activeTour.stops.length)}
          {renderMetric("Freshness", freshness.label)}
        </div>
        <div className="list-stack">
          {activeTour.stops.map((stop) => (
            <div key={`${activeTour.id}-${stop.title}`} className="list-card compact static">
              <strong>{stop.title}</strong>
              <p>{stop.narrative}</p>
            </div>
          ))}
        </div>
      </aside>
    );
  }

  if (!entity) {
    return (
      <aside className="detail-panel detail-panel--full panel-shell">
        <div className="detail-panel__toolbar">
          <div>
            <span className="eyebrow">Inspector</span>
            <h2>{activeMode === "featured-tours" ? "Choose a guided tour" : "Select an object"}</h2>
          </div>
          <div className="panel-actions">
            <button type="button" className="ghost-button" onClick={onMinimize}>
              Minimize
            </button>
            <button type="button" className="ghost-button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
        <p>
          Details appear here in a fixed location so the scene stays readable. Search from the header or select a target in the
          viewport to inspect metrics, tags, and data freshness.
        </p>
        <div className="metric-grid">
          {renderMetric("Mode", activeMode.replace("-", " "))}
          {renderMetric("Freshness", freshness.label)}
        </div>
      </aside>
    );
  }

  const title = "title" in entity ? entity.title : entity.name;
  const summary = "summary" in entity ? entity.summary : entity.description;

  return (
    <aside className="detail-panel detail-panel--full panel-shell">
      <div className="detail-panel__toolbar">
        <div>
          <span className="eyebrow">Inspector</span>
          <h2>{title}</h2>
        </div>
        <div className="panel-actions">
          {"id" in entity ? (
            <button type="button" className={`favorite-button ${isFavorite ? "is-active" : ""}`} onClick={onToggleFavorite}>
              {isFavorite ? "Saved" : "Save"}
            </button>
          ) : null}
          <button type="button" className="ghost-button" onClick={onMinimize}>
            Minimize
          </button>
          <button type="button" className="ghost-button" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
      <p>{summary}</p>

      <div className="metric-grid">
        {"altitude_km" in entity ? renderMetric("Altitude", `${entity.altitude_km.toFixed(0)} km`) : null}
        {"speed_kps" in entity ? renderMetric("Velocity", `${entity.speed_kps.toFixed(2)} km/s`) : null}
        {"semi_major_axis_au" in entity ? renderMetric("Semi-major axis", `${entity.semi_major_axis_au.toFixed(2)} AU`) : null}
        {"relative_velocity_kps" in entity ? renderMetric("Approach speed", `${entity.relative_velocity_kps.toFixed(1)} km/s`) : null}
        {"miss_distance_km" in entity ? renderMetric("Miss distance", `${Math.round(entity.miss_distance_km).toLocaleString()} km`) : null}
        {"distance_ly" in entity ? renderMetric("Distance", `${entity.distance_ly?.toLocaleString()} ly`) : null}
        {renderMetric("Freshness", freshness.label)}
      </div>

      {"tags" in entity && entity.tags.length ? (
        <div className="tag-row">
          {entity.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      ) : null}
    </aside>
  );
}
