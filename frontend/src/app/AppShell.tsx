import { Suspense, lazy, useDeferredValue, useEffect, useMemo, useState, startTransition } from "react";
import { useQuery } from "@tanstack/react-query";

import { CommandBar } from "@/components/chrome/CommandBar";
import { ModeRail } from "@/components/chrome/ModeRail";
import { TimelineBar } from "@/components/chrome/TimelineBar";
import { DetailPanel } from "@/components/panels/DetailPanel";
import { DiscoveryPanel } from "@/components/panels/DiscoveryPanel";
import { useLocalStorageState } from "@/hooks/useLocalStorageState";
import { api } from "@/lib/api";
import { MODES } from "@/lib/modes";
import { queryClient } from "@/lib/queryClient";
import type {
  DeepSpaceObject,
  FeaturedTour,
  FreshnessInfo,
  Mode,
  NeoObject,
  OrbitObject,
  SearchResult,
  SolarBody,
  UniverseEntity,
} from "@/types/api";


const SPEED_STEPS = [1, 30, 120, 600];
const CesiumViewport = lazy(() =>
  import("@/components/cesium/CesiumViewport").then((module) => ({
    default: module.CesiumViewport,
  })),
);

type DiscoveryView = "highlights" | "favorites" | "editorial";
type DetailPanelState = "open" | "minimized" | "closed";


function resolveEntityMode(entityId: string, lookup: Record<string, Mode>): Mode | undefined {
  return lookup[entityId];
}


function findStatusLabel(activeMode: Mode, freshness: Record<string, FreshnessInfo | undefined>) {
  const key =
    activeMode === "earth-orbit"
      ? "orbit"
      : activeMode === "solar-system"
        ? "solar"
        : activeMode === "neo"
          ? "neo"
          : activeMode === "deep-space"
            ? "deep"
            : "tours";
  return freshness[key]?.label ?? "Loading source state";
}


export function AppShell() {
  const [activeMode, setActiveMode] = useState<Mode>("earth-orbit");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedTourId, setSelectedTourId] = useState<string | null>(null);
  const [searchValue, setSearchValue] = useState("");
  const [favorites, setFavorites] = useLocalStorageState<string[]>("universe-favorites", []);
  const [playing, setPlaying] = useState(true);
  const [speed, setSpeed] = useState(SPEED_STEPS[2]);
  const [followSelection, setFollowSelection] = useState(true);
  const [simulatedTime, setSimulatedTime] = useState(() => new Date());
  const [navigationOpen, setNavigationOpen] = useLocalStorageState("observatory-nav-open", true);
  const [discoveryView, setDiscoveryView] = useLocalStorageState<DiscoveryView>("observatory-discovery-view", "highlights");
  const [detailPanelState, setDetailPanelState] = useLocalStorageState<DetailPanelState>("observatory-detail-state", "open");
  const deferredSearch = useDeferredValue(searchValue);

  const liveObjectsQuery = useQuery({ queryKey: ["live-objects"], queryFn: api.liveObjects });
  const stationsQuery = useQuery({ queryKey: ["orbit", "stations"], queryFn: api.orbitStations });
  const satellitesQuery = useQuery({ queryKey: ["orbit", "satellites"], queryFn: api.orbitSatellites });
  const solarBodiesQuery = useQuery({ queryKey: ["solar", "bodies"], queryFn: api.solarBodies });
  const neoFeedQuery = useQuery({ queryKey: ["neo", "feed"], queryFn: api.neoFeed });
  const deepSpaceQuery = useQuery({ queryKey: ["deep-space", "objects"], queryFn: api.deepSpaceObjects });
  const toursQuery = useQuery({ queryKey: ["featured", "tours"], queryFn: api.featuredTours });
  const apodQuery = useQuery({ queryKey: ["content", "apod"], queryFn: api.apod });
  const searchQuery = useQuery({
    queryKey: ["search", deferredSearch],
    queryFn: () => api.search(deferredSearch),
    enabled: deferredSearch.trim().length > 1,
  });

  const orbitObjects = useMemo(
    () => [...(stationsQuery.data?.data ?? []), ...(satellitesQuery.data?.data ?? [])],
    [satellitesQuery.data?.data, stationsQuery.data?.data],
  );
  const solarBodies = solarBodiesQuery.data?.data ?? [];
  const neoObjects = neoFeedQuery.data?.data ?? [];
  const deepSpaceObjects = deepSpaceQuery.data?.data ?? [];
  const tours = toursQuery.data?.data ?? [];

  const entityIndex = useMemo(() => {
    const map = new Map<string, UniverseEntity>();
    orbitObjects.forEach((item) => map.set(item.id, item));
    solarBodies.forEach((item) => map.set(item.id, item));
    neoObjects.forEach((item) => map.set(item.id, item));
    deepSpaceObjects.forEach((item) => map.set(item.id, item));
    tours.forEach((item) => map.set(item.id, item));
    return map;
  }, [deepSpaceObjects, neoObjects, orbitObjects, solarBodies, tours]);

  const entityModeLookup = useMemo(() => {
    const map: Record<string, Mode> = {};
    orbitObjects.forEach((item) => {
      map[item.id] = "earth-orbit";
    });
    solarBodies.forEach((item) => {
      map[item.id] = "solar-system";
    });
    neoObjects.forEach((item) => {
      map[item.id] = "neo";
    });
    deepSpaceObjects.forEach((item) => {
      map[item.id] = "deep-space";
    });
    tours.forEach((item) => {
      map[item.id] = "featured-tours";
    });
    return map;
  }, [deepSpaceObjects, neoObjects, orbitObjects, solarBodies, tours]);

  const favoriteEntities = useMemo(
    () =>
      favorites
        .map((id) => entityIndex.get(id))
        .filter((item): item is OrbitObject | SolarBody | NeoObject | DeepSpaceObject => Boolean(item && !("stops" in item))),
    [entityIndex, favorites],
  );

  const activeTour = useMemo<FeaturedTour | null>(
    () => tours.find((tour) => tour.id === selectedTourId) ?? null,
    [selectedTourId, tours],
  );

  const sceneMode: Exclude<Mode, "featured-tours"> =
    activeMode === "featured-tours" ? activeTour?.stops[0]?.mode ?? "earth-orbit" : activeMode;

  const effectiveSelectedId =
    activeMode === "featured-tours" ? activeTour?.stops[0]?.object_id ?? null : selectedId;
  const selectedEntity = effectiveSelectedId ? entityIndex.get(effectiveSelectedId) ?? null : null;
  const currentFreshness = {
    orbit: stationsQuery.data?.freshness,
    solar: solarBodiesQuery.data?.freshness,
    neo: neoFeedQuery.data?.freshness,
    deep: deepSpaceQuery.data?.freshness,
    tours: toursQuery.data?.freshness,
  };
  const statusLabel = findStatusLabel(activeMode, currentFreshness);
  const isFavorite = Boolean(selectedEntity && "id" in selectedEntity && favorites.includes(selectedEntity.id));
  const modeMeta = MODES.find((mode) => mode.id === activeMode);
  const viewportSelectionLabel =
    activeMode === "featured-tours"
      ? activeTour?.title ?? "Featured tour"
      : selectedEntity && "name" in selectedEntity
        ? selectedEntity.name
        : null;

  useEffect(() => {
    if (!playing) {
      return;
    }
    const handle = window.setInterval(() => {
      setSimulatedTime((current) => new Date(current.getTime() + speed * 1000));
    }, 1000);
    return () => window.clearInterval(handle);
  }, [playing, speed]);

  useEffect(() => {
    if (activeMode === "featured-tours") {
      if (!selectedTourId && tours[0]) {
        setSelectedTourId(tours[0].id);
      }
      return;
    }

    if (selectedId) {
      return;
    }

    const defaults: Record<Exclude<Mode, "featured-tours">, string | undefined> = {
      "earth-orbit": orbitObjects[0]?.id,
      "solar-system": solarBodies[0]?.id,
      neo: neoObjects[0]?.id,
      "deep-space": deepSpaceObjects[0]?.id,
    };
    const nextDefault = defaults[activeMode];
    if (nextDefault) {
      setSelectedId(nextDefault);
    }
  }, [activeMode, deepSpaceObjects, neoObjects, orbitObjects, selectedId, selectedTourId, solarBodies, tours]);

  const handleSelectMode = (mode: Mode) => {
    startTransition(() => {
      setActiveMode(mode);
      setSearchValue("");
      if (mode === "featured-tours") {
        setSelectedId(null);
      } else {
        setSelectedTourId(null);
      }
    });
  };

  const handlePrefetchMode = (mode: Mode) => {
    if (mode === "earth-orbit") {
      queryClient.prefetchQuery({ queryKey: ["orbit", "stations"], queryFn: api.orbitStations });
      queryClient.prefetchQuery({ queryKey: ["orbit", "satellites"], queryFn: api.orbitSatellites });
    }
    if (mode === "solar-system") {
      queryClient.prefetchQuery({ queryKey: ["solar", "bodies"], queryFn: api.solarBodies });
    }
    if (mode === "neo") {
      queryClient.prefetchQuery({ queryKey: ["neo", "feed"], queryFn: api.neoFeed });
    }
    if (mode === "deep-space") {
      queryClient.prefetchQuery({ queryKey: ["deep-space", "objects"], queryFn: api.deepSpaceObjects });
    }
    if (mode === "featured-tours") {
      queryClient.prefetchQuery({ queryKey: ["featured", "tours"], queryFn: api.featuredTours });
    }
  };

  const handleSelectObject = (id: string, modeOverride?: Mode) => {
    const mode = modeOverride ?? resolveEntityMode(id, entityModeLookup) ?? activeMode;
    startTransition(() => {
      if (mode === "featured-tours") {
        setActiveMode("featured-tours");
        setSelectedTourId(id);
      } else {
        setActiveMode(mode);
        setSelectedTourId(null);
        setSelectedId(id);
      }
      setDetailPanelState("open");
    });
  };

  const handleSelectSearchResult = (result: SearchResult) => {
    const mode = result.mode === "featured-tour" ? "featured-tours" : result.mode;
    handleSelectObject(result.id, mode);
    setSearchValue("");
  };

  const handleToggleFavorite = () => {
    if (!selectedEntity || !("id" in selectedEntity) || "stops" in selectedEntity) {
      return;
    }
    setFavorites((current) =>
      current.includes(selectedEntity.id) ? current.filter((item) => item !== selectedEntity.id) : [...current, selectedEntity.id],
    );
  };

  const detailFreshness =
    currentFreshness[
      activeMode === "earth-orbit"
        ? "orbit"
        : activeMode === "solar-system"
          ? "solar"
          : activeMode === "neo"
            ? "neo"
            : activeMode === "deep-space"
              ? "deep"
              : "tours"
    ] ?? {
      classification: "demo",
      label: "Loading",
      updated_at: new Date().toISOString(),
    };

  return (
    <main className={["app-shell", navigationOpen ? "nav-open" : "nav-closed", `detail-${detailPanelState}`].join(" ")}>
      <header className="topbar panel-shell">
        <div className="topbar__brand">
          <span className="eyebrow">Universe Visualizer</span>
          <div>
            <h1>Observatory Console</h1>
            <p>{modeMeta?.kicker}</p>
          </div>
        </div>

        <div className="topbar__modes">
          <ModeRail activeMode={activeMode} onSelectMode={handleSelectMode} onPrefetchMode={handlePrefetchMode} />
        </div>

        <CommandBar
          activeMode={activeMode}
          query={searchValue}
          onQueryChange={setSearchValue}
          onClearQuery={() => setSearchValue("")}
          onSelectResult={handleSelectSearchResult}
          results={searchQuery.data?.data ?? []}
          statusLabel={statusLabel}
          searching={searchQuery.isFetching}
          onToggleNavigation={() => setNavigationOpen((current) => !current)}
          onToggleDetails={() =>
            setDetailPanelState((current) => {
              if (current === "closed") {
                return "open";
              }
              return current === "open" ? "minimized" : "open";
            })
          }
          navigationOpen={navigationOpen}
          detailPanelState={detailPanelState}
        />
      </header>

      <div className="workspace-shell">
        <aside className={`workspace-panel workspace-panel--left ${navigationOpen ? "is-open" : "is-closed"}`}>
          {/* Keep navigation and discovery in one docked surface so the scene stays clear. */}
          <DiscoveryPanel
            activeMode={activeMode}
            liveObjects={liveObjectsQuery.data?.data}
            tours={tours}
            apod={apodQuery.data?.data}
            favorites={favoriteEntities}
            onSelectObject={handleSelectObject}
            onSelectTour={(tourId) => handleSelectObject(tourId, "featured-tours")}
            activeSection={discoveryView}
            onSectionChange={setDiscoveryView}
            loading={liveObjectsQuery.isLoading || toursQuery.isLoading}
            apodLoading={apodQuery.isLoading}
            hasError={Boolean(liveObjectsQuery.isError || toursQuery.isError || apodQuery.isError)}
          />
        </aside>

        <section className="viewport-stage">
          <div className="viewport-shell">
            <Suspense fallback={<div className="scene-loading panel-shell">Initializing observatory scene...</div>}>
              <CesiumViewport
                sceneMode={sceneMode}
                selectedId={effectiveSelectedId}
                followSelection={followSelection}
                playing={playing}
                speed={speed}
                orbitObjects={orbitObjects}
                solarBodies={solarBodies}
                neoObjects={neoObjects}
                deepSpaceObjects={deepSpaceObjects}
                onSelectObject={handleSelectObject}
              />
            </Suspense>
          </div>

          <div className="viewport-overlay">
            <div className="viewport-overlay__badge panel-shell">
              <span className="eyebrow">Viewport Focus</span>
              <strong>{viewportSelectionLabel ?? modeMeta?.label ?? "Observatory"}</strong>
              <p>{detailFreshness.label}</p>
            </div>
          </div>
        </section>

        <aside className={`workspace-panel workspace-panel--right state-${detailPanelState}`}>
          <DetailPanel
            activeMode={activeMode}
            entity={selectedEntity}
            activeTour={activeMode === "featured-tours" ? activeTour : null}
            freshness={detailFreshness}
            isFavorite={isFavorite}
            onToggleFavorite={handleToggleFavorite}
            panelState={detailPanelState}
            onClose={() => setDetailPanelState("closed")}
            onMinimize={() => setDetailPanelState("minimized")}
            onExpand={() => setDetailPanelState("open")}
          />
        </aside>
      </div>

      <TimelineBar
        activeMode={activeMode}
        playing={playing}
        speed={speed}
        follow={followSelection}
        currentTimeLabel={simulatedTime.toLocaleString()}
        onTogglePlaying={() => setPlaying((current) => !current)}
        onCycleSpeed={() =>
          setSpeed((current) => {
            const currentIndex = SPEED_STEPS.indexOf(current);
            return SPEED_STEPS[(currentIndex + 1) % SPEED_STEPS.length];
          })
        }
        onToggleFollow={() => setFollowSelection((current) => !current)}
      />
    </main>
  );
}
