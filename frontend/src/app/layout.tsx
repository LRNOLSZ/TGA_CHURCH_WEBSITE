import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import QueryProvider from "@/providers/QueryProvider";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { Analytics } from "@vercel/analytics/next";

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
  icons: {
    icon: "/favicon.png",
    apple: "/favicon.png",
  },
  title: {
    default: "TGA Global — Building Faith, Changing Lives",
    template: "%s | TGA Global",
  },
  description:
    "TGA Global (The Gospel Appraisal) is a Spirit-filled Christian community led by Head Pastor Kelvin Offeh Gyimah, with branches in Ghana (Accra, Kumasi), the USA (Baton Rouge), and Tanzania. Committed to building faith, changing lives, and serving communities worldwide.",
  keywords: [
    "TGA Global", "TGA", "The Gospel Appraisal",
    "church Ghana", "Christian church", "church Accra", "church Kumasi",
    "sermons", "worship", "Pastor Kelvin Offeh Gyimah",
  ],
  openGraph: {
    type: "website",
    siteName: "TGA Global",
    title: "TGA Global — Building Faith, Changing Lives",
    description:
      "TGA Global (The Gospel Appraisal) is a Spirit-filled Christian community led by Head Pastor Kelvin Offeh Gyimah, with branches in Ghana (Accra, Kumasi), the USA (Baton Rouge), and Tanzania. Committed to building faith, changing lives, and serving communities worldwide.",
    url: siteUrl,
  },
  twitter: {
    card: "summary_large_image",
    title: "TGA Global — Building Faith, Changing Lives",
    description:
      "TGA Global (The Gospel Appraisal) is a Spirit-filled Christian community led by Head Pastor Kelvin Offeh Gyimah, with branches in Ghana (Accra, Kumasi), the USA (Baton Rouge), and Tanzania. Committed to building faith, changing lives, and serving communities worldwide.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

const churchSchema = {
  "@context": "https://schema.org",
  "@type": "Church",
  name: "TGA Global",
  url: siteUrl,
  description:
    "TGA Global (The Gospel Appraisal) is a Spirit-filled Christian community led by Head Pastor Kelvin Offeh Gyimah, with branches in Ghana (Accra, Kumasi), the USA (Baton Rouge), and Tanzania. Committed to building faith, changing lives, and serving communities worldwide.",
  sameAs: [
    "https://youtube.com/@t_gbn",
    "https://www.tiktok.com/@p_k_o_g",
    "https://pkog.net",
    "https://www.instagram.com/p_k_o_g_",
    "https://www.instagram.com/tgag_lobal",
  ],
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
        <SpeedInsights />
        <Analytics />
      </body>
    </html>
  );
}
