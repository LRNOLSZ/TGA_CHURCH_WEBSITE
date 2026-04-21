interface BadgeProps {
  children: React.ReactNode;
  variant?: "primary" | "accent" | "white";
}

export default function Badge({ children, variant = "primary" }: BadgeProps) {
  const variants = {
    primary: "bg-navy text-white",
    accent: "bg-gold text-navy-ink",
    white: "bg-paper text-navy",
  };
  return (
    <span
      className={`inline-block px-3 py-1 text-[10px] font-mono uppercase tracking-[0.12em] ${variants[variant]}`}
      style={{ borderRadius: "3px" }}
    >
      {children}
    </span>
  );
}
