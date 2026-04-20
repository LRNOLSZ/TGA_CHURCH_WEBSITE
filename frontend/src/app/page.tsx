import HeroBanner from "@/components/home/HeroBanner";
import ChurchInfoSection from "@/components/home/ChurchInfoSection";
import HeadPastorSection from "@/components/home/HeadPastorSection";
import FeaturedEvents from "@/components/home/FeaturedEvents";
import FeaturedSermons from "@/components/home/FeaturedSermons";
import TestimonialsCarousel from "@/components/home/TestimonialsCarousel";
import CTASection from "@/components/home/CTASection";

export const revalidate = 60;

export default function HomePage() {
  return (
    <>
      <HeroBanner />
      <ChurchInfoSection />
      <HeadPastorSection />
      <FeaturedEvents />
      <FeaturedSermons />
      <TestimonialsCarousel />
      <CTASection />
    </>
  );
}
