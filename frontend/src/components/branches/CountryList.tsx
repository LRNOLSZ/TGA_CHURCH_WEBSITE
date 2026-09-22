import { useCountries } from "@/hooks/useCountries";
import { ContinentCode } from "@/types";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { MapPin } from "lucide-react";

export default function CountryList({
  continent,
  onSelect,
}: {
  continent: ContinentCode;
  onSelect: (countryId: number, countryName: string, lat: number | null, lng: number | null) => void;
}) {
  const { data: countries, isLoading } = useCountries(continent);

  if (isLoading) return <LoadingSpinner />;

  if (!countries?.length) {
    return <p className="text-center text-muted py-16">No branches in this continent yet.</p>;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {countries.map((country) => (
        <button
          key={country.id}
          onClick={() => onSelect(country.id, country.name, country.latitude, country.longitude)}
          className="flex items-center justify-between gap-3 p-5 border border-navy/10 rounded-xl bg-paper hover:border-gold transition text-left"
        >
          <div className="flex items-center gap-3">
            <MapPin size={18} className="text-gold-2 shrink-0" />
            <span className="font-medium text-navy">{country.name}</span>
          </div>
          <span className="text-xs font-mono text-muted whitespace-nowrap">
            {country.branch_count} {country.branch_count === 1 ? "branch" : "branches"}
          </span>
        </button>
      ))}
    </div>
  );
}
