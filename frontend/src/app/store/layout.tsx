import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Church Store",
  description:
    "Browse the TGA Church store — books, devotionals, merchandise, and more to support your faith journey.",
  openGraph: {
    title: "Church Store | TGA Church",
    description:
      "Browse the TGA Church store — books, devotionals, merchandise, and more to support your faith journey.",
  },
};

export default function StoreLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
