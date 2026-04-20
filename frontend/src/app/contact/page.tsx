"use client";

import { MapPin, Phone, Mail } from "lucide-react";
import { useChurchInfo } from "@/hooks/useChurchData";
import SectionHeader from "@/components/ui/SectionHeader";
import SocialLinks from "@/components/ui/SocialLinks";
import ContactForm from "@/components/forms/ContactForm";

export default function ContactPage() {
  const { data: info } = useChurchInfo();

  return (
    <div className="bg-light min-h-screen">
      <div className="bg-primary py-16 text-center">
        <SectionHeader title="Get In Touch" subtitle="We would love to hear from you" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-10">
          {/* Contact Info */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-2xl shadow-md p-8">
              <h3 className="text-xl font-bold text-primary mb-6">Contact Information</h3>
              <div className="space-y-4 text-sm text-gray-600">
                {info?.address && (
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg shrink-0 mt-0.5">
                      <MapPin size={16} className="text-primary" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 mb-0.5">Address</p>
                      <p className="whitespace-pre-line">{info.address}</p>
                    </div>
                  </div>
                )}
                {info?.phone && (
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg shrink-0">
                      <Phone size={16} className="text-primary" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 mb-0.5">Phone</p>
                      <a href={`tel:${info.phone}`} className="hover:text-primary transition">{info.phone}</a>
                    </div>
                  </div>
                )}
                {info?.email && (
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg shrink-0">
                      <Mail size={16} className="text-primary" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 mb-0.5">Email</p>
                      <a href={`mailto:${info.email}`} className="hover:text-primary transition">{info.email}</a>
                    </div>
                  </div>
                )}
              </div>

              {/* Social Links */}
              {info && (
                <div className="mt-6 pt-6 border-t border-gray-100">
                  <p className="text-sm font-medium text-gray-800 mb-3">Follow Us</p>
                  <SocialLinks
                    youtube={info.youtube_channel_url}
                    facebook={info.facebook_url}
                    instagram={info.instagram_url}
                    twitter={info.twitter_url}
                    whatsapp={info.whatsapp_url}
                    tiktok={info.tiktok_url}
                    className="gap-4"
                    iconSize={22}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Contact Form */}
          <div className="lg:col-span-3 bg-white rounded-2xl shadow-md p-8">
            <h3 className="text-xl font-bold text-primary mb-6">Send a Message</h3>
            <ContactForm />
          </div>
        </div>
      </div>
    </div>
  );
}
