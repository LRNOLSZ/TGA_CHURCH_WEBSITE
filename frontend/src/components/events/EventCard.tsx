import Image from "next/image";
import Link from "next/link";
import { Calendar, MapPin } from "lucide-react";
import { Event } from "@/types";
import { formatDate, getImageUrl } from "@/lib/utils";

export default function EventCard({ event }: { event: Event }) {
  return (
    <div
      className="group overflow-hidden transition-shadow duration-300"
      style={{
        background: "#f6efe0",
        borderRadius: "3px",
        boxShadow: "0 2px 12px rgba(11,30,63,0.06)",
      }}
    >
      {/* Image */}
      <div className="relative overflow-hidden" style={{ height: "192px", background: "#e9e1cf" }}>
        <Image
          src={getImageUrl(event.image)}
          alt={event.title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-500"
        />
        {/* Category badge */}
        <div
          className="absolute top-3 left-3"
          style={{
            background: "#f6efe0",
            borderRadius: "3px",
            padding: "3px 8px",
          }}
        >
          <span className="font-mono text-gold-2" style={{ fontSize: "10px", letterSpacing: "0.12em", textTransform: "uppercase" }}>
            {event.category}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <h3
          className="font-display text-navy mb-3 line-clamp-2 group-hover:text-gold-2 transition-colors duration-200"
          style={{ fontSize: "18px", fontWeight: 400, lineHeight: 1.25 }}
        >
          {event.title}
        </h3>

        <div className="space-y-1.5 mb-4">
          <div className="flex items-center gap-2 text-muted" style={{ fontSize: "13px" }}>
            <Calendar size={13} className="text-gold-2 shrink-0" />
            <span>{formatDate(event.date)}</span>
          </div>
          <div className="flex items-center gap-2 text-muted" style={{ fontSize: "13px" }}>
            <MapPin size={13} className="text-gold-2 shrink-0" />
            <span className="line-clamp-1">{event.location}</span>
          </div>
        </div>

        <div className="flex gap-2">
          <Link
            href={`/events/${event.id}`}
            className="flex-1 text-center px-4 py-2 font-medium rounded-full text-sm transition-all duration-200 text-navy hover:bg-navy hover:text-white"
            style={{ border: "1.5px solid rgba(11,30,63,0.3)", fontSize: "13px" }}
          >
            Details
          </Link>
          {event.registration_link && (
            <a
              href={event.registration_link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center px-4 py-2 bg-navy text-white font-medium rounded-full text-sm transition-all duration-200 hover:bg-gold hover:text-navy"
              style={{ fontSize: "13px" }}
            >
              Register
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
