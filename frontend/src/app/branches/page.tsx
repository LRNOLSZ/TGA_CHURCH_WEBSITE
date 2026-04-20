"use client";

import Image from "next/image";
import { MapPin, Phone, Mail, User, ExternalLink, Clock } from "lucide-react";
import { useBranches } from "@/hooks/useBranches";
import { getImageUrl } from "@/lib/utils";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function BranchesPage() {
  const { data: branches, isLoading } = useBranches();

  const main = branches?.find((b) => b.is_main_branch);
  const others = branches?.filter((b) => !b.is_main_branch) ?? [];

  return (
    <div className="bg-light min-h-screen">
      <div className="bg-primary py-16 text-center">
        <SectionHeader title="Our Branches" subtitle="Find a TGA Church near you" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <>
            {/* Main Branch */}
            {main && (
              <div className="mb-12">
                <div className="flex items-center gap-2 mb-6">
                  <span className="bg-accent text-white text-xs font-bold px-3 py-1 rounded-full uppercase">Main Branch</span>
                </div>
                <BranchCard branch={main} featured />
              </div>
            )}

            {/* Other Branches */}
            {others.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {others.map((branch) => (
                  <BranchCard key={branch.id} branch={branch} />
                ))}
              </div>
            )}

            {!branches?.length && (
              <p className="text-center text-gray-500 py-20">No branches found.</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function BranchCard({ branch, featured = false }: { branch: import("@/types").Branch; featured?: boolean }) {
  return (
    <div className={`bg-white rounded-2xl shadow-md overflow-hidden ${featured ? "border-2 border-accent" : ""}`}>
      {branch.image && (
        <div className="relative h-56">
          <Image src={getImageUrl(branch.image)} alt={branch.name} fill className="object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-dark/60 to-transparent" />
          <div className="absolute bottom-4 left-4 text-white">
            <h3 className="text-xl font-bold">{branch.name}</h3>
          </div>
        </div>
      )}

      <div className="p-6">
        {!branch.image && <h3 className="text-xl font-bold text-primary mb-4">{branch.name}</h3>}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-start gap-2">
              <MapPin size={15} className="text-accent mt-0.5 shrink-0" />
              <span>{branch.location}</span>
            </div>
            {branch.phone && (
              <div className="flex items-center gap-2">
                <Phone size={15} className="text-accent shrink-0" />
                <a href={`tel:${branch.phone}`} className="hover:text-primary transition">{branch.phone}</a>
              </div>
            )}
            {branch.email && (
              <div className="flex items-center gap-2">
                <Mail size={15} className="text-accent shrink-0" />
                <a href={`mailto:${branch.email}`} className="hover:text-primary transition">{branch.email}</a>
              </div>
            )}
            {branch.pastor_in_charge && (
              <div className="flex items-center gap-2">
                <User size={15} className="text-accent shrink-0" />
                <span>{branch.pastor_in_charge}</span>
              </div>
            )}
          </div>

          {/* Service Times */}
          {branch.service_times?.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-primary mb-2 flex items-center gap-1">
                <Clock size={13} /> Service Times
              </h4>
              <ul className="space-y-1 text-sm text-gray-600">
                {branch.service_times.filter((st) => st.is_active).map((st) => (
                  <li key={st.id} className="flex justify-between">
                    <span className="font-medium">{st.day}</span>
                    <span>{st.time} — {st.service_type}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {branch.google_maps_url && (
          <a
            href={branch.google_maps_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-blue-800 transition"
          >
            <MapPin size={14} /> View on Google Maps <ExternalLink size={13} />
          </a>
        )}
      </div>
    </div>
  );
}
