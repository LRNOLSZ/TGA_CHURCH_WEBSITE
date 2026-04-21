"use client";

import { useState } from "react";
import Image from "next/image";
import { useGallery } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

const CATEGORIES = ["All", "Church Building", "Worship", "Events", "Outreach", "Other"];

export default function GalleryPage() {
  const [category, setCategory] = useState("All");
  const { data: photos, isLoading } = useGallery(category);

  return (
    <div className="bg-bg min-h-screen">
      <div className="bg-navy py-16 text-center">
        <SectionHeader title="Photo Gallery" subtitle="Moments of faith, fellowship, and community" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 justify-center mb-10">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-colors ${
                category === cat
                  ? "bg-navy text-white"
                  : "bg-white text-gray-600 border border-gray-300 hover:border-primary hover:text-primary"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {isLoading ? (
          <LoadingSpinner />
        ) : !photos?.length ? (
          <p className="text-center text-gray-500 py-20">No photos found.</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {photos.map((photo) => (
              <div key={photo.id} className="group relative aspect-square rounded-xl overflow-hidden bg-gray-100 shadow-sm">
                <Image
                  src={getImageUrl(photo.image)}
                  alt={photo.title}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-dark/0 group-hover:bg-dark/60 transition-colors flex items-end">
                  <div className="p-3 text-white opacity-0 group-hover:opacity-100 transition-opacity">
                    <p className="text-sm font-semibold">{photo.title}</p>
                    {photo.caption && <p className="text-xs text-gray-300">{photo.caption}</p>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
