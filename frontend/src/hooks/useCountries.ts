import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { CountrySummary, ContinentCode } from "@/types";

export function useCountries(continent?: ContinentCode) {
  return useQuery({
    queryKey: ["countries", continent],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (continent) params.set("continent", continent);
      const res = await api.get<CountrySummary[]>(`/api/countries/?${params.toString()}`);
      return res.data;
    },
    enabled: !!continent,
  });
}
