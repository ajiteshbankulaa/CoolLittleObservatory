export type FreshnessClass = "near-live" | "refreshed" | "curated" | "demo";
export type ResponseStatus = "ok" | "degraded" | "demo";
export type Mode = "earth-orbit" | "solar-system" | "neo" | "deep-space" | "featured-tours";

export interface WarningInfo {
  code: string;
  message: string;
  severity: "info" | "warning" | "error";
}

export interface SourceInfo {
  provider: string;
  dataset: string;
  classification: FreshnessClass;
  status: "ok" | "fallback" | "demo" | "unavailable";
  fetched_at?: string | null;
  epoch?: string | null;
  url?: string | null;
}

export interface FreshnessInfo {
  classification: FreshnessClass;
  label: string;
  updated_at: string;
  expires_at?: string | null;
  age_seconds?: number | null;
}

export interface ApiResponse<T> {
  status: ResponseStatus;
  freshness: FreshnessInfo;
  warnings: WarningInfo[];
  sources: SourceInfo[];
  data: T;
}

export interface OrbitPoint {
  timestamp: string;
  latitude: number;
  longitude: number;
  altitude_km: number;
  speed_kps: number;
}

export interface OrbitObject {
  id: string;
  name: string;
  norad_id?: number | null;
  category: string;
  subcategory?: string | null;
  description: string;
  operator?: string | null;
  country?: string | null;
  tags: string[];
  latitude: number;
  longitude: number;
  altitude_km: number;
  speed_kps: number;
  inclination_deg?: number | null;
  period_minutes?: number | null;
  tle_epoch?: string | null;
  trail: OrbitPoint[];
  ground_track: OrbitPoint[];
  visibility?: string | null;
  tracked: boolean;
}

export interface OrbitOverview {
  featured: OrbitObject[];
  stations: OrbitObject[];
  satellites: OrbitObject[];
}

export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

export interface SolarBody {
  id: string;
  name: string;
  kind: "star" | "planet" | "moon" | "dwarf-planet";
  description: string;
  color: string;
  radius_km: number;
  semi_major_axis_au: number;
  orbital_period_days?: number | null;
  position_au: Vector3;
  orbit_path_au: Vector3[];
  parent_id?: string | null;
  gravity_mps2?: number | null;
  tags: string[];
}

export interface NeoObject {
  id: string;
  name: string;
  designation: string;
  is_hazardous: boolean;
  close_approach: string;
  miss_distance_km: number;
  relative_velocity_kps: number;
  estimated_diameter_min_m: number;
  estimated_diameter_max_m: number;
  orbit_class?: string | null;
  position_au?: Vector3 | null;
  description: string;
  tags: string[];
}

export interface DeepSpaceObject {
  id: string;
  name: string;
  category:
    | "nearby-star"
    | "nebula"
    | "star-cluster"
    | "compact-object"
    | "exoplanet-system"
    | "galactic-context";
  constellation?: string | null;
  distance_ly?: number | null;
  right_ascension_deg?: number | null;
  declination_deg?: number | null;
  galactic_position?: Vector3 | null;
  description: string;
  tags: string[];
}

export interface ApodEntry {
  date: string;
  title: string;
  explanation: string;
  media_type: "image" | "video";
  url: string;
  hdurl?: string | null;
  copyright?: string | null;
}

export interface TourStop {
  object_id?: string | null;
  mode: "earth-orbit" | "solar-system" | "neo" | "deep-space";
  title: string;
  narrative: string;
  camera_hint?: string | null;
}

export interface FeaturedTour {
  id: string;
  title: string;
  summary: string;
  duration_minutes: number;
  tags: string[];
  stops: TourStop[];
}

export interface SearchResult {
  id: string;
  name: string;
  mode: "earth-orbit" | "solar-system" | "neo" | "deep-space" | "featured-tour";
  category: string;
  summary: string;
  tags: string[];
  freshness_label: string;
}

export interface LiveObjectsPayload {
  featured_orbit: OrbitObject[];
  solar_highlights: SolarBody[];
  neo_watch: NeoObject[];
  deep_space_highlights: DeepSpaceObject[];
}

export type UniverseEntity =
  | OrbitObject
  | SolarBody
  | NeoObject
  | DeepSpaceObject
  | FeaturedTour;
