import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, Sermon } from "@/types";

interface SermonsParams {
  page?: number;
  search?: string;
  speaker?: string;
  series?: string;
}

export function useSermons(params: SermonsParams = {}) {
  return useQuery({
    queryKey: ["sermons", params],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Sermon>>("/api/sermons/", { params });
      return res.data;
    },
  });
}

export function useFeaturedSermons() {
  return useQuery({
    queryKey: ["sermons", "featured"],
    queryFn: async () => {
      const res = await api.get<Sermon[]>("/api/sermons/featured/");
      return res.data;
    },
  });
}

export function useSermon(id: number) {
  return useQuery({
    queryKey: ["sermon", id],
    queryFn: async () => {
      const res = await api.get<Sermon>(`/api/sermons/${id}/`);
      return res.data;
    },
    enabled: !!id,
  });
}
