"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useFeaturedEvents } from "@/hooks/useEvents";
import EventCard from "@/components/events/EventCard";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function FeaturedEvents() {
  const { data: events, isLoading } = useFeaturedEvents();

  return (
    <section className="bg-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionHeader title="Upcoming Events" subtitle="Join us for worship, fellowship, and community" />

        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events?.slice(0, 3).map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        )}

        <div className="text-center mt-10">
          <Link
            href="/events"
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-blue-800 transition-colors"
          >
            View All Events <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
