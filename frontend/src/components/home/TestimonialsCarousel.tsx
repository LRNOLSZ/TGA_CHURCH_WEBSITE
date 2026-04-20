"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight, Quote } from "lucide-react";
import { useTestimonies } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";
import SectionHeader from "@/components/ui/SectionHeader";

export default function TestimonialsCarousel() {
  const { data: testimonies, isLoading } = useTestimonies();
  const [current, setCurrent] = useState(0);

  if (isLoading || !testimonies?.length) return null;

  const prev = () => setCurrent((c) => (c === 0 ? testimonies.length - 1 : c - 1));
  const next = () => setCurrent((c) => (c + 1) % testimonies.length);
  const t = testimonies[current];

  return (
    <section className="bg-primary py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionHeader title="Testimonies" subtitle="What God is doing in our community" light />

        <div className="relative bg-white/10 rounded-2xl p-8 md:p-12 text-center">
          <Quote size={48} className="text-accent mx-auto mb-6 opacity-70" />

          <p className="text-white text-lg md:text-xl leading-relaxed mb-8 italic">
            &ldquo;{t.testimony_text}&rdquo;
          </p>

          <div className="flex items-center justify-center gap-4">
            {t.image && (
              <div className="relative w-14 h-14 rounded-full overflow-hidden border-2 border-accent">
                <Image src={getImageUrl(t.image)} alt={t.name} fill className="object-cover" />
              </div>
            )}
            <div className="text-left">
              <p className="text-white font-bold">{t.name}</p>
              {t.location && <p className="text-gray-300 text-sm">{t.location}</p>}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-center gap-4 mt-8">
            <button onClick={prev} className="p-2 rounded-full bg-white/20 hover:bg-white/30 text-white transition">
              <ChevronLeft size={20} />
            </button>
            <div className="flex gap-2">
              {testimonies.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  className={`w-2 h-2 rounded-full transition-all ${i === current ? "bg-accent w-5" : "bg-white/40"}`}
                />
              ))}
            </div>
            <button onClick={next} className="p-2 rounded-full bg-white/20 hover:bg-white/30 text-white transition">
              <ChevronRight size={20} />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
