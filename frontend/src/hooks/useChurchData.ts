import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import {
  PaginatedResponse,
  ChurchInfo,
  HeadPastor,
  Leader,
  PhotoGallery,
  Testimony,
  GivingInfo,
  ServiceTime,
} from "@/types";

export function useChurchInfo() {
  return useQuery({
    queryKey: ["church-info"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<ChurchInfo>>("/api/church-info/");
      return res.data.results[0] ?? null;
    },
  });
}

export function useHeadPastor() {
  return useQuery({
    queryKey: ["head-pastor"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<HeadPastor>>("/api/head-pastor/");
      return res.data.results[0] ?? null;
    },
  });
}

export function useServiceTimes() {
  return useQuery({
    queryKey: ["service-times"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<ServiceTime>>("/api/service-times/");
      return res.data.results.filter((s) => s.is_active);
    },
  });
}

export function useLeaders() {
  return useQuery({
    queryKey: ["leaders"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Leader>>("/api/leaders/");
      return res.data.results;
    },
  });
}

export function useGallery(category?: string) {
  return useQuery({
    queryKey: ["gallery", category],
    queryFn: async () => {
      const params = category && category !== "All" ? { category } : {};
      const res = await api.get<PaginatedResponse<PhotoGallery>>("/api/gallery/", { params });
      return res.data.results;
    },
  });
}

export function useTestimonies() {
  return useQuery({
    queryKey: ["testimonies", "carousel"],
    queryFn: async () => {
      const res = await api.get<Testimony[]>("/api/testimonies/carousel/");
      return res.data;
    },
  });
}

export function useGivingInfo() {
  return useQuery({
    queryKey: ["giving-info"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<GivingInfo>>("/api/giving-info/");
      return res.data.results[0] ?? null;
    },
  });
}
