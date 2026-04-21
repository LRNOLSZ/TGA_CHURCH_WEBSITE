"use client";

import Image from "next/image";
import { useHeadPastor } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";

const SOCIAL_KEYS = [
  { key: "whatsapp_url", label: "wa", href: (v: string) => v },
  { key: "instagram", label: "ig", href: (v: string) => v.startsWith("http") ? v : `https://instagram.com/${v.replace("@", "")}` },
  { key: "tiktok", label: "tt", href: (v: string) => v.startsWith("http") ? v : `https://tiktok.com/@${v.replace("@", "")}` },
] as const;

export default function HeadPastorSection() {
  const { data: pastor } = useHeadPastor();

  if (!pastor) return null;

  return (
    <section className="bg-bg-2" style={{ paddingTop: "96px", paddingBottom: "96px" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="tga-two-col" style={{ alignItems: "start" }}>

          {/* ── LEFT: Portrait ── */}
          <div className="relative">
            {/* Gold mono number top-right */}
            <span
              className="absolute top-4 right-4 z-10 font-mono text-gold"
              style={{ fontSize: "12px", letterSpacing: "0.1em" }}
            >
              02
            </span>

            {/* Portrait image */}
            <div
              className="relative w-full overflow-hidden"
              style={{ aspectRatio: "4/5", borderRadius: "3px" }}
            >
              <Image
                src={getImageUrl(pastor.image)}
                alt={pastor.name}
                fill
                className="object-cover"
              />
              {/* Name overlay — bottom left */}
              <div
                className="absolute bottom-0 left-0 right-0 z-10 px-6 py-5"
                style={{ background: "linear-gradient(to top, rgba(11,30,63,0.85) 0%, transparent 100%)" }}
              >
                <p
                  className="font-display text-white"
                  style={{ fontSize: "28px", fontWeight: 400, lineHeight: 1.1 }}
                >
                  {pastor.name}
                </p>
                <p className="font-mono text-gold text-[11px] uppercase tracking-[0.18em] mt-1">
                  {pastor.title}
                </p>
              </div>
            </div>
          </div>

          {/* ── RIGHT: Bio ── */}
          <div className="flex flex-col justify-center">
            {/* Eyebrow */}
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-4">
              Our Shepherd
            </p>

            {/* Heading with italic emphasis */}
            <h2
              className="font-display text-navy mb-3"
              style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400, lineHeight: 1.1 }}
            >
              A leader <em className="italic text-gold">rooted</em>
              <br />in purpose.
            </h2>

            {/* Role tag */}
            <p className="font-mono text-muted text-[11px] uppercase tracking-[0.2em] mb-5">
              {pastor.title}
            </p>

            {/* Bio text */}
            <p
              className="text-muted leading-[1.75] mb-7"
              style={{ fontSize: "16px" }}
            >
              {pastor.full_bio
                ? pastor.full_bio.slice(0, 320) + (pastor.full_bio.length > 320 ? "…" : "")
                : ""}
            </p>

            {/* Social links — 42px circular outlined pills */}
            <div className="flex gap-3">
              {SOCIAL_KEYS.map(({ key, label, href }) => {
                const val = pastor[key as keyof typeof pastor] as string | null;
                if (!val) return null;
                return (
                  <a
                    key={key}
                    href={href(val)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="tga-social-pill"
                  >
                    {label}
                  </a>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
