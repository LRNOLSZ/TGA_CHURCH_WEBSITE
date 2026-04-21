"use client";

import { useState } from "react";
import { useEvents } from "@/hooks/useEvents";
import EventCard from "@/components/events/EventCard";
import Pagination from "@/components/ui/Pagination";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import { Search } from "lucide-react";

const CATEGORIES = ["All", "General", "Conference", "Outreach", "Worship Night", "Healing to the city", "Other"];

export default function EventsPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  const { data, isLoading } = useEvents({
    page,
    search: search || undefined,
    category: category || undefined,
  });

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPage(1);
  };

  return (
    <div className="bg-bg min-h-screen">
      {/* Header */}
      <div className="bg-navy py-16 text-white text-center">
        <SectionHeader title="Upcoming Events" subtitle="Join us for worship, fellowship, and community" light />
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
                placeholder="Search events..."
                className="w-full pl-9 pr-4 py-2.5 text-sm focus:outline-none"
                style={{
                  background: "#f1ebde",
                  border: "1.5px solid rgba(11,30,63,0.18)",
                  borderRadius: "3px",
                  color: "#1a1a1a",
                }}
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 bg-navy text-white rounded-full text-sm transition-all duration-200 hover:bg-gold hover:text-navy font-medium"
            >
              Search
            </button>
          </form>

          <select
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="text-sm focus:outline-none"
            style={{
              background: "#f1ebde",
              border: "1.5px solid rgba(11,30,63,0.18)",
              borderRadius: "3px",
              padding: "10px 16px",
              color: "#1a1a1a",
            }}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c === "All" ? "" : c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Results */}
        {isLoading ? (
          <LoadingSpinner />
        ) : !data?.results.length ? (
          <div className="text-center py-20 font-mono text-muted text-sm">No events found.</div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.results.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
            <Pagination
              currentPage={page}
              totalCount={data.count}
              onPageChange={setPage}
            />
          </>
        )}
      </div>
    </div>
  );
}
