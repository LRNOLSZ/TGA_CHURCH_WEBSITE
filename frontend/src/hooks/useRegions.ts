import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { RegionSummary } from "@/types";

export function useRegions(countryId?: string) {
  return useQuery({
    queryKey: ["regions", countryId],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (countryId) params.set("country", countryId);
      const res = await api.get<RegionSummary[]>(`/api/regions/?${params.toString()}`);
      return res.data;
    },
    enabled: !!countryId,
  });
}
