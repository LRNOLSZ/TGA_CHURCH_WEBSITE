import { useCountries } from "@/hooks/useCountries";
import { ContinentCode } from "@/types";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { MapPin } from "lucide-react";

export default function CountryList({
  continent,
  onSelect,
}: {
  continent: ContinentCode;
  onSelect: (
    countryId: number,
    countryName: string,
    lat: number | null,
    lng: number | null,
    isSatelliteOnly: boolean
  ) => void;
}) {
  const { data: countries, isLoading } = useCountries(continent);

  if (isLoading) return <LoadingSpinner />;

  if (!countries?.length) {
    return <p className="text-center text-muted py-16">No branches in this continent yet.</p>;
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {countries.map((country) => (
        <button
          key={country.id}
          onClick={() =>
            onSelect(
              country.id,
              country.name,
              country.latitude,
              country.longitude,
              country.branch_count > 0 && !country.has_physical_branch
            )
          }
          className="flex items-center justify-between gap-3 p-5 border border-navy/10 rounded-xl bg-paper hover:border-gold transition text-left"
        >
          <div className="flex items-center gap-3 min-w-0">
            <MapPin size={18} className="text-gold-2 shrink-0" />
            <span className="font-medium text-navy truncate">{country.name}</span>
          </div>
          <span className="text-xs font-mono text-muted whitespace-nowrap shrink-0">
            {country.branch_count} {country.branch_count === 1 ? "branch" : "branches"}
          </span>
        </button>
      ))}
    </div>
  );
}
