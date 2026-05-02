import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Give & Support the Ministry",
  description:
    "Support the work of TGA Church through your generous giving. Your contribution makes a difference in lives across Ghana.",
  openGraph: {
    title: "Give & Support the Ministry | TGA Church",
    description:
      "Support the work of TGA Church through your generous giving. Your contribution makes a difference in lives across Ghana.",
  },
};

export default function GivingLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
