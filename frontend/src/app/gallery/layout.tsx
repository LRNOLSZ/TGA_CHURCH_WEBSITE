import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Photo Gallery",
  description:
    "Browse photos from TGA Church — moments of faith, fellowship, worship, and community captured across our locations.",
  openGraph: {
    title: "Photo Gallery | TGA Church",
    description:
      "Browse photos from TGA Church — moments of faith, fellowship, worship, and community.",
  },
};

export default function GalleryLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
