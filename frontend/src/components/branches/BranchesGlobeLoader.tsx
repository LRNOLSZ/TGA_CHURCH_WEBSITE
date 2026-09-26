"use client";

import dynamic from "next/dynamic";
import { useInView } from "@/hooks/useInView";
import GlobePlaceholder from "./GlobePlaceholder";
import type { ContinentCode } from "@/types";

const LazyGlobe = dynamic(() => import("./BranchesGlobe"), {
  ssr: false,
  loading: () => <GlobePlaceholder />,
});

interface SelectedCountry {
  lat: number;
  lng: number;
  name: string;
  isSatelliteOnly?: boolean;
}

export default function BranchesGlobeLoader({
  continent,
  country,
}: {
  continent: ContinentCode | null;
  country: SelectedCountry | null;
}) {
  const { ref, inView } = useInView<HTMLDivElement>();

  return (
    <div ref={ref}>
      {inView ? <LazyGlobe continent={continent} country={country} /> : <GlobePlaceholder />}
    </div>
  );
}
