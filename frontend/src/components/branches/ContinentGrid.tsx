import { ContinentCode } from "@/types";
import { Globe2 } from "lucide-react";

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
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
      {CONTINENTS.map((continent) => (
        <button
          key={continent.code}
          onClick={() => onSelect(continent.code)}
          className="group flex flex-col items-center justify-center gap-3 py-8 px-4 border border-navy/10 rounded-xl bg-paper hover:border-gold hover:bg-navy transition-all duration-200"
        >
          <Globe2 size={28} className="text-gold-2 group-hover:text-gold transition" />
          <span className="font-display text-lg text-navy group-hover:text-white transition">
            {continent.label}
          </span>
        </button>
      ))}
    </div>
  );
}
