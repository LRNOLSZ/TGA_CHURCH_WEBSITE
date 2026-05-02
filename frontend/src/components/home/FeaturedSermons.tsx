"use client";

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ChevronLeft, ChevronRight, Play } from "lucide-react";
import useEmblaCarousel from "embla-carousel-react";
import { useFeaturedSermons } from "@/hooks/useSermons";
import { getImageUrl } from "@/lib/utils";
import { Sermon } from "@/types";

const PAGE_SIZE = 3;

function getYoutubeThumbnail(videoUrl: string): string | null {
  const match = videoUrl.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})/);
  return match ? `https://img.youtube.com/vi/${match[1]}/hqdefault.jpg` : null;
}

function SermonCard({ sermon, isCenter }: { sermon: Sermon; isCenter: boolean }) {
  const thumbUrl = sermon.custom_thumbnail
    ? getImageUrl(sermon.custom_thumbnail)
    : sermon.video_url
    ? getYoutubeThumbnail(sermon.video_url)
    : null;

  return (
    <div
      className="w-full"
      style={{
        background: isCenter ? "#152c57" : "#0f2349",
        borderRadius: "3px",
        overflow: "hidden",
      }}
    >
      {/* 4:3 image */}
      <div className="relative w-full" style={{ aspectRatio: "4/3", background: "#0a1530" }}>
        {thumbUrl ? (
          <Image src={thumbUrl} alt={sermon.title} fill className="object-cover" />
        ) : (
          <div className="absolute inset-0" style={{ background: "#0a1530" }} />
        )}
        {/* Dark overlay */}
        <div className="absolute inset-0" style={{ background: "rgba(11,30,63,0.3)" }} />

        {/* Play button — top right */}
        <div
          className="absolute top-3 right-3 flex items-center justify-center"
          style={{
            width: "44px",
            height: "44px",
            borderRadius: "999px",
            background: "rgba(255,255,255,0.15)",
            backdropFilter: "blur(4px)",
          }}
        >
          <Play size={16} className="text-white" fill="white" />
        </div>

        {/* Duration chip — bottom right */}
        {sermon.duration && (
          <div
            className="absolute bottom-3 right-3"
            style={{
              background: "rgba(11,30,63,0.7)",
              borderRadius: "3px",
              padding: "3px 8px",
            }}
          >
            <span className="font-mono text-white" style={{ fontSize: "10px" }}>
              {sermon.duration}
            </span>
          </div>
        )}
      </div>

      {/* Body */}
      <div className="p-5">
        <p className="font-mono text-gold text-[10px] uppercase tracking-[0.18em] mb-2">
          {sermon.series || sermon.scripture_reference || "Message"}
        </p>
        <h3
          className="font-display text-white mb-3 line-clamp-2"
          style={{ fontSize: isCenter ? "22px" : "19px", fontWeight: 400, lineHeight: 1.2 }}
        >
          {sermon.title}
        </h3>
        <div
          className="flex items-center gap-3 pt-3"
          style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }}
        >
          <span className="text-[#8090aa]" style={{ fontSize: "12px" }}>
            {sermon.speaker}
          </span>
          <span className="text-[#8090aa]" style={{ fontSize: "12px" }}>
            {new Date(sermon.date).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function FeaturedSermons() {
  const { data: sermons, isLoading } = useFeaturedSermons();
  const [page, setPage] = useState(0);
  const totalPages = Math.ceil((sermons?.length ?? 0) / PAGE_SIZE);

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

  const items = sermons?.slice(0, 6) ?? [];
  const progress = totalPages > 1 ? (page / (totalPages - 1)) * 100 : 100;

  return (
    <section style={{ background: "#0b1e3f", paddingTop: "clamp(48px, 8vw, 96px)", paddingBottom: "clamp(48px, 8vw, 96px)" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Section header */}
        <div className="tga-carousel-header">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-[0.22em] mb-3" style={{ color: "#b28a30" }}>
              The Word
            </p>
            <h2
              className="font-display text-white"
              style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400, lineHeight: 1.1 }}
            >
              Messages &amp; Sermons
            </h2>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-4 shrink-0">
            <span className="font-mono text-[13px]" style={{ color: "#8090aa" }}>
              {String(page + 1).padStart(2, "0")} / {String(Math.max(1, totalPages)).padStart(2, "0")}
            </span>
            <button onClick={scrollPrev} className="tga-carousel-btn-dark" aria-label="Previous sermons">
              <ChevronLeft size={18} />
            </button>
            <button onClick={scrollNext} className="tga-carousel-btn-dark" aria-label="Next sermons">
              <ChevronRight size={18} />
            </button>
          </div>
        </div>

        {/* Carousel */}
        {isLoading ? (
          <div className="h-64 flex items-center justify-center">
            <span className="font-mono text-sm" style={{ color: "#8090aa" }}>Loading sermons…</span>
          </div>
        ) : items.length === 0 ? (
          <div className="h-64 flex items-center justify-center">
            <span className="font-mono text-sm" style={{ color: "#8090aa" }}>No featured sermons yet.</span>
          </div>
        ) : (
          <div ref={emblaRef} className="overflow-hidden">
            <div className="flex items-center" style={{ gap: "16px" }}>
              {items.map((sermon, i) => {
                const isCenter = i === selectedIndex;
                return (
                  <div
                    key={sermon.id}
                    className={isCenter ? "tga-card-center" : "tga-card-side"}
                    style={{ flexShrink: 0, minWidth: 0 }}
                  >
                    <Link href={`/sermons/${sermon.id}`}>
                      <SermonCard sermon={sermon} isCenter={isCenter} />
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
          style={{ height: "1px", background: "rgba(255,255,255,0.10)" }}
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
            href="/sermons"
            className="inline-flex items-center gap-2 font-mono text-[12px] uppercase tracking-[0.15em] transition-colors duration-200"
            style={{ color: "#8090aa" }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#c9a24a")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "#8090aa")}
          >
            View all sermons <ChevronRight size={14} />
          </Link>
        </div>
      </div>
    </section>
  );
}
