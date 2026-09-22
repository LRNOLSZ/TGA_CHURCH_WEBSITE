import Image from "next/image";
import { MapPin, Phone, Mail, User, ExternalLink, Clock } from "lucide-react";
import { getImageUrl } from "@/lib/utils";
import type { Branch } from "@/types";

export default function BranchCard({ branch, featured = false }: { branch: Branch; featured?: boolean }) {
  return (
    <div className={`overflow-hidden ${featured ? "border-2 border-accent rounded-2xl" : ""}`}>
      {branch.image && (
        <div className="relative h-56 rounded-xl overflow-hidden group transition-shadow duration-300 hover:shadow-[0_0_20px_4px_rgba(212,175,55,0.5)]">
          <Image src={getImageUrl(branch.image)} alt={branch.name} fill className="object-cover transition-transform duration-500 group-hover:scale-105" />
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
