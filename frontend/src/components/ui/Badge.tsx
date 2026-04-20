interface BadgeProps {
  children: React.ReactNode;
  variant?: "primary" | "accent" | "white";
}

export default function Badge({ children, variant = "primary" }: BadgeProps) {
  const variants = {
    primary: "bg-primary text-white",
    accent: "bg-accent text-dark",
    white: "bg-white text-primary",
  };
  return (
    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ${variants[variant]}`}>
      {children}
    </span>
  );
}
