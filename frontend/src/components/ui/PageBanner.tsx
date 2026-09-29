import SectionHeader from "./SectionHeader";

export default function PageBanner({
  title,
  subtitle,
}: {
  title: string;
  subtitle?: string;
}) {
  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-navy to-navy-2 py-16 text-center">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.06]"
        style={{
          backgroundImage: "radial-gradient(circle, #c9a24a 1px, transparent 1px)",
          backgroundSize: "22px 22px",
        }}
      />
      <div className="pointer-events-none absolute -top-16 -left-10 w-64 h-64 rounded-full bg-gold/15 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-20 -right-10 w-72 h-72 rounded-full bg-gold-soft/10 blur-3xl" />
      <div className="relative">
        <SectionHeader title={title} subtitle={subtitle} light divider />
      </div>
    </div>
  );
}
