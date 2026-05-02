import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact Us",
  description:
    "Get in touch with TGA Church. We would love to hear from you — reach out with questions, prayer requests, or to learn more about our community.",
  openGraph: {
    title: "Contact TGA Church",
    description:
      "Get in touch with TGA Church. Reach out with questions, prayer requests, or to learn more about our community.",
  },
};

export default function ContactLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
