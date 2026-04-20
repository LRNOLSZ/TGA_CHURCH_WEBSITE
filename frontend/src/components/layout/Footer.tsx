"use client";

import Link from "next/link";
import { MapPin, Phone, Mail } from "lucide-react";
import SocialLinks from "@/components/ui/SocialLinks";
import { useChurchInfo } from "@/hooks/useChurchData";

const quickLinks = [
  { href: "/about", label: "About Us" },
  { href: "/events", label: "Events" },
  { href: "/sermons", label: "Sermons" },
  { href: "/leadership", label: "Leadership" },
  { href: "/gallery", label: "Gallery" },
  { href: "/branches", label: "Branches" },
  { href: "/store", label: "Store" },
  { href: "/giving", label: "Give" },
  { href: "/contact", label: "Contact" },
];

export default function Footer() {
  const { data: info } = useChurchInfo();

  return (
    <footer className="bg-dark text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">{info?.church_name || "TGA Church"}</h3>
            <p className="text-gray-400 text-sm mb-4">{info?.tagline}</p>
            <SocialLinks
              youtube={info?.youtube_channel_url}
              facebook={info?.facebook_url}
              instagram={info?.instagram_url}
              twitter={info?.twitter_url}
              whatsapp={info?.whatsapp_url}
              tiktok={info?.tiktok_url}
            />
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4 text-lg">Quick Links</h4>
            <ul className="space-y-2">
              {quickLinks.map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className="text-gray-400 hover:text-accent transition-colors text-sm">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-semibold mb-4 text-lg">Contact Us</h4>
            <ul className="space-y-3 text-sm">
              {info?.address && (
                <li className="flex gap-2 text-gray-400">
                  <MapPin size={16} className="mt-0.5 shrink-0 text-accent" />
                  <span>{info.address}</span>
                </li>
              )}
              {info?.phone && (
                <li className="flex gap-2 text-gray-400">
                  <Phone size={16} className="mt-0.5 shrink-0 text-accent" />
                  <a href={`tel:${info.phone}`} className="hover:text-accent transition-colors">{info.phone}</a>
                </li>
              )}
              {info?.email && (
                <li className="flex gap-2 text-gray-400">
                  <Mail size={16} className="mt-0.5 shrink-0 text-accent" />
                  <a href={`mailto:${info.email}`} className="hover:text-accent transition-colors">{info.email}</a>
                </li>
              )}
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-10 pt-6 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} {info?.church_name || "TGA Church"}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
