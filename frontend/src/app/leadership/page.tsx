"use client";

import Image from "next/image";
import { Mail, Phone } from "lucide-react";
import { useLeaders } from "@/hooks/useChurchData";
import { getImageUrl } from "@/lib/utils";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function LeadershipPage() {
  const { data: leaders, isLoading } = useLeaders();

  return (
    <div className="bg-bg min-h-screen">
      <div className="bg-navy py-16 text-center">
        <SectionHeader title="Our Leadership Team" subtitle="Dedicated servants leading with faith and purpose" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {isLoading ? (
          <LoadingSpinner />
        ) : !leaders?.length ? (
          <p className="text-center text-gray-500 py-20">No leaders found.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {leaders.map((leader) => (
              <div key={leader.id} className="overflow-hidden group">
                {/* Photo */}
                <div className="relative h-64 bg-gray-100">
                  <Image
                    src={getImageUrl(leader.profile_picture)}
                    alt={leader.full_name}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-dark/70 to-transparent" />
                  <div className="absolute bottom-4 left-4 text-white">
                    <p className="font-bold text-lg">{leader.full_name}</p>
                    <p className="text-accent text-sm font-medium">{leader.position}</p>
                  </div>
                </div>

                {/* Content */}
                <div className="p-5">
                  <p className="text-gray-600 text-sm leading-relaxed line-clamp-4 mb-4">{leader.biography}</p>
                  <div className="space-y-1.5 text-sm">
                    {leader.email && (
                      <a href={`mailto:${leader.email}`} className="flex items-center gap-2 text-gray-500 hover:text-primary transition">
                        <Mail size={14} className="text-accent" />{leader.email}
                      </a>
                    )}
                    {leader.phone && (
                      <a href={`tel:${leader.phone}`} className="flex items-center gap-2 text-gray-500 hover:text-primary transition">
                        <Phone size={14} className="text-accent" />{leader.phone}
                      </a>
                    )}
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
