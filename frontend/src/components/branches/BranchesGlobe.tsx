"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import createGlobe from "cobe";
import type { ContinentCode } from "@/types";
import { CONTINENT_CENTROIDS, locationToAngles, shortestAngleDelta, easeInOutCubic } from "./globeConstants";

interface SelectedCountry {
  lat: number;
  lng: number;
  name: string;
  isSatelliteOnly?: boolean;
}

const PHYSICAL_MARKER_COLOR: [number, number, number] = [0.79, 0.635, 0.29];
const SATELLITE_MARKER_COLOR: [number, number, number] = [0.72, 0.75, 0.8];

export default function BranchesGlobe({
  continent,
  country,
}: {
  continent: ContinentCode | null;
  country: SelectedCountry | null;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const widthRef = useRef(0);

  const phiRef = useRef(0);
  const thetaRef = useRef(0.15);
  const tweenRef = useRef<{ startPhi: number; endPhi: number; startTheta: number; endTheta: number; startTime: number } | null>(null);

  const pinAppearedAtRef = useRef<number | null>(null);
  const countryRef = useRef<SelectedCountry | null>(null);
  countryRef.current = country;
  const continentRef = useRef<ContinentCode | null>(null);
  continentRef.current = continent;

  // Kick off an eased rotation whenever the selected continent changes
  useEffect(() => {
    const target = continent ? CONTINENT_CENTROIDS[continent] : null;
    const [endPhi, endTheta] = target ? locationToAngles(target.lat, target.lng) : [phiRef.current, thetaRef.current];
    const startPhi = phiRef.current;
    const delta = shortestAngleDelta(startPhi, endPhi);
    tweenRef.current = {
      startPhi,
      endPhi: startPhi + delta,
      startTheta: thetaRef.current,
      endTheta,
      startTime: performance.now(),
    };
  }, [continent]);

  // Reset the pin "drop in" animation whenever the selected country changes
  useEffect(() => {
    pinAppearedAtRef.current = country ? performance.now() : null;
  }, [country?.name]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const updateWidth = () => {
      widthRef.current = canvas.offsetWidth;
    };
    updateWidth();
    window.addEventListener("resize", updateWidth);

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const globe = createGlobe(canvas, {
      devicePixelRatio: dpr,
      width: widthRef.current * dpr,
      height: widthRef.current * dpr,
      phi: 0,
      theta: 0.15,
      dark: 1,
      diffuse: 1.2,
      mapSamples: 14000,
      mapBrightness: 5,
      baseColor: [0.09, 0.15, 0.31],
      markerColor: [0.79, 0.635, 0.29],
      glowColor: [0.29, 0.35, 0.55],
      markers: [],
    });

    let animationFrame: number;

    const tick = () => {
      const now = performance.now();
      const tween = tweenRef.current;

      if (tween) {
        const t = Math.min((now - tween.startTime) / 1200, 1);
        const eased = easeInOutCubic(t);
        phiRef.current = tween.startPhi + (tween.endPhi - tween.startPhi) * eased;
        thetaRef.current = tween.startTheta + (tween.endTheta - tween.startTheta) * eased;
        if (t >= 1) tweenRef.current = null;
      } else if (!continentRef.current) {
        phiRef.current += 0.0025;
      }

      let markers: { location: [number, number]; size: number; color: [number, number, number] }[] = [];
      const activeCountry = countryRef.current;
      if (activeCountry) {
        const appearedAt = pinAppearedAtRef.current ?? now;
        const age = now - appearedAt;
        const baseSize = 0.045;
        let size: number;
        if (age < 400) {
          // spring-like scale-in with slight overshoot
          const t = age / 400;
          const overshoot = 1 - Math.pow(1 - t, 3) * Math.cos(t * 4);
          size = baseSize * Math.max(overshoot, 0);
        } else {
          // gentle continuous pulse once settled
          size = baseSize + Math.sin((age - 400) / 350) * 0.012;
        }
        markers = [{
          location: [activeCountry.lat, activeCountry.lng],
          size,
          color: activeCountry.isSatelliteOnly ? SATELLITE_MARKER_COLOR : PHYSICAL_MARKER_COLOR,
        }];
      }

      globe.update({
        phi: phiRef.current,
        theta: thetaRef.current,
        width: widthRef.current * dpr,
        height: widthRef.current * dpr,
        markers,
      });

      animationFrame = requestAnimationFrame(tick);
    };
    animationFrame = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(animationFrame);
      globe.destroy();
      window.removeEventListener("resize", updateWidth);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-[220px] md:w-[380px] aspect-square">
        <canvas
          ref={canvasRef}
          style={{ width: "100%", height: "100%", contain: "layout paint size" }}
        />
      </div>
      <AnimatePresence mode="wait">
        {country && (
          <motion.div
            key={country.name}
            initial={{ opacity: 0, y: 8, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, transition: { duration: 0.15 } }}
            transition={{ type: "spring", stiffness: 300, damping: 18 }}
            className="mt-4 flex items-center gap-2 px-4 py-1.5 rounded-full bg-navy-2 text-gold-soft text-sm font-medium"
          >
            <span
              className={`w-2 h-2 rounded-full animate-pulse ${country.isSatelliteOnly ? "bg-gray-300" : "bg-gold"}`}
            />
            {country.name}
            {country.isSatelliteOnly && (
              <span className="text-xs font-mono text-gray-300 uppercase tracking-wide">Online</span>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
