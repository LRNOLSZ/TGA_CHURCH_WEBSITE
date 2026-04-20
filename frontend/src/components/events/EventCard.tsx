import Image from "next/image";
import Link from "next/link";
import { Calendar, MapPin } from "lucide-react";
import { Event } from "@/types";
import { formatDate, getImageUrl } from "@/lib/utils";
import Badge from "@/components/ui/Badge";

export default function EventCard({ event }: { event: Event }) {
  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-shadow group">
      {/* Image */}
      <div className="relative h-48 bg-gray-100">
        <Image
          src={getImageUrl(event.image)}
          alt={event.title}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-3 left-3">
          <Badge variant="accent">{event.category}</Badge>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <h3 className="font-bold text-text-main text-lg mb-3 line-clamp-2 group-hover:text-primary transition-colors">
          {event.title}
        </h3>

        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-gray-500 text-sm">
            <Calendar size={14} className="text-accent" />
            <span>{formatDate(event.date)}</span>
          </div>
          <div className="flex items-center gap-2 text-gray-500 text-sm">
            <MapPin size={14} className="text-accent" />
            <span className="line-clamp-1">{event.location}</span>
          </div>
        </div>

        <div className="flex gap-2">
          <Link
            href={`/events/${event.id}`}
            className="flex-1 text-center px-4 py-2 border border-primary text-primary font-medium rounded-lg text-sm hover:bg-primary hover:text-white transition-colors"
          >
            Details
          </Link>
          {event.registration_link && (
            <a
              href={event.registration_link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center px-4 py-2 bg-accent text-white font-medium rounded-lg text-sm hover:bg-amber-600 transition-colors"
            >
              Register
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
