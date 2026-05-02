"use client";

import Image from "next/image";
import { Instagram } from "lucide-react";
import { useHeadPastor } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";

function WhatsAppIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>
  );
}

function TikTokIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.22 8.22 0 004.84 1.56V6.81a4.85 4.85 0 01-1.07-.12z"/>
    </svg>
  );
}

const SOCIAL_KEYS = [
  { key: "whatsapp_url", icon: <WhatsAppIcon />, label: "WhatsApp", href: (v: string) => v },
  { key: "instagram", icon: <Instagram size={16} />, label: "Instagram", href: (v: string) => v.startsWith("http") ? v : `https://instagram.com/${v.replace("@", "")}` },
  { key: "tiktok", icon: <TikTokIcon />, label: "TikTok", href: (v: string) => v.startsWith("http") ? v : `https://tiktok.com/@${v.replace("@", "")}` },
] as const;

export default function HeadPastorSection() {
  const { data: pastor } = useHeadPastor();

  if (!pastor) return null;

  return (
    <section className="bg-bg-2" style={{ paddingTop: "clamp(48px, 8vw, 96px)", paddingBottom: "clamp(48px, 8vw, 96px)" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="tga-two-col" style={{ alignItems: "center" }}>

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
              style={{ aspectRatio: "4/5", borderRadius: "20px" }}
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
                  style={{ fontSize: "clamp(18px, 3vw, 28px)", fontWeight: 400, lineHeight: 1.1 }}
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
              {SOCIAL_KEYS.map(({ key, icon, label, href }) => {
                const val = pastor[key as keyof typeof pastor] as string | null;
                if (!val) return null;
                return (
                  <a
                    key={key}
                    href={href(val)}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={label}
                    className="tga-social-pill"
                  >
                    {icon}
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
