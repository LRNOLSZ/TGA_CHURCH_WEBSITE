"use client";

import { Clock, Target, Eye, Star } from "lucide-react";
import { useChurchInfo } from "@/hooks/useChurchData";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function AboutPage() {
  const { data: info, isLoading } = useChurchInfo();

  if (isLoading) return <LoadingSpinner className="py-40" />;

  return (
    <div className="bg-light min-h-screen">
      {/* Header */}
      <div className="bg-primary py-16 text-center">
        <SectionHeader title="About Us" subtitle={info?.tagline} light />
      </div>

      {/* Church Story */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-white rounded-2xl shadow-md p-10">
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
          <div className="bg-white rounded-2xl shadow-md p-8 text-center">
            <div className="p-3 bg-primary/10 rounded-full w-fit mx-auto mb-4">
              <Target className="text-primary" size={28} />
            </div>
            <h3 className="text-xl font-bold text-primary mb-3">Our Mission</h3>
            <p className="text-gray-600 leading-relaxed">{info?.mission_statement}</p>
          </div>

          <div className="bg-primary rounded-2xl shadow-md p-8 text-center">
            <div className="p-3 bg-white/20 rounded-full w-fit mx-auto mb-4">
              <Eye className="text-white" size={28} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Our Vision</h3>
            <p className="text-gray-200 leading-relaxed">{info?.vision_statement}</p>
          </div>

          <div className="bg-white rounded-2xl shadow-md p-8 text-center">
            <div className="p-3 bg-accent/10 rounded-full w-fit mx-auto mb-4">
              <Star className="text-accent" size={28} />
            </div>
            <h3 className="text-xl font-bold text-primary mb-3">Core Values</h3>
            <p className="text-gray-600 leading-relaxed whitespace-pre-line">{info?.core_values}</p>
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
