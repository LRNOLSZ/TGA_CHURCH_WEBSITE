import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Upcoming Events",
  description:
    "Join TGA Church for upcoming events — worship services, fellowships, community outreach, and more across Ghana.",
  openGraph: {
    title: "Upcoming Events | TGA Church",
    description:
      "Join TGA Church for upcoming events — worship services, fellowships, community outreach, and more across Ghana.",
  },
};

export default function EventsLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
