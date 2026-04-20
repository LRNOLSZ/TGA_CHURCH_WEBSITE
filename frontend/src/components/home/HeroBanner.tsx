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
      <div className="relative w-full h-[80vh] bg-dark flex items-center justify-center">
        <div className="text-center text-white px-4">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">Welcome</h1>
          <p className="text-xl text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  const banner = banners[current];

  return (
    <div className="relative w-full h-[80vh] overflow-hidden bg-dark">
      {banners.map((b, i) => (
        <div
          key={b.id}
          className={`absolute inset-0 transition-opacity duration-1000 ${i === current ? "opacity-100" : "opacity-0"}`}
        >
          <Image
            src={getImageUrl(b.image)}
            alt={b.title || "Banner"}
            fill
            className="object-cover"
            priority={i === 0}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-dark/60 via-dark/40 to-dark/70" />
        </div>
      ))}

      {/* Content */}
      <div className="relative z-10 h-full flex items-center justify-center text-center px-4">
        <div className="max-w-3xl">
          {banner.title && (
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg">
              {banner.title}
            </h1>
          )}
          {banner.subtitle && (
            <p className="text-lg md:text-2xl text-gray-200 mb-8 drop-shadow">{banner.subtitle}</p>
          )}
          {banner.button_text && banner.button_link && (
            <Link
              href={banner.button_link}
              className="inline-block px-8 py-3 bg-accent text-white font-semibold rounded-lg text-lg hover:bg-amber-600 transition-colors shadow-lg"
            >
              {banner.button_text}
            </Link>
          )}
        </div>
      </div>

      {/* Dots */}
      {banners.length > 1 && (
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10 flex gap-2">
          {banners.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrent(i)}
              className={`w-3 h-3 rounded-full transition-all ${
                i === current ? "bg-accent w-6" : "bg-white/60 hover:bg-white"
              }`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
