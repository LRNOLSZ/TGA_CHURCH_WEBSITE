import HeroBanner from "@/components/home/HeroBanner";
import ChurchInfoSection from "@/components/home/ChurchInfoSection";
import HeadPastorSection from "@/components/home/HeadPastorSection";
import FeaturedEvents from "@/components/home/FeaturedEvents";
import FeaturedSermons from "@/components/home/FeaturedSermons";
import TestimonialsCarousel from "@/components/home/TestimonialsCarousel";
import CTASection from "@/components/home/CTASection";
import FadeIn from "@/components/ui/FadeIn";

export const revalidate = 60;

export default function HomePage() {
  return (
    <>
      <HeroBanner />
      <FadeIn><ChurchInfoSection /></FadeIn>
      <FadeIn><HeadPastorSection /></FadeIn>
      <FadeIn><FeaturedEvents /></FadeIn>
      <FadeIn><FeaturedSermons /></FadeIn>
      <FadeIn><TestimonialsCarousel /></FadeIn>
      <FadeIn><CTASection /></FadeIn>
    </>
  );
}
