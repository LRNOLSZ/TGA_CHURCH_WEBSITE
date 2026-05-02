import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Us",
  description:
    "Learn about TGA Church — our story, mission, vision, core values, and service times. A community built on faith across Ghana.",
  openGraph: {
    title: "About TGA Church",
    description:
      "Learn about TGA Church — our story, mission, vision, core values, and service times.",
  },
};

export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
