import type { Mode } from "@/types/api";


export const MODES: Array<{
  id: Mode;
  label: string;
  shortLabel: string;
  kicker: string;
}> = [
  {
    id: "earth-orbit",
    label: "Earth Orbit",
    shortLabel: "Orbit",
    kicker: "Near-live satellites and stations",
  },
  {
    id: "solar-system",
    label: "Solar System",
    shortLabel: "Solar",
    kicker: "Heliocentric scene and planetary scale",
  },
  {
    id: "neo",
    label: "Asteroids / NEOs",
    shortLabel: "NEOs",
    kicker: "Close approaches, hazard filters, and small bodies",
  },
  {
    id: "deep-space",
    label: "Deep Space",
    shortLabel: "Deep",
    kicker: "Curated stars, nebulae, clusters, and context layers",
  },
  {
    id: "featured-tours",
    label: "Featured Tours",
    shortLabel: "Tours",
    kicker: "Guided observatory experiences",
  },
];
