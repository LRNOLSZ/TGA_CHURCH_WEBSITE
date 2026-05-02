import Link from "next/link";
import { ArrowRight } from "lucide-react";

const cards = [
  {
    num: "01",
    title: "Plan a Visit",
    body: "Experience our warm, welcoming community in person. We'd love to meet you.",
    href: "/branches",
    cta: "Find us",
  },
  {
    num: "02",
    title: "Give & Support",
    body: "Partner with us to spread the Gospel and transform communities across Ghana.",
    href: "/giving",
    cta: "Give now",
    featured: true,
  },
  {
    num: "03",
    title: "Get in Touch",
    body: "Have questions, prayer requests, or feedback? We're here for you.",
    href: "/contact",
    cta: "Contact us",
  },
];

export default function CTASection() {
  return (
    <section className="bg-bg-2" style={{ paddingTop: "96px", paddingBottom: "96px" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Heading */}
        <div className="text-center mb-12">
          <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-3">
            Next Steps
          </p>
          <h2
            className="font-display text-navy mb-4"
            style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400 }}
          >
            Get Involved
          </h2>
          <p className="text-muted" style={{ fontSize: "16px", maxWidth: "480px", margin: "0 auto" }}>
            There are many ways to connect with our community and grow in faith.
          </p>
        </div>

        {/* 3-card grid */}
        <div className="tga-cta-grid grid grid-cols-1 md:grid-cols-3 gap-6">
          {cards.map(({ num, title, body, href, cta, featured }) => (
            <Link
              key={href}
              href={href}
              className="tga-cta-card items-center text-center"
              data-featured={featured ? "true" : undefined}
            >
              <span className="font-mono tga-cta-num" style={{ fontSize: "11px", letterSpacing: "0.15em" }}>
                {num}
              </span>
              <h3 className="font-display tga-cta-title" style={{ fontSize: "clamp(24px, 4vw, 36px)", fontWeight: 400, lineHeight: 1.1, marginTop: "20px", marginBottom: "12px" }}>
                {title}
              </h3>
              <p className="tga-cta-body" style={{ fontSize: "15px", lineHeight: 1.7, flexGrow: 1 }}>
                {body}
              </p>
              <div className="flex items-center justify-center gap-2 mt-6 tga-cta-link" style={{ fontSize: "13px", fontWeight: 500 }}>
                {cta} <ArrowRight size={14} className="tga-cta-arrow" />
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
