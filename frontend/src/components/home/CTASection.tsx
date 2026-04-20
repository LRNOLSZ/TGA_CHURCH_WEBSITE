import Link from "next/link";
import { CalendarDays, Heart, MessageCircle } from "lucide-react";

export default function CTASection() {
  return (
    <section className="bg-dark py-16">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">Get Involved</h2>
        <div className="w-16 h-1 bg-accent mx-auto mb-4" />
        <p className="text-gray-400 text-lg mb-10">There are many ways to connect with our community.</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/events"
            className="group p-8 bg-white/5 border border-white/10 rounded-2xl hover:bg-primary/80 transition-all"
          >
            <CalendarDays size={40} className="text-accent mx-auto mb-4" />
            <h3 className="text-white font-bold text-xl mb-2">View Events</h3>
            <p className="text-gray-400 text-sm group-hover:text-gray-200">Join us at upcoming church events and programs</p>
          </Link>

          <Link
            href="/giving"
            className="group p-8 bg-accent/90 border border-accent rounded-2xl hover:bg-accent transition-all"
          >
            <Heart size={40} className="text-white mx-auto mb-4" />
            <h3 className="text-white font-bold text-xl mb-2">Give Now</h3>
            <p className="text-white/80 text-sm group-hover:text-white">Support the ministry and spread the gospel</p>
          </Link>

          <Link
            href="/contact"
            className="group p-8 bg-white/5 border border-white/10 rounded-2xl hover:bg-primary/80 transition-all"
          >
            <MessageCircle size={40} className="text-accent mx-auto mb-4" />
            <h3 className="text-white font-bold text-xl mb-2">Contact Us</h3>
            <p className="text-gray-400 text-sm group-hover:text-gray-200">Reach out with questions, prayer requests, or feedback</p>
          </Link>
        </div>
      </div>
    </section>
  );
}
