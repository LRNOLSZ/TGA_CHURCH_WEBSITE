import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sermons & Messages",
  description:
    "Watch and listen to sermons and messages from TGA Church. Be inspired and strengthened through the Word of God.",
  openGraph: {
    title: "Sermons & Messages | TGA Church",
    description:
      "Watch and listen to sermons and messages from TGA Church. Be inspired and strengthened through the Word of God.",
  },
};

export default function SermonsLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
