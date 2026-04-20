"use client";

import Image from "next/image";
import { useParams } from "next/navigation";
import { Calendar, MapPin, User, Tag, ExternalLink } from "lucide-react";
import { useEvent } from "@/hooks/useEvents";
import { formatDate, getImageUrl } from "@/lib/utils";
import Badge from "@/components/ui/Badge";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import Link from "next/link";

export default function EventDetailPage() {
  const { id } = useParams();
  const { data: event, isLoading } = useEvent(Number(id));

  if (isLoading) return <LoadingSpinner className="py-40" />;
  if (!event) return <div className="text-center py-40 text-gray-500">Event not found.</div>;

  return (
    <div className="bg-light min-h-screen">
      {/* Banner */}
      <div className="relative h-72 md:h-96 bg-dark">
        {event.image ? (
          <Image src={getImageUrl(event.image)} alt={event.title} fill className="object-cover opacity-60" />
        ) : (
          <div className="absolute inset-0 bg-primary/80" />
        )}
        <div className="absolute inset-0 flex items-end">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8 w-full">
            <Badge variant="accent">{event.category}</Badge>
            <h1 className="text-3xl md:text-5xl font-bold text-white mt-3 drop-shadow">{event.title}</h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl shadow-md p-8">
          {/* Meta */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8 pb-8 border-b border-gray-100">
            <div className="flex items-center gap-3 text-gray-600">
              <Calendar className="text-accent" size={18} />
              <span>{formatDate(event.date)}</span>
            </div>
            <div className="flex items-center gap-3 text-gray-600">
              <MapPin className="text-accent" size={18} />
              <span>{event.location}</span>
            </div>
            {event.branch_name && (
              <div className="flex items-center gap-3 text-gray-600">
                <Tag className="text-accent" size={18} />
                <span>{event.branch_name}</span>
              </div>
            )}
            {event.contact_person && (
              <div className="flex items-center gap-3 text-gray-600">
                <User className="text-accent" size={18} />
                <span>{event.contact_person}</span>
              </div>
            )}
          </div>

          {/* Description */}
          <div className="prose max-w-none text-gray-700 leading-relaxed whitespace-pre-line mb-8">
            {event.description}
          </div>

          {/* CTA */}
          <div className="flex gap-4 flex-wrap">
            {event.registration_link && (
              <a
                href={event.registration_link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-semibold rounded-lg hover:bg-amber-600 transition"
              >
                Register Now <ExternalLink size={16} />
              </a>
            )}
            <Link href="/events" className="px-6 py-3 border border-primary text-primary font-semibold rounded-lg hover:bg-primary hover:text-white transition">
              ← All Events
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
