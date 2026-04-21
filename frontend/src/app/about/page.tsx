"use client";

import { Clock, Target, Eye, Star } from "lucide-react";
import { useChurchInfo } from "@/hooks/useChurchData";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function AboutPage() {
  const { data: info, isLoading } = useChurchInfo();

  if (isLoading) return <LoadingSpinner className="py-40" />;

  return (
    <div className="bg-bg min-h-screen">
      {/* Header */}
      <div className="bg-navy py-16 text-center">
        <SectionHeader title="About Us" subtitle={info?.tagline} light />
      </div>

      {/* Church Story */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="p-10">
          <div className="w-12 h-1 bg-accent mb-4" />
          <h2 className="text-2xl font-bold text-primary mb-6">Our Story</h2>
          <div className="text-gray-700 leading-relaxed whitespace-pre-line">
            {info?.full_about}
          </div>
        </div>
      </section>

      {/* Mission, Vision, Values */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-8 text-center" style={{ background: "#f6efe0", borderRadius: "3px" }}>
            <div className="p-3 bg-navy/10 rounded-full w-fit mx-auto mb-4">
              <Target className="text-navy" size={28} />
            </div>
            <h3 className="font-display text-navy text-xl mb-3" style={{ fontWeight: 400 }}>Our Mission</h3>
            <p className="text-muted leading-relaxed">{info?.mission_statement}</p>
          </div>

          <div className="p-8 text-center" style={{ background: "#0b1e3f", borderRadius: "3px" }}>
            <div className="p-3 rounded-full w-fit mx-auto mb-4" style={{ background: "rgba(255,255,255,0.1)" }}>
              <Eye className="text-white" size={28} />
            </div>
            <h3 className="font-display text-white text-xl mb-3" style={{ fontWeight: 400 }}>Our Vision</h3>
            <p className="leading-relaxed" style={{ color: "rgba(255,255,255,0.75)" }}>{info?.vision_statement}</p>
          </div>

          <div className="p-8 text-center" style={{ background: "#f6efe0", borderRadius: "3px" }}>
            <div className="p-3 rounded-full w-fit mx-auto mb-4" style={{ background: "rgba(201,162,74,0.12)" }}>
              <Star className="text-gold" size={28} />
            </div>
            <h3 className="font-display text-navy text-xl mb-3" style={{ fontWeight: 400 }}>Core Values</h3>
            <p className="text-muted leading-relaxed whitespace-pre-line">{info?.core_values}</p>
          </div>
        </div>
      </section>

      {/* Service Times */}
      {info?.service_times_text && (
        <section className="bg-white py-16">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <SectionHeader title="Service Times" />
            <div className="bg-primary/5 rounded-2xl p-8 flex gap-4">
              <Clock className="text-primary shrink-0 mt-1" size={24} />
              <div className="whitespace-pre-line text-gray-700 leading-relaxed">
                {info.service_times_text}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
