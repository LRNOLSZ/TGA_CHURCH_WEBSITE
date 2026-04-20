import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, HomeBanner } from "@/types";

export function useBanners() {
  return useQuery({
    queryKey: ["banners"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<HomeBanner>>("/api/banners/");
      return res.data.results.filter((b) => b.is_active);
    },
  });
}
