"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useBranches } from "@/hooks/useBranches";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import FadeIn from "@/components/ui/FadeIn";
import Breadcrumb, { Crumb } from "@/components/ui/Breadcrumb";
import BranchCard from "@/components/branches/BranchCard";
import ContinentGrid, { CONTINENTS } from "@/components/branches/ContinentGrid";
import CountryList from "@/components/branches/CountryList";
import RegionOrBranchList from "@/components/branches/RegionOrBranchList";
import AntarcticaEasterEgg from "@/components/branches/AntarcticaEasterEgg";
import BranchesGlobeLoader from "@/components/branches/BranchesGlobeLoader";
import type { ContinentCode } from "@/types";

export default function BranchesPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const continent = searchParams.get("continent") as ContinentCode | null;
  const countryId = searchParams.get("country");
  const countryName = searchParams.get("countryName");
  const regionId = searchParams.get("region");
  const regionName = searchParams.get("regionName");
  const lat = searchParams.get("lat");
  const lng = searchParams.get("lng");

  const { data: mainBranchList, isLoading: mainLoading } = useBranches({ main: true });
  const main = mainBranchList?.[0];

  const globeCountry =
    continent !== "AN" && countryId && countryName && lat && lng
      ? { lat: Number(lat), lng: Number(lng), name: countryName }
      : null;

  const navigateTo = (params: Record<string, string | undefined>) => {
    const next = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) next.set(key, value);
    });
    router.push(`/branches?${next.toString()}`);
  };

  const continentLabel = CONTINENTS.find((c) => c.code === continent)?.label;

  const crumbs: Crumb[] = [
    { label: "All Continents", onClick: continent ? () => navigateTo({}) : undefined },
  ];
  if (continent) {
    crumbs.push({
      label: continentLabel ?? continent,
      onClick: countryId ? () => navigateTo({ continent }) : undefined,
    });
  }
  if (continent && countryId && countryName) {
    crumbs.push({
      label: countryName,
      onClick: regionId
        ? () => navigateTo({ continent, country: countryId, countryName, lat: lat ?? undefined, lng: lng ?? undefined })
        : undefined,
    });
  }
  if (regionId && regionName) {
    crumbs.push({ label: regionName });
  }

  return (
    <div className="bg-bg min-h-screen">
      <div className="bg-navy py-16 text-center">
        <SectionHeader title="Our Branches" subtitle="Find a TGA Church near you" light />
      </div>

      <div className="bg-navy-2 py-12">
        <BranchesGlobeLoader continent={continent} country={globeCountry} />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Main Branch — always pinned at the top */}
        {mainLoading ? (
          <LoadingSpinner />
        ) : (
          main && (
            <FadeIn>
              <div className="mb-16">
                <div className="flex items-center gap-2 mb-6">
                  <span className="bg-accent text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Main Branch</span>
                </div>
                <BranchCard branch={main} featured />
              </div>
            </FadeIn>
          )
        )}

        <FadeIn delay={0.1}>
          <Breadcrumb crumbs={crumbs} />

          {!continent && (
            <ContinentGrid onSelect={(code) => navigateTo({ continent: code })} />
          )}

          {continent === "AN" && <AntarcticaEasterEgg />}

          {continent && continent !== "AN" && !countryId && (
            <CountryList
              continent={continent}
              onSelect={(id, name, selectedLat, selectedLng) =>
                navigateTo({
                  continent,
                  country: String(id),
                  countryName: name,
                  lat: selectedLat != null ? String(selectedLat) : undefined,
                  lng: selectedLng != null ? String(selectedLng) : undefined,
                })
              }
            />
          )}

          {continent && countryId && (
            <RegionOrBranchList
              countryId={Number(countryId)}
              regionId={regionId ? Number(regionId) : undefined}
              onSelectRegion={(id, name) =>
                navigateTo({
                  continent,
                  country: countryId,
                  countryName: countryName ?? undefined,
                  lat: lat ?? undefined,
                  lng: lng ?? undefined,
                  region: String(id),
                  regionName: name,
                })
              }
            />
          )}
        </FadeIn>
      </div>
    </div>
  );
}
