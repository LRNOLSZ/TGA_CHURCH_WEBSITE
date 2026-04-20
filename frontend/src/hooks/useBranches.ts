import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, Branch } from "@/types";

export function useBranches() {
  return useQuery({
    queryKey: ["branches"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Branch>>("/api/branches/");
      return res.data.results;
    },
  });
}
