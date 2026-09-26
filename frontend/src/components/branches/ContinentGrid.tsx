import { ContinentCode } from "@/types";

export const CONTINENTS: { code: ContinentCode; label: string }[] = [
  { code: "AF", label: "Africa" },
  { code: "AS", label: "Asia" },
  { code: "EU", label: "Europe" },
  { code: "NA", label: "North America" },
  { code: "SA", label: "South America" },
  { code: "OC", label: "Oceania" },
  { code: "AN", label: "Antarctica" },
];

export default function ContinentGrid({ onSelect }: { onSelect: (code: ContinentCode) => void }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
      {CONTINENTS.map((continent) => (
        <button
          key={continent.code}
          onClick={() => onSelect(continent.code)}
          className="group flex items-center justify-center text-center py-4 px-3 sm:py-8 sm:px-4 border border-navy/10 rounded-xl bg-paper hover:border-gold hover:bg-navy transition-all duration-200"
        >
          <span className="font-display text-sm sm:text-lg text-navy group-hover:text-white transition">
            {continent.label}
          </span>
        </button>
      ))}
    </div>
  );
}
