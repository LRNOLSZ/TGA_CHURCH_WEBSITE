import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // TGA brand
        navy: "#0b1e3f",
        "navy-2": "#152a52",
        "navy-ink": "#0a1530",
        gold: "#c9a24a",
        "gold-2": "#b28a30",
        "gold-soft": "#e6cf91",
        // surfaces
        bg: "#f1ebde",
        "bg-2": "#e9e1cf",
        paper: "#f6efe0",
        // text
        ink: "#1a1a1a",
        muted: "#6b6458",
        // legacy aliases so existing pages stay consistent
        primary: "#0b1e3f",
        accent: "#c9a24a",
        dark: "#0a1530",
        light: "#f1ebde",
        "text-main": "#1a1a1a",
      },
      fontFamily: {
        display: ["var(--font-fraunces)", "serif"],
        sans: ["var(--font-inter)", "Inter", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", '"JetBrains Mono"', "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
