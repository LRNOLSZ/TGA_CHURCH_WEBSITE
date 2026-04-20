"use client";

import { useParams } from "next/navigation";
import { Calendar, User, BookOpen, Clock } from "lucide-react";
import { useSermon } from "@/hooks/useSermons";
import { formatDate, getYouTubeEmbedUrl } from "@/lib/utils";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import Link from "next/link";

export default function SermonDetailPage() {
  const { id } = useParams();
  const { data: sermon, isLoading } = useSermon(Number(id));

  if (isLoading) return <LoadingSpinner className="py-40" />;
  if (!sermon) return <div className="text-center py-40 text-gray-500">Sermon not found.</div>;

  const embedUrl = getYouTubeEmbedUrl(sermon.video_url);

  return (
    <div className="bg-light min-h-screen">
      {/* Video */}
      <div className="bg-dark py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {embedUrl ? (
            <div className="relative w-full" style={{ paddingTop: "56.25%" }}>
              <iframe
                src={embedUrl}
                title={sermon.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="absolute inset-0 w-full h-full rounded-xl"
              />
            </div>
          ) : (
            <div className="h-64 bg-gray-800 rounded-xl flex items-center justify-center text-gray-400">
              Video not available
            </div>
          )}
        </div>
      </div>

      {/* Details */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="bg-white rounded-2xl shadow-md p-8">
          {sermon.series && (
            <span className="inline-block bg-primary/10 text-primary text-xs font-semibold px-3 py-1 rounded-full mb-3">
              {sermon.series}
            </span>
          )}
          <h1 className="text-2xl md:text-3xl font-bold text-text-main mb-6">{sermon.title}</h1>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 pb-8 border-b border-gray-100">
            <div className="flex items-center gap-2 text-gray-600 text-sm">
              <User size={15} className="text-accent" />{sermon.speaker}
            </div>
            <div className="flex items-center gap-2 text-gray-600 text-sm">
              <Calendar size={15} className="text-accent" />{formatDate(sermon.date)}
            </div>
            {sermon.scripture_reference && (
              <div className="flex items-center gap-2 text-gray-600 text-sm">
                <BookOpen size={15} className="text-accent" />{sermon.scripture_reference}
              </div>
            )}
            {sermon.duration && (
              <div className="flex items-center gap-2 text-gray-600 text-sm">
                <Clock size={15} className="text-accent" />{sermon.duration}
              </div>
            )}
          </div>

          {sermon.description && (
            <div className="text-gray-700 leading-relaxed whitespace-pre-line mb-8">
              {sermon.description}
            </div>
          )}

          <Link href="/sermons" className="inline-block px-6 py-3 border border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white transition">
            ← All Sermons
          </Link>
        </div>
      </div>
    </div>
  );
}
