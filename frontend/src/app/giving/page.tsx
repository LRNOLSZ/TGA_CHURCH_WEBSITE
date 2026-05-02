"use client";

import Image from "next/image";
import { Heart, ExternalLink } from "lucide-react";
import { useGivingInfo } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function GivingPage() {
  const { data: giving, isLoading } = useGivingInfo();

  if (isLoading) return <LoadingSpinner className="py-40" />;

  return (
    <div className="bg-bg min-h-screen">
      {/* Header */}
      <div className="bg-navy py-16 text-center">
        <SectionHeader
          title={giving?.title || "Give / Support the Ministry"}
          subtitle="Your generosity makes a difference"
          light
        />
      </div>

      {/* Why Give */}
      {giving?.why_give_message && (
        <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="bg-white rounded-2xl shadow-md p-10 text-center">
            <div className="p-4 bg-accent/10 rounded-full w-fit mx-auto mb-6">
              <Heart className="text-accent" size={36} />
            </div>
            <div className="text-gray-700 leading-relaxed whitespace-pre-line text-lg">
              {giving.why_give_message}
            </div>
          </div>
        </section>
      )}

      {/* Instructions */}
      {giving?.instructions && (
        <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
          <div className="bg-primary/5 border border-primary/20 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-primary mb-4">How to Give</h2>
            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              {giving.instructions}
            </div>
          </div>
        </section>
      )}

      {/* Images Grid */}
      {giving?.images && giving.images.length > 0 && (
        <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {giving.images.map((img) => (
              <div key={img.id} className="relative aspect-video rounded-xl overflow-hidden shadow-sm">
                <Image src={getImageUrl(img.image)} alt={img.caption || "Giving"} fill className="object-cover" />
                {img.caption && (
                  <div className="absolute bottom-0 inset-x-0 bg-dark/60 text-white text-xs p-2">{img.caption}</div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* CTA Button */}
      {giving?.flutterwave_link && (
        <section className="py-12 text-center">
          <a
            href={giving.flutterwave_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 px-8 py-4 bg-navy text-white font-bold text-base sm:text-xl rounded-full hover:bg-gold hover:text-navy transition-all duration-200"
          >
            <Heart size={24} /> Give Now via Flutterwave <ExternalLink size={18} />
          </a>
        </section>
      )}
    </div>
  );
}
