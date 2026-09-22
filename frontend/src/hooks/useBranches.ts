import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, Branch } from "@/types";

interface UseBranchesOptions {
  country?: string;
  region?: string;
  main?: boolean;
}

export function useBranches({ country, region, main }: UseBranchesOptions = {}) {
  return useQuery({
    queryKey: ["branches", country, region, main],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (country) params.set("country", country);
      if (region) params.set("region", region);
      if (main !== undefined) params.set("main", String(main));
      const res = await api.get<PaginatedResponse<Branch>>(`/api/branches/?${params.toString()}`);
      return res.data.results;
    },
  });
}
