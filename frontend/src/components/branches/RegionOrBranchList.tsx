import { useRegions } from "@/hooks/useRegions";
import { useBranches } from "@/hooks/useBranches";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import BranchCard from "@/components/branches/BranchCard";
import { MapPinned } from "lucide-react";

export default function RegionOrBranchList({
  countryId,
  regionId,
  onSelectRegion,
}: {
  countryId: number;
  regionId?: number;
  onSelectRegion: (regionId: number, regionName: string) => void;
}) {
  const countryIdStr = String(countryId);
  const { data: regions, isLoading: regionsLoading } = useRegions(countryIdStr);

  const hasRegions = (regions?.length ?? 0) > 0;
  const showBranchesDirectly = !hasRegions || !!regionId;

  const { data: branches, isLoading: branchesLoading } = useBranches({
    country: countryIdStr,
    region: regionId ? String(regionId) : undefined,
  });

  if (regionsLoading) return <LoadingSpinner />;

  if (!showBranchesDirectly) {
    if (!regions?.length) {
      return <p className="text-center text-muted py-16">No branches in this country yet.</p>;
    }
    return (
      <div className="grid grid-cols-1 gap-4">
        {regions.map((region) => (
          <button
            key={region.id}
            onClick={() => onSelectRegion(region.id, region.name)}
            className="flex items-center justify-between gap-3 p-5 border border-navy/10 rounded-xl bg-paper hover:border-gold transition text-left"
          >
            <div className="flex items-center gap-3 min-w-0">
              <MapPinned size={18} className="text-gold-2 shrink-0" />
              <span className="font-medium text-navy truncate">{region.name}</span>
            </div>
            <span className="text-xs font-mono text-muted whitespace-nowrap shrink-0">
              {region.branch_count} {region.branch_count === 1 ? "branch" : "branches"}
            </span>
          </button>
        ))}
      </div>
    );
  }

  if (branchesLoading) return <LoadingSpinner />;

  if (!branches?.length) {
    return <p className="text-center text-muted py-16">No branches found here yet.</p>;
  }

  return (
    <div className="grid grid-cols-1 gap-8">
      {branches.map((branch) => (
        <BranchCard key={branch.id} branch={branch} />
      ))}
    </div>
  );
}
