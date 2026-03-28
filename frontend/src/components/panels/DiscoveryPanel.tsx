import type {
  ApodEntry,
  DeepSpaceObject,
  FeaturedTour,
  LiveObjectsPayload,
  Mode,
  NeoObject,
  OrbitObject,
  SolarBody,
} from "@/types/api";


type DiscoveryItem = OrbitObject | SolarBody | NeoObject | DeepSpaceObject;
type DiscoveryView = "highlights" | "favorites" | "editorial";

interface DiscoveryPanelProps {
  activeMode: Mode;
  liveObjects?: LiveObjectsPayload;
  tours?: FeaturedTour[];
  apod?: ApodEntry;
  favorites: DiscoveryItem[];
  onSelectObject: (id: string, mode?: Mode) => void;
  onSelectTour: (tourId: string) => void;
  activeSection: DiscoveryView;
  onSectionChange: (view: DiscoveryView) => void;
  loading: boolean;
  apodLoading: boolean;
  hasError: boolean;
}


function itemName(item: DiscoveryItem) {
  return "name" in item ? item.name : "";
}


function itemSummary(item: DiscoveryItem) {
  return "description" in item ? item.description : "";
}


export function DiscoveryPanel({
  activeMode,
  liveObjects,
  tours,
  apod,
  favorites,
  onSelectObject,
  onSelectTour,
  activeSection,
  onSectionChange,
  loading,
  apodLoading,
  hasError,
}: DiscoveryPanelProps) {
  const activeItems: DiscoveryItem[] =
    activeMode === "earth-orbit"
      ? liveObjects?.featured_orbit ?? []
      : activeMode === "solar-system"
        ? liveObjects?.solar_highlights ?? []
        : activeMode === "neo"
          ? liveObjects?.neo_watch ?? []
          : liveObjects?.deep_space_highlights ?? [];

  return (
    <div className="discovery-panel panel-shell">
      <div className="panel-header">
        <div>
          <span className="eyebrow">Navigator</span>
          <h2>Scene Library</h2>
        </div>
        <p>Browse highlights, reopen saved targets, or skim the editorial feed without covering the viewport.</p>
      </div>

      <div className="segmented-control" role="tablist" aria-label="Navigator sections">
        <button
          type="button"
          className={activeSection === "highlights" ? "is-active" : ""}
          onClick={() => onSectionChange("highlights")}
        >
          Highlights
        </button>
        <button
          type="button"
          className={activeSection === "favorites" ? "is-active" : ""}
          onClick={() => onSectionChange("favorites")}
        >
          Watchlist
        </button>
        <button
          type="button"
          className={activeSection === "editorial" ? "is-active" : ""}
          onClick={() => onSectionChange("editorial")}
        >
          Editorial
        </button>
      </div>

      {activeSection === "highlights" ? (
        <section className="panel-section">
          <div className="panel-section__heading">
            <span className="eyebrow">Interesting Now</span>
            <h3>{activeMode === "featured-tours" ? "Featured Runs" : "Mode Highlights"}</h3>
          </div>

          {loading ? <div className="empty-card">Loading scene highlights...</div> : null}
          {!loading && hasError ? <div className="empty-card">Highlights are temporarily unavailable.</div> : null}

          {!loading && !hasError ? (
            <div className="list-stack">
              {activeMode === "featured-tours"
                ? tours?.slice(0, 4).map((tour) => (
                    <button key={tour.id} type="button" className="list-card" onClick={() => onSelectTour(tour.id)}>
                      <strong>{tour.title}</strong>
                      <p>{tour.summary}</p>
                    </button>
                  ))
                : activeItems.map((item) => (
                    <button key={item.id} type="button" className="list-card" onClick={() => onSelectObject(item.id)}>
                      <strong>{itemName(item)}</strong>
                      <p>{itemSummary(item)}</p>
                    </button>
                  ))}
              {activeMode !== "featured-tours" && activeItems.length === 0 ? (
                <div className="empty-card">No highlights are loaded for this mode yet.</div>
              ) : null}
              {activeMode === "featured-tours" && !tours?.length ? (
                <div className="empty-card">No tours are available yet.</div>
              ) : null}
            </div>
          ) : null}
        </section>
      ) : null}

      {activeSection === "favorites" ? (
        <section className="panel-section">
          <div className="panel-section__heading">
            <span className="eyebrow">Favorites</span>
            <h3>Watchlist</h3>
          </div>

          <div className="list-stack">
            {favorites.length ? (
              favorites.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className="list-card compact"
                  onClick={() => onSelectObject(item.id)}
                >
                  <strong>{itemName(item)}</strong>
                  <p>{item.tags.slice(0, 3).join(" / ")}</p>
                </button>
              ))
            ) : (
              <div className="empty-card">Save objects from the inspector to keep a quick watchlist here.</div>
            )}
          </div>
        </section>
      ) : null}

      {activeSection === "editorial" ? (
        <section className="panel-section">
          <div className="panel-section__heading">
            <span className="eyebrow">Editorial Feed</span>
            <h3>Context</h3>
          </div>

          {apodLoading ? <div className="empty-card">Loading the latest editorial context...</div> : null}
          {!apodLoading && apod ? (
            <article className="apod-card">
              <span className="eyebrow">Astronomy Picture of the Day</span>
              <h2>{apod.title}</h2>
              <p>{apod.explanation}</p>
            </article>
          ) : null}
          {!apodLoading && !apod ? <div className="empty-card">Editorial context is unavailable right now.</div> : null}
        </section>
      ) : null}
    </div>
  );
}
