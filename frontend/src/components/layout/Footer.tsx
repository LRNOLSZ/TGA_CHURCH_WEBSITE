"use client";

import Link from "next/link";
import { Youtube, Instagram, Twitter } from "lucide-react";
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

function FacebookIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.886v2.268h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/>
    </svg>
  );
}

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

const socials = [
  { key: "youtube_channel_url", icon: <Youtube size={16} />, label: "YouTube" },
  { key: "facebook_url", icon: <FacebookIcon />, label: "Facebook" },
  { key: "instagram_url", icon: <Instagram size={16} />, label: "Instagram" },
  { key: "twitter_url", icon: <Twitter size={16} />, label: "Twitter" },
  { key: "whatsapp_url", icon: <WhatsAppIcon />, label: "WhatsApp" },
  { key: "tiktok_url", icon: <TikTokIcon />, label: "TikTok" },
] as const;

export default function Footer() {
  const { data: info } = useChurchInfo();

  return (
    <footer className="bg-navy-ink text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-14 pb-6">
        {/* 4-column grid */}
        <div
          className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-10 pb-10"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.08)" }}
        >
          {/* Col 1 — brand */}
          <div className="col-span-2 lg:col-span-1 text-center">
            <div className="flex items-center justify-center gap-2.5 mb-3">
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
            <div className="flex flex-wrap gap-2 justify-center">
              {socials.map(({ key, icon, label }) => {
                const url = info?.[key];
                if (!url) return null;
                return (
                  <a
                    key={key}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={label}
                    className="w-[38px] h-[38px] rounded-full flex items-center justify-center text-[#a09880] transition-colors duration-200 hover:text-gold hover:border-gold"
                    style={{ border: "1px solid rgba(255,255,255,0.18)" }}
                  >
                    {icon}
                  </a>
                );
              })}
            </div>
          </div>

          {/* Col 2 — Discover */}
          <div className="text-center">
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
          <div className="text-center">
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
          <div className="col-span-2 lg:col-span-1 text-center">
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
            Built by{" "}
            <a
              href="mailto:laryea024@gmail.com"
              className="text-gold-2 hover:text-gold transition-colors duration-200"
            >
              LEMUEL
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
