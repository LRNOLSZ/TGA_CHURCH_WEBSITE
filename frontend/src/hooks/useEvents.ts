import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, Event } from "@/types";

interface EventsParams {
  page?: number;
  category?: string;
  branch?: number;
  search?: string;
}

export function useEvents(params: EventsParams = {}) {
  return useQuery({
    queryKey: ["events", params],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Event>>("/api/events/", { params });
      return res.data;
    },
  });
}

export function useFeaturedEvents() {
  return useQuery({
    queryKey: ["events", "featured"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Event>>("/api/events/featured/");
      return res.data.results;
    },
  });
}

export function useEvent(id: number) {
  return useQuery({
    queryKey: ["event", id],
    queryFn: async () => {
      const res = await api.get<Event>(`/api/events/${id}/`);
      return res.data;
    },
    enabled: !!id,
  });
}
