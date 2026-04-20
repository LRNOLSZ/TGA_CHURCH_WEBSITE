"use client";

import { Clock } from "lucide-react";
import { useChurchInfo } from "@/hooks/useChurchData";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function ChurchInfoSection() {
  const { data: info, isLoading } = useChurchInfo();

  if (isLoading) return <LoadingSpinner />;
  if (!info) return null;

  return (
    <section className="bg-light py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Welcome */}
          <div>
            <div className="w-12 h-1 bg-accent mb-4" />
            <h2 className="text-3xl md:text-4xl font-bold text-primary mb-4">
              Welcome to {info.church_name}
            </h2>
            <p className="text-gray-600 text-lg leading-relaxed">{info.welcome_message}</p>
          </div>

          {/* Service Times */}
          <div className="bg-white rounded-2xl p-8 shadow-md">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Clock className="text-primary" size={24} />
              </div>
              <h3 className="text-xl font-bold text-primary">Service Times</h3>
            </div>
            <div className="whitespace-pre-line text-gray-600 leading-relaxed">
              {info.service_times_text}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
