"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useBanners } from "@/hooks/useBanners";
import { getImageUrl } from "@/lib/utils";

export default function HeroBanner() {
  const { data: banners, isLoading } = useBanners();
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    if (!banners?.length) return;
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % banners.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [banners]);

  if (isLoading || !banners?.length) {
    return (
      <section className="tga-hero bg-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-center" style={{ minHeight: 560 }}>
          <div className="text-center">
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-4">Welcome to TGA</p>
            <h1 className="font-display text-navy tga-hero-h1">Loading…</h1>
          </div>
        </div>
      </section>
    );
  }

  const banner = banners[current];
  const commaIdx = banner.title?.indexOf(",") ?? -1;
  const titleFirst = commaIdx > -1 ? banner.title!.slice(0, commaIdx).trim() : (banner.title ?? "Welcome");
  const titleSecond = commaIdx > -1 ? banner.title!.slice(commaIdx + 1).trim() : null;

  return (
    <section className="tga-hero bg-bg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="tga-hero-grid">

          {/* ── LEFT COLUMN ── */}
          <div className="flex flex-col justify-center">
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-6">
              Welcome to TGA
            </p>

            <h1 className="font-display text-navy tga-hero-h1 mb-6">
              {titleFirst}
              {titleSecond && (
                <><span className="text-navy">,</span>{" "}
                  <em className="tga-hero-em">{titleSecond}</em>
                </>
              )}
            </h1>

            {banner.subtitle && (
              <p className="text-muted leading-[1.75] mb-8 tga-hero-lede">
                {banner.subtitle}
              </p>
            )}

            <div className="flex flex-wrap gap-3">
              <Link href="/about" className="tga-btn-primary">
                Plan a Visit
              </Link>
              <Link href="/sermons" className="tga-btn-ghost">
                Watch Latest Sermon
              </Link>
            </div>
          </div>

          {/* ── RIGHT COLUMN ── */}
          <div className="tga-hero-visual">
            <div className="tga-hero-img-wrap">
              {banners.map((b, i) => (
                <div
                  key={b.id}
                  className="absolute inset-0 transition-opacity duration-1000"
                  style={{ opacity: i === current ? 1 : 0 }}
                >
                  <Image
                    src={getImageUrl(b.image)}
                    alt={b.title || "Banner"}
                    fill
                    className="object-cover"
                    priority={i === 0}
                  />
                </div>
              ))}
              {/* Overlay */}
              <div className="absolute inset-0" style={{ background: "linear-gradient(to bottom, rgba(11,30,63,0.15) 0%, rgba(11,30,63,0.5) 100%)" }} />

            </div>

            {/* Vertical pagination dots */}
            {banners.length > 1 && (
              <div className="tga-hero-dots">
                {banners.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrent(i)}
                    aria-label={`Slide ${i + 1}`}
                    className="rounded-full transition-all duration-300 block"
                    style={{
                      width: "6px",
                      height: i === current ? "36px" : "22px",
                      background: i === current ? "#c9a24a" : "rgba(11,30,63,0.25)",
                    }}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
