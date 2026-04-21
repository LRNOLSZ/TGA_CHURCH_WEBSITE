"use client";

import { useState } from "react";
import { useSermons } from "@/hooks/useSermons";
import SermonCard from "@/components/sermons/SermonCard";
import Pagination from "@/components/ui/Pagination";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { Search } from "lucide-react";

export default function SermonsPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [speaker, setSpeaker] = useState("");
  const [series, setSeries] = useState("");

  const { data, isLoading } = useSermons({
    page,
    search: search || undefined,
    speaker: speaker || undefined,
    series: series || undefined,
  });

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPage(1);
  };

  // Derive unique speakers/series from results for filter dropdowns
  const speakers = Array.from(new Set(data?.results.map((s) => s.speaker) ?? []));
  const seriesList = Array.from(new Set(data?.results.map((s) => s.series).filter(Boolean) ?? []));

  const filterInputStyle = {
    background: "#f1ebde",
    border: "1.5px solid rgba(11,30,63,0.18)",
    borderRadius: "3px",
    padding: "10px 16px",
    color: "#1a1a1a",
    fontSize: "14px",
  };

  return (
    <div className="bg-bg min-h-screen">
      <div className="bg-navy py-16 text-white text-center">
        <SectionHeader title="Messages & Sermons" subtitle="Be inspired and strengthened through the Word" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Filters */}
        <div className="p-5 mb-8 flex flex-col md:flex-row gap-4" style={{ background: "#f6efe0", borderRadius: "3px" }}>
          <form onSubmit={handleSearch} className="flex-1 flex gap-2">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search sermons..."
                className="w-full pl-9 pr-4 py-2.5 text-sm focus:outline-none"
                style={{ ...filterInputStyle, paddingLeft: "36px" }}
              />
            </div>
            <button type="submit" className="px-4 py-2 bg-navy text-white rounded-full text-sm font-medium transition-all duration-200 hover:bg-gold hover:text-navy">
              Search
            </button>
          </form>

          <select value={speaker} onChange={(e) => { setSpeaker(e.target.value); setPage(1); }} style={filterInputStyle} className="focus:outline-none">
            <option value="">All Speakers</option>
            {speakers.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>

          <select value={series} onChange={(e) => { setSeries(e.target.value); setPage(1); }} style={filterInputStyle} className="focus:outline-none">
            <option value="">All Series</option>
            {seriesList.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        {isLoading ? (
          <LoadingSpinner />
        ) : !data?.results.length ? (
          <div className="text-center py-20 font-mono text-muted text-sm">No sermons found.</div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.results.map((sermon) => (
                <SermonCard key={sermon.id} sermon={sermon} />
              ))}
            </div>
            <Pagination currentPage={page} totalCount={data.count} onPageChange={setPage} />
          </>
        )}
      </div>
    </div>
  );
}
