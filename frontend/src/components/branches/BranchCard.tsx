import Image from "next/image";
import { MapPin, Phone, Mail, User, ExternalLink, Clock, Radio } from "lucide-react";
import { getImageUrl } from "@/lib/utils";
import { useChurchInfo } from "@/hooks/useChurchData";
import SocialLinks from "@/components/ui/SocialLinks";
import type { Branch } from "@/types";

export default function BranchCard({ branch, featured = false }: { branch: Branch; featured?: boolean }) {
  const { data: churchInfo } = useChurchInfo();

  return (
    <div className={`overflow-hidden ${featured ? "border-2 border-accent rounded-2xl" : ""}`}>
      {branch.is_satellite && (
        <div className="flex justify-center pt-4">
          <span className="inline-flex items-center gap-1.5 bg-navy text-white text-xs font-bold px-3 py-1 rounded-full uppercase">
            <Radio size={12} /> Online
          </span>
        </div>
      )}

      {branch.image && (
        <div className="relative aspect-[16/10] rounded-xl overflow-hidden group transition-shadow duration-300 hover:shadow-[0_0_20px_4px_rgba(212,175,55,0.5)]">
          <Image src={getImageUrl(branch.image)} alt={branch.name} fill className="object-cover transition-transform duration-500 group-hover:scale-105" />
          <div className="absolute inset-0 bg-gradient-to-t from-dark/60 to-transparent" />
          <div className="absolute bottom-4 inset-x-0 text-center text-white">
            <h3 className="text-xl font-bold">{branch.name}</h3>
          </div>
        </div>
      )}

      <div className="p-6 text-center">
        {!branch.image && <h3 className="text-xl font-bold text-primary mb-4">{branch.name}</h3>}

        <div className="flex flex-col gap-4 mb-6">
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-start gap-2 justify-center">
              <MapPin size={15} className="text-accent mt-0.5 shrink-0" />
              <span>{branch.location || "Meets Online"}</span>
            </div>
            {branch.phone && (
              <div className="flex items-center gap-2 justify-center">
                <Phone size={15} className="text-accent shrink-0" />
                <a href={`tel:${branch.phone}`} className="hover:text-primary transition">{branch.phone}</a>
              </div>
            )}
            {branch.email && (
              <div className="flex items-center gap-2 justify-center">
                <Mail size={15} className="text-accent shrink-0" />
                <a href={`mailto:${branch.email}`} className="hover:text-primary transition">{branch.email}</a>
              </div>
            )}
            {branch.pastor_in_charge && (
              <div className="flex items-center gap-2 justify-center">
                <User size={15} className="text-accent shrink-0" />
                <span>{branch.pastor_in_charge}</span>
              </div>
            )}
          </div>

          {/* Service Times */}
          {branch.service_times?.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-primary mb-2 flex items-center justify-center gap-1">
                <Clock size={13} /> Service Times
              </h4>
              <ul className="space-y-1 text-sm text-gray-600">
                {branch.service_times.filter((st) => st.is_active).map((st) => (
                  <li key={st.id}>
                    <span className="font-medium">{st.day}:</span> {st.time} — {st.service_type}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {branch.is_satellite ? (
          (churchInfo?.youtube_channel_url || churchInfo?.tiktok_url) && (
            <div className="flex flex-col items-center gap-2">
              <span className="text-xs font-semibold text-muted uppercase tracking-wide">Catch us online</span>
              <SocialLinks
                youtube={churchInfo?.youtube_channel_url}
                tiktok={churchInfo?.tiktok_url}
                iconSize={22}
              />
            </div>
          )
        ) : (
          branch.google_maps_url && (
            <a
              href={branch.google_maps_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-blue-800 transition"
            >
              <MapPin size={14} /> View on Google Maps <ExternalLink size={13} />
            </a>
          )
        )}
      </div>
    </div>
  );
}
