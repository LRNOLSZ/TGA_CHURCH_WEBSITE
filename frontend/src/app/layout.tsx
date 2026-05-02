import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import QueryProvider from "@/providers/QueryProvider";

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  weight: ["400", "500"],
  display: "swap",
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://tgachurch.org";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "TGA Church — Building Faith, Changing Lives",
    template: "%s | TGA Church",
  },
  description:
    "TGA Church is a Spirit-filled Christian community committed to building faith, changing lives, and serving communities across Ghana.",
  keywords: ["TGA Church", "church Ghana", "Christian church", "church Accra", "sermons", "worship"],
  openGraph: {
    type: "website",
    siteName: "TGA Church",
    title: "TGA Church — Building Faith, Changing Lives",
    description:
      "TGA Church is a Spirit-filled Christian community committed to building faith, changing lives, and serving communities across Ghana.",
    url: siteUrl,
  },
  twitter: {
    card: "summary_large_image",
    title: "TGA Church — Building Faith, Changing Lives",
    description:
      "TGA Church is a Spirit-filled Christian community committed to building faith, changing lives, and serving communities across Ghana.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

const churchSchema = {
  "@context": "https://schema.org",
  "@type": "Church",
  name: "TGA Church",
  url: siteUrl,
  description:
    "TGA Church is a Spirit-filled Christian community committed to building faith, changing lives, and serving communities across Ghana.",
  sameAs: [],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${fraunces.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(churchSchema) }}
        />
      </head>
      <body className="antialiased">
        <QueryProvider>
          <Navbar />
          <main className="min-h-screen">{children}</main>
          <Footer />
        </QueryProvider>
      </body>
    </html>
  );
}
