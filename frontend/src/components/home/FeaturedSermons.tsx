"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useFeaturedSermons } from "@/hooks/useSermons";
import SermonCard from "@/components/sermons/SermonCard";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function FeaturedSermons() {
  const { data: sermons, isLoading } = useFeaturedSermons();

  return (
    <section className="bg-light py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionHeader title="Messages & Sermons" subtitle="Be inspired, encouraged and strengthened through the Word" />

        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sermons?.slice(0, 3).map((sermon) => (
              <SermonCard key={sermon.id} sermon={sermon} />
            ))}
          </div>
        )}

        <div className="text-center mt-10">
          <Link
            href="/sermons"
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-blue-800 transition-colors"
          >
            All Sermons <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
