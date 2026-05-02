import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Our Leadership",
  description:
    "Meet the leadership team at TGA Church — dedicated servants leading with faith and purpose to serve God and the community.",
  openGraph: {
    title: "Our Leadership | TGA Church",
    description:
      "Meet the leadership team at TGA Church — dedicated servants leading with faith and purpose.",
  },
};

export default function LeadershipLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
