"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useTestimonies } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";

export default function TestimonialsCarousel() {
  const { data: testimonies } = useTestimonies();
  const [current, setCurrent] = useState(0);

  if (!testimonies?.length) return null;

  const prev = () => setCurrent((c) => (c === 0 ? testimonies.length - 1 : c - 1));
  const next = () => setCurrent((c) => (c + 1) % testimonies.length);
  const t = testimonies[current];

  return (
    <section className="bg-bg" style={{ paddingTop: "clamp(48px, 8vw, 96px)", paddingBottom: "clamp(48px, 8vw, 96px)" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Eyebrow */}
        <div className="text-center mb-12">
          <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-3">
            Testimonies
          </p>
          <h2
            className="font-display text-navy"
            style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400 }}
          >
            What God is doing
          </h2>
        </div>

        {/* Quote block */}
        <div className="mx-auto text-center" style={{ maxWidth: "840px" }}>
          {/* Oversized opening quote */}
          <div
            className="font-display text-gold select-none"
            style={{
              fontSize: "clamp(60px, 15vw, 120px)",
              lineHeight: 0.6,
              marginBottom: "24px",
              fontWeight: 300,
            }}
            aria-hidden="true"
          >
            &ldquo;
          </div>

          {/* Quote text */}
          <p
            className="font-display italic text-navy"
            style={{
              fontSize: "clamp(26px, 3.4vw, 42px)",
              fontWeight: 300,
              lineHeight: 1.4,
              marginBottom: "40px",
            }}
          >
            {t.testimony_text}
          </p>

          {/* Avatar + name */}
          <div className="flex flex-col items-center gap-3">
            {t.image ? (
              <div
                className="relative rounded-full overflow-hidden"
                style={{
                  width: "52px",
                  height: "52px",
                  border: "2px solid #c9a24a",
                }}
              >
                <Image
                  src={getImageUrl(t.image)}
                  alt={t.name}
                  fill
                  className="object-cover"
                />
              </div>
            ) : (
              <div
                className="rounded-full bg-navy-2 flex items-center justify-center"
                style={{ width: "52px", height: "52px", border: "2px solid #c9a24a" }}
              >
                <span className="font-display text-gold text-lg">
                  {t.name.charAt(0)}
                </span>
              </div>
            )}
            <div>
              <p className="font-display text-navy" style={{ fontSize: "18px", fontWeight: 400 }}>
                {t.name}
              </p>
              {t.location && (
                <p className="font-mono text-muted text-center" style={{ fontSize: "12px" }}>
                  {t.location}
                </p>
              )}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-center gap-5 mt-10">
            <button onClick={prev} className="tga-carousel-btn" aria-label="Previous testimony">
              <ChevronLeft size={18} />
            </button>

            {/* Dots */}
            <div className="flex items-center gap-2">
              {testimonies.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  aria-label={`Testimony ${i + 1}`}
                  className="rounded-full transition-all duration-300"
                  style={{
                    height: "6px",
                    width: i === current ? "24px" : "6px",
                    background: i === current ? "#c9a24a" : "rgba(11,30,63,0.2)",
                  }}
                />
              ))}
            </div>

            <button onClick={next} className="tga-carousel-btn" aria-label="Next testimony">
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
