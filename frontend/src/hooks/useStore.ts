import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { PaginatedResponse, Book, Merchandise, ExchangeRate } from "@/types";

export function useBooks() {
  return useQuery({
    queryKey: ["books"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Book>>("/api/books/");
      return res.data.results;
    },
  });
}

export function useMerchandise() {
  return useQuery({
    queryKey: ["merchandise"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<Merchandise>>("/api/merchandise/");
      return res.data.results;
    },
  });
}

export function useExchangeRates() {
  return useQuery({
    queryKey: ["exchange-rates"],
    queryFn: async () => {
      const res = await api.get<PaginatedResponse<ExchangeRate>>("/api/exchange-rates/");
      return res.data.results;
    },
  });
}
