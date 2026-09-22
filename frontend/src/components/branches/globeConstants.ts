import type { ContinentCode } from "@/types";

// Approximate continent centroids (lat, lng in degrees) used to aim the
// globe's camera. Not precise geographic centroids — tuned for a
// visually-centered decorative rotation, not cartographic accuracy.
export const CONTINENT_CENTROIDS: Record<ContinentCode, { lat: number; lng: number }> = {
  AF: { lat: 2, lng: 20 },
  AS: { lat: 34, lng: 100 },
  EU: { lat: 54, lng: 15 },
  NA: { lat: 45, lng: -100 },
  SA: { lat: -15, lng: -60 },
  OC: { lat: -25, lng: 140 },
  AN: { lat: -90, lng: 0 },
};

/** Converts a lat/lng (degrees) into cobe's phi/theta camera-rotation angles. */
export function locationToAngles(lat: number, lng: number): [number, number] {
  return [
    Math.PI - ((lng * Math.PI) / 180 - Math.PI / 2),
    (lat * Math.PI) / 180,
  ];
}

/** Normalizes an angle delta into [-PI, PI] so rotation takes the shortest path. */
export function shortestAngleDelta(from: number, to: number): number {
  const delta = to - from;
  return ((delta + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
}

export function easeInOutCubic(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}
