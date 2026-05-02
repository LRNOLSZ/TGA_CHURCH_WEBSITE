import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Our Branches",
  description:
    "Find a TGA Church branch near you. We have multiple locations across Ghana — discover service times and contact details for each campus.",
  openGraph: {
    title: "Our Branches | TGA Church",
    description:
      "Find a TGA Church branch near you. Multiple locations across Ghana with service times and contact details.",
  },
};

export default function BranchesLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
