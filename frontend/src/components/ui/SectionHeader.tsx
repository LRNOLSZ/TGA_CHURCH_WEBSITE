interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  eyebrow?: string;
  centered?: boolean;
  light?: boolean;
  divider?: boolean;
}

export default function SectionHeader({
  title,
  subtitle,
  eyebrow,
  centered = true,
  light = false,
  divider = false,
}: SectionHeaderProps) {
  return (
    <div className={`mb-12 ${centered ? "text-center" : ""}`}>
      {eyebrow && (
        <p
          className={`font-mono text-[11px] uppercase tracking-[0.22em] mb-3 ${
            light ? "text-gold-soft" : "text-gold-2"
          }`}
        >
          {eyebrow}
        </p>
      )}
      <h2
        className={`font-display mb-4 ${light ? "text-white" : "text-navy"}`}
        style={{ fontSize: "clamp(36px, 4.6vw, 56px)", fontWeight: 400, lineHeight: 1.1 }}
      >
        {title}
      </h2>
      {divider && (
        <span className="mx-auto mb-4 block h-[2px] w-16 rounded-full bg-gradient-to-r from-transparent via-gold to-transparent" />
      )}
      {subtitle && (
        <p
          className={`text-base leading-relaxed max-w-2xl ${centered ? "mx-auto" : ""} ${
            light ? "text-[rgba(255,255,255,0.7)]" : "text-muted"
          }`}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
}
