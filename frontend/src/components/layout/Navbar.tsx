"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/events", label: "Events" },
  { href: "/sermons", label: "Sermons" },
  { href: "/leadership", label: "Leadership" },
  { href: "/gallery", label: "Gallery" },
  { href: "/branches", label: "Branches" },
  { href: "/store", label: "Store" },
  { href: "/contact", label: "Contact" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        background: "rgba(241,235,222,0.78)",
        backdropFilter: "blur(10px)",
        WebkitBackdropFilter: "blur(10px)",
        borderBottom: "1px solid rgba(11,30,63,0.12)",
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-[72px]">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5">
            <div
              className="w-10 h-10 rounded-full bg-navy flex items-center justify-center shrink-0"
            >
              <span className="font-display text-gold font-semibold text-lg leading-none">T</span>
            </div>
            <span className="font-display text-navy font-normal text-[21px] tracking-tight">
              TGA<span className="text-gold">·</span>Church
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden lg:flex items-center gap-0.5">
            {navLinks.map(({ href, label }) => {
              const isActive = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  className="relative px-3 py-2 text-[13.5px] font-medium text-navy transition-colors duration-200 hover:text-gold-2"
                  style={isActive ? { color: "#0b1e3f" } : {}}
                >
                  {label}
                  {isActive && (
                    <span
                      className="absolute bottom-[2px] left-3 right-3 h-px bg-gold-2"
                    />
                  )}
                </Link>
              );
            })}
            <Link
              href="/giving"
              className="ml-4 px-5 py-2 bg-navy text-white font-medium rounded-full text-[13.5px] transition-all duration-200 hover:bg-gold hover:text-navy"
            >
              Give
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button
            className="lg:hidden p-2 rounded-md text-navy hover:text-gold-2 transition-colors"
            onClick={() => setOpen(!open)}
            aria-label="Toggle menu"
          >
            {open ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div
          className="lg:hidden"
          style={{
            background: "rgba(241,235,222,0.97)",
            borderTop: "1px solid rgba(11,30,63,0.10)",
          }}
        >
          <div className="px-4 py-3 space-y-0.5">
            {navLinks.map(({ href, label }) => {
              const isActive = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setOpen(false)}
                  className={`block px-3 py-2.5 text-sm font-medium rounded-sm transition-colors duration-200 ${
                    isActive
                      ? "text-navy border-l-2 border-gold pl-4"
                      : "text-muted hover:text-navy"
                  }`}
                >
                  {label}
                </Link>
              );
            })}
            <Link
              href="/giving"
              onClick={() => setOpen(false)}
              className="block mt-3 px-5 py-2.5 bg-navy text-white font-medium rounded-full text-sm text-center hover:bg-gold hover:text-navy transition-all duration-200"
            >
              Give Now
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
