import type { Mode, SearchResult } from "@/types/api";


type DetailPanelState = "open" | "minimized" | "closed";

interface CommandBarProps {
  activeMode: Mode;
  query: string;
  onQueryChange: (value: string) => void;
  onClearQuery: () => void;
  onSelectResult: (result: SearchResult) => void;
  results: SearchResult[];
  statusLabel: string;
  searching: boolean;
  onToggleNavigation: () => void;
  onToggleDetails: () => void;
  navigationOpen: boolean;
  detailPanelState: DetailPanelState;
}


export function CommandBar({
  activeMode,
  query,
  onQueryChange,
  onClearQuery,
  onSelectResult,
  results,
  statusLabel,
  searching,
  onToggleNavigation,
  onToggleDetails,
  navigationOpen,
  detailPanelState,
}: CommandBarProps) {
  const hasQuery = query.trim().length > 1;
  const detailLabel =
    detailPanelState === "open" ? "Inspector open" : detailPanelState === "minimized" ? "Inspector minimized" : "Inspector hidden";

  return (
    <div className="command-bar">
      <label className="command-input">
        <span className="command-input__icon">Search</span>
        <input
          type="text"
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Search objects, tours, and observatory targets"
          aria-label="Search observatory targets"
        />
        {query ? (
          <button type="button" className="ghost-button" onClick={onClearQuery}>
            Clear
          </button>
        ) : null}
      </label>

      <div className="command-bar__meta">
        <div className="command-pills">
          <span className="status-pill">{activeMode.replace("-", " ")}</span>
          <span className="status-pill subtle">{statusLabel}</span>
        </div>

        <div className="panel-toggle-row">
          <button type="button" className={`shell-toggle ${navigationOpen ? "is-active" : ""}`} onClick={onToggleNavigation}>
            {navigationOpen ? "Hide navigator" : "Show navigator"}
          </button>
          <button
            type="button"
            className={`shell-toggle ${detailPanelState !== "closed" ? "is-active" : ""}`}
            onClick={onToggleDetails}
            title={detailLabel}
          >
            {detailPanelState === "open" ? "Minimize inspector" : "Open inspector"}
          </button>
        </div>
      </div>

      {hasQuery ? (
        <div className="search-results panel-shell">
          {searching ? <div className="search-results__status">Searching the catalog...</div> : null}
          {!searching && results.length === 0 ? <div className="search-results__status">No matching objects yet.</div> : null}
          {results.map((result) => (
            <button
              key={`${result.mode}-${result.id}`}
              type="button"
              className="search-result"
              onClick={() => onSelectResult(result)}
            >
              <span className="search-result__mode">{result.mode}</span>
              <strong>{result.name}</strong>
              <p>{result.summary}</p>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
