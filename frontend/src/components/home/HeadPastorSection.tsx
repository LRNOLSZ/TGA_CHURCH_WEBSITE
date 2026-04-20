"use client";

import Image from "next/image";
import { useHeadPastor } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";
import SocialLinks from "@/components/ui/SocialLinks";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function HeadPastorSection() {
  const { data: pastor, isLoading } = useHeadPastor();

  if (isLoading) return <LoadingSpinner />;
  if (!pastor) return null;

  return (
    <section className="bg-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Photo */}
          <div className="relative h-96 rounded-2xl overflow-hidden shadow-xl">
            <Image
              src={getImageUrl(pastor.image)}
              alt={pastor.name}
              fill
              className="object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-dark/60 to-transparent" />
            <div className="absolute bottom-6 left-6 text-white">
              <p className="text-lg font-bold">{pastor.name}</p>
              <p className="text-accent text-sm">{pastor.title}</p>
            </div>
          </div>

          {/* Bio */}
          <div>
            <div className="w-12 h-1 bg-accent mb-4" />
            <h2 className="text-3xl font-bold text-primary mb-2">{pastor.name}</h2>
            <p className="text-accent font-semibold mb-4">{pastor.title}</p>
            <p className="text-gray-600 leading-relaxed mb-6 line-clamp-6">{pastor.full_bio}</p>
            <SocialLinks
              whatsapp={pastor.whatsapp_url}
              instagram={pastor.instagram}
              tiktok={pastor.tiktok}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
