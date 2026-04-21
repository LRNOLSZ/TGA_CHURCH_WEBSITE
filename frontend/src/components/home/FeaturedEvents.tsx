"use client";

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ChevronLeft, ChevronRight, MapPin, Clock } from "lucide-react";
import useEmblaCarousel from "embla-carousel-react";
import { useFeaturedEvents } from "@/hooks/useEvents";
import { getImageUrl } from "@/lib/utils";
import { Event } from "@/types";

const PAGE_SIZE = 3;

function EventCard({ event, isCenter }: { event: Event; isCenter: boolean }) {
  const dateObj = new Date(event.date);
  const day = dateObj.toLocaleDateString("en-US", { day: "2-digit" });
  const month = dateObj.toLocaleDateString("en-US", { month: "short" }).toUpperCase();
  const time = dateObj.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });

  return (
    <div
      className="w-full"
      style={{
        background: isCenter ? "#fff8e8" : "#f6efe0",
        borderRadius: "3px",
        overflow: "hidden",
      }}
    >
      {/* 4:3 image */}
      <div className="relative w-full" style={{ aspectRatio: "4/3", background: "#e9e1cf" }}>
        {event.image ? (
          <Image
            src={getImageUrl(event.image)}
            alt={event.title}
            fill
            className="object-cover"
          />
        ) : (
          <div className="absolute inset-0 bg-bg-2" />
        )}
        {/* Date badge */}
        <div
          className="absolute top-3 left-3"
          style={{
            background: "#f6efe0",
            borderRadius: "3px",
            padding: "6px 10px",
            textAlign: "center",
            minWidth: "48px",
          }}
        >
          <p
            className="font-display text-navy block"
            style={{ fontSize: "20px", fontWeight: 400, lineHeight: 1 }}
          >
            {day}
          </p>
          <p className="font-mono text-gold-2 block" style={{ fontSize: "9px", letterSpacing: "0.12em" }}>
            {month}
          </p>
        </div>
      </div>

      {/* Body */}
      <div className="p-5">
        <p className="font-mono text-gold-2 text-[10px] uppercase tracking-[0.18em] mb-2">
          {event.category}
        </p>
        <h3
          className="font-display text-navy mb-3 line-clamp-2"
          style={{ fontSize: isCenter ? "22px" : "19px", fontWeight: 400, lineHeight: 1.2 }}
        >
          {event.title}
        </h3>
        <div
          className="flex items-center gap-4 pt-3"
          style={{ borderTop: "1px solid rgba(11,30,63,0.10)" }}
        >
          <span className="flex items-center gap-1 text-muted" style={{ fontSize: "12px" }}>
            <MapPin size={12} />
            <span className="line-clamp-1">{event.location}</span>
          </span>
          <span className="flex items-center gap-1 text-muted shrink-0" style={{ fontSize: "12px" }}>
            <Clock size={12} />
            {time}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function FeaturedEvents() {
  const { data: events, isLoading } = useFeaturedEvents();
  const [page, setPage] = useState(0);
  const totalPages = Math.ceil((events?.length ?? 0) / PAGE_SIZE);

  const [emblaRef, emblaApi] = useEmblaCarousel({
    loop: true,
    align: "center",
    containScroll: false,
  });

  const scrollPrev = useCallback(() => {
    if (!emblaApi) return;
    emblaApi.scrollPrev();
    setPage((p) => (p === 0 ? Math.max(0, totalPages - 1) : p - 1));
  }, [emblaApi, totalPages]);

  const scrollNext = useCallback(() => {
    if (!emblaApi) return;
    emblaApi.scrollNext();
    setPage((p) => (p + 1) % Math.max(1, totalPages));
  }, [emblaApi, totalPages]);

  const [selectedIndex, setSelectedIndex] = useState(0);
  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setSelectedIndex(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    emblaApi.on("select", onSelect);
    return () => { emblaApi.off("select", onSelect); };
  }, [emblaApi, onSelect]);

  const items = events?.slice(0, 6) ?? [];
  const progress = totalPages > 1 ? (page / (totalPages - 1)) * 100 : 100;

  return (
    <section className="bg-bg" style={{ paddingTop: "96px", paddingBottom: "96px" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Section header */}
        <div className="tga-carousel-header">
          <div>
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-3">
              Coming Up
            </p>
            <h2
              className="font-display text-navy"
              style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400, lineHeight: 1.1 }}
            >
              Featured Events
            </h2>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-4 shrink-0">
            <span className="font-mono text-muted" style={{ fontSize: "13px" }}>
              {String(page + 1).padStart(2, "0")} / {String(Math.max(1, totalPages)).padStart(2, "0")}
            </span>
            <button
              onClick={scrollPrev}
              className="tga-carousel-btn"
              aria-label="Previous events"
            >
              <ChevronLeft size={18} />
            </button>
            <button
              onClick={scrollNext}
              className="tga-carousel-btn"
              aria-label="Next events"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>

        {/* Carousel */}
        {isLoading ? (
          <div className="h-64 flex items-center justify-center">
            <span className="font-mono text-muted text-sm">Loading events…</span>
          </div>
        ) : items.length === 0 ? (
          <div className="h-64 flex items-center justify-center">
            <span className="font-mono text-muted text-sm">No featured events yet.</span>
          </div>
        ) : (
          <div ref={emblaRef} className="overflow-hidden">
            <div className="flex items-center" style={{ gap: "16px" }}>
              {items.map((event, i) => {
                const isCenter = i === selectedIndex;
                return (
                  <div
                    key={event.id}
                    className={isCenter ? "tga-card-center" : "tga-card-side"}
                    style={{ flexShrink: 0, minWidth: 0 }}
                  >
                    <Link href={`/events/${event.id}`}>
                      <EventCard event={event} isCenter={isCenter} />
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Progress bar */}
        <div
          className="mt-8 relative"
          style={{ height: "1px", background: "rgba(11,30,63,0.12)" }}
        >
          <div
            className="absolute left-0 top-[-1px] transition-all duration-500"
            style={{
              width: `${progress}%`,
              height: "3px",
              background: "#c9a24a",
              borderRadius: "2px",
            }}
          />
        </div>

        {/* View all */}
        <div className="mt-8 text-center">
          <Link
            href="/events"
            className="inline-flex items-center gap-2 font-mono text-navy text-[12px] uppercase tracking-[0.15em] hover:text-gold-2 transition-colors duration-200"
          >
            View all events <ChevronRight size={14} />
          </Link>
        </div>
      </div>
    </section>
  );
}
