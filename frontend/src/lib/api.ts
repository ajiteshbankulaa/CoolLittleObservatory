import type {
  ApiResponse,
  ApodEntry,
  DeepSpaceObject,
  FeaturedTour,
  LiveObjectsPayload,
  NeoObject,
  OrbitObject,
  SearchResult,
  SolarBody,
} from "@/types/api";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";


async function fetchJson<T>(path: string): Promise<ApiResponse<T>> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed for ${path}: ${response.status}`);
  }
  return (await response.json()) as ApiResponse<T>;
}


export const api = {
  liveObjects: () => fetchJson<LiveObjectsPayload>("/objects/live"),
  orbitIss: () => fetchJson<OrbitObject>("/orbit/iss"),
  orbitStations: () => fetchJson<OrbitObject[]>("/orbit/stations"),
  orbitSatellites: () => fetchJson<OrbitObject[]>("/orbit/satellites"),
  orbitObject: (id: string) => fetchJson<OrbitObject>(`/orbit/object/${id}`),
  solarBodies: () => fetchJson<SolarBody[]>("/solar-system/bodies"),
  neoFeed: () => fetchJson<NeoObject[]>("/neo/feed"),
  deepSpaceObjects: () => fetchJson<DeepSpaceObject[]>("/deep-space/objects"),
  featuredTours: () => fetchJson<FeaturedTour[]>("/featured/tours"),
  apod: () => fetchJson<ApodEntry>("/content/apod"),
  search: (query: string) => fetchJson<SearchResult[]>(`/search?query=${encodeURIComponent(query)}`),
};
