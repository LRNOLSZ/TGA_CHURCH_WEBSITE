"use client";

import { useChurchInfo, useServiceTimes } from "@/hooks/useChurchData";

export default function ChurchInfoSection() {
  const { data: info } = useChurchInfo();
  const { data: serviceTimes } = useServiceTimes();

  return (
    <section className="bg-bg" style={{ paddingTop: "clamp(48px, 8vw, 96px)", paddingBottom: "clamp(48px, 8vw, 96px)" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="tga-two-col">

          {/* ── LEFT: Welcome copy ── */}
          <div className="flex flex-col justify-center">
            {/* Eyebrow with gold bar */}
            <div className="flex items-center gap-3 mb-5">
              <span
                className="block shrink-0"
                style={{ width: "28px", height: "2px", background: "#c9a24a" }}
              />
              <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em]">
                01 — Welcome
              </p>
            </div>

            <h2
              className="font-display text-navy mb-5"
              style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400, lineHeight: 1.1 }}
            >
              A place to{" "}
              <em className="italic text-gold">belong,</em>
              <br />grow, and serve.
            </h2>

            <p className="text-muted leading-[1.75] mb-8" style={{ fontSize: "16px", maxWidth: "480px" }}>
              {info?.welcome_message ||
                "We are a family of believers committed to faith, community, and the transforming power of the Gospel."}
            </p>

          </div>

          {/* ── RIGHT: Navy service times card ── */}
          <div
            className="relative overflow-hidden p-6 md:p-10"
            style={{
              background: "#0b1e3f",
              borderRadius: "20px",
            }}
          >
            {/* Decorative gold radial glow */}
            <div
              className="absolute top-0 right-0 pointer-events-none"
              style={{
                width: "240px",
                height: "240px",
                background: "radial-gradient(circle at top right, rgba(201,162,74,0.18) 0%, transparent 70%)",
              }}
            />

            <p className="font-mono text-gold-2 text-[11px] uppercase tracking-[0.22em] mb-3 relative z-10">
              Service Times
            </p>
            <h3
              className="font-display text-white mb-6 relative z-10"
              style={{ fontSize: "clamp(22px, 3.5vw, 32px)", fontWeight: 400, lineHeight: 1.1 }}
            >
              Join us this week.
            </h3>

            {/* Service list */}
            <div className="relative z-10">
              {serviceTimes && serviceTimes.length > 0 ? (
                serviceTimes.map((st, i) => (
                  <div key={st.id}>
                    {i > 0 && (
                      <div style={{ height: "1px", background: "rgba(255,255,255,0.10)", margin: "0" }} />
                    )}
                    <div
                      className="flex items-center gap-4 py-4"
                    >
                      <span
                        className="font-mono text-gold shrink-0"
                        style={{ fontSize: "12px", minWidth: "54px", textTransform: "uppercase", letterSpacing: "0.08em" }}
                      >
                        {st.day.slice(0, 3)}
                      </span>
                      <span
                        className="font-display text-white"
                        style={{ fontSize: "18px", fontWeight: 400 }}
                      >
                        {st.time}
                      </span>
                      <span
                        className="font-mono text-[#9a9080] ml-auto"
                        style={{ fontSize: "11px", textAlign: "right" }}
                      >
                        {st.service_type}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                /* Fallback: render service_times_text */
                <p className="text-[#c8bfaa] leading-relaxed whitespace-pre-line" style={{ fontSize: "15px" }}>
                  {info?.service_times_text || "Sunday Service: 9:00 AM & 11:00 AM\nWednesday Bible Study: 7:00 PM"}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
