import Image from "next/image";
import Link from "next/link";
import { Play, Calendar, User, BookOpen } from "lucide-react";
import { Sermon } from "@/types";
import { formatDate, getYouTubeThumbnail, getImageUrl } from "@/lib/utils";

export default function SermonCard({ sermon }: { sermon: Sermon }) {
  const thumbnail = sermon.custom_thumbnail
    ? getImageUrl(sermon.custom_thumbnail)
    : getYouTubeThumbnail(sermon.video_url);

  return (
    <div
      className="group overflow-hidden transition-shadow duration-300"
      style={{
        background: "#f6efe0",
        borderRadius: "3px",
        boxShadow: "0 2px 12px rgba(11,30,63,0.06)",
      }}
    >
      {/* Thumbnail */}
      <div className="relative overflow-hidden" style={{ height: "192px", background: "#0a1530" }}>
        <Image src={thumbnail} alt={sermon.title} fill className="object-cover" />
        {/* Play overlay */}
        <div className="absolute inset-0 bg-navy/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <div
            className="flex items-center justify-center"
            style={{
              width: "52px",
              height: "52px",
              borderRadius: "999px",
              background: "rgba(201,162,74,0.9)",
            }}
          >
            <Play size={20} className="text-navy ml-0.5" fill="currentColor" />
          </div>
        </div>
        {/* Series badge */}
        {sermon.series && (
          <div
            className="absolute top-3 left-3"
            style={{
              background: "rgba(11,30,63,0.75)",
              borderRadius: "3px",
              padding: "3px 8px",
            }}
          >
            <span className="font-mono text-gold" style={{ fontSize: "10px", letterSpacing: "0.12em" }}>
              {sermon.series}
            </span>
          </div>
        )}
        {/* Duration chip */}
        {sermon.duration && (
          <div
            className="absolute bottom-3 right-3"
            style={{ background: "rgba(11,30,63,0.7)", borderRadius: "3px", padding: "3px 7px" }}
          >
            <span className="font-mono text-white" style={{ fontSize: "10px" }}>{sermon.duration}</span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-5">
        <h3
          className="font-display text-navy mb-3 line-clamp-2 group-hover:text-gold-2 transition-colors duration-200"
          style={{ fontSize: "18px", fontWeight: 400, lineHeight: 1.25 }}
        >
          {sermon.title}
        </h3>

        <div className="space-y-1.5 mb-4 text-muted" style={{ fontSize: "13px" }}>
          <div className="flex items-center gap-2">
            <User size={13} className="text-gold-2 shrink-0" />
            <span>{sermon.speaker}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar size={13} className="text-gold-2 shrink-0" />
            <span>{formatDate(sermon.date)}</span>
          </div>
          {sermon.scripture_reference && (
            <div className="flex items-center gap-2">
              <BookOpen size={13} className="text-gold-2 shrink-0" />
              <span className="italic">{sermon.scripture_reference}</span>
            </div>
          )}
        </div>

        <Link
          href={`/sermons/${sermon.id}`}
          className="flex items-center justify-center gap-2 w-full px-4 py-2.5 bg-navy text-white font-medium rounded-full text-sm hover:bg-gold hover:text-navy transition-all duration-200"
          style={{ fontSize: "13px" }}
        >
          <Play size={13} fill="currentColor" /> Watch Sermon
        </Link>
      </div>
    </div>
  );
}
