"use client";

import Link from "next/link";
import { useChurchInfo } from "@/hooks/useChurchData";

const discoverLinks = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/gallery", label: "Gallery" },
  { href: "/leadership", label: "Leadership" },
];

const growLinks = [
  { href: "/sermons", label: "Sermons" },
  { href: "/events", label: "Events" },
  { href: "/branches", label: "Branches" },
  { href: "/store", label: "Store" },
];

const contactLinks = [
  { href: "/contact", label: "Contact" },
  { href: "/giving", label: "Give" },
];

const socials = [
  { key: "youtube_channel_url", label: "yt" },
  { key: "facebook_url", label: "fb" },
  { key: "instagram_url", label: "ig" },
  { key: "twitter_url", label: "tw" },
  { key: "whatsapp_url", label: "wa" },
  { key: "tiktok_url", label: "tt" },
] as const;

export default function Footer() {
  const { data: info } = useChurchInfo();

  return (
    <footer className="bg-navy-ink text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-14 pb-6">
        {/* 4-column grid */}
        <div
          className="grid gap-10 pb-10"
          style={{
            gridTemplateColumns: "1.4fr 1fr 1fr 1fr",
            borderBottom: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          {/* Col 1 — brand */}
          <div className="col-span-4 lg:col-span-1">
            <div className="flex items-center gap-2.5 mb-3">
              <div className="w-9 h-9 rounded-full bg-navy-2 flex items-center justify-center shrink-0">
                <span className="font-display text-gold font-semibold text-base leading-none">T</span>
              </div>
              <span className="font-display text-white font-normal text-lg tracking-tight">
                TGA<span className="text-gold">·</span>Church
              </span>
            </div>
            <p className="text-[#a09880] text-sm leading-relaxed mb-5">
              {info?.tagline || "Building Faith, Changing Lives"}
            </p>
            {/* Social icons */}
            <div className="flex flex-wrap gap-2">
              {socials.map(({ key, label }) => {
                const url = info?.[key];
                if (!url) return null;
                return (
                  <a
                    key={key}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-[38px] h-[38px] rounded-full flex items-center justify-center font-mono text-[10px] text-[#a09880] transition-colors duration-200 hover:text-gold hover:border-gold"
                    style={{ border: "1px solid rgba(255,255,255,0.18)" }}
                  >
                    {label}
                  </a>
                );
              })}
            </div>
          </div>

          {/* Col 2 — Discover */}
          <div className="col-span-2 sm:col-span-1">
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-4">
              Discover
            </p>
            <ul className="space-y-2.5">
              {discoverLinks.map(({ href, label }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-[#a09880] text-sm transition-colors duration-200 hover:text-gold"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 3 — Grow */}
          <div className="col-span-2 sm:col-span-1">
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-4">
              Grow
            </p>
            <ul className="space-y-2.5">
              {growLinks.map(({ href, label }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-[#a09880] text-sm transition-colors duration-200 hover:text-gold"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 4 — Contact */}
          <div className="col-span-4 sm:col-span-1">
            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-4">
              Contact
            </p>
            <ul className="space-y-2.5">
              {contactLinks.map(({ href, label }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-[#a09880] text-sm transition-colors duration-200 hover:text-gold"
                  >
                    {label}
                  </Link>
                </li>
              ))}
              {info?.address && (
                <li className="text-[#a09880] text-sm leading-relaxed pt-1">{info.address}</li>
              )}
              {info?.phone && (
                <li>
                  <a
                    href={`tel:${info.phone}`}
                    className="text-[#a09880] text-sm transition-colors duration-200 hover:text-gold"
                  >
                    {info.phone}
                  </a>
                </li>
              )}
              {info?.email && (
                <li>
                  <a
                    href={`mailto:${info.email}`}
                    className="text-[#a09880] text-sm transition-colors duration-200 hover:text-gold"
                  >
                    {info.email}
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-2 pt-5">
          <p className="font-mono text-[11px] text-[#5a5244] uppercase tracking-[0.12em]">
            © {new Date().getFullYear()} TGA Church. All rights reserved.
          </p>
          <p className="font-mono text-[11px] text-[#5a5244] uppercase tracking-[0.12em]">
            Built on Grace
          </p>
        </div>
      </div>
    </footer>
  );
}
