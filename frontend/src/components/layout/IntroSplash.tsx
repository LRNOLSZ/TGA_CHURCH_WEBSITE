"use client";

import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

const SEEN_KEY = "tga-intro-seen";

export default function IntroSplash() {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const alreadySeen = sessionStorage.getItem(SEEN_KEY);
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (alreadySeen || reducedMotion) {
      sessionStorage.setItem(SEEN_KEY, "1");
      setVisible(false);
      return;
    }

    document.body.style.overflow = "hidden";
  }, []);

  const dismiss = () => {
    sessionStorage.setItem(SEEN_KEY, "1");
    setVisible(false);
    document.body.style.overflow = "";
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="intro-splash"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          className="fixed inset-0 z-[100] bg-navy flex items-center justify-center"
        >
          <video
            autoPlay
            muted
            playsInline
            preload="auto"
            onEnded={dismiss}
            className="max-h-full max-w-full object-contain"
          >
            <source src="/videos/intro-mobile.mp4" media="(orientation: portrait)" />
            <source src="/videos/intro-desktop.mp4" media="(orientation: landscape)" />
          </video>
          <button
            onClick={dismiss}
            aria-label="Skip intro"
            className="tga-btn-hero-ghost absolute bottom-8 right-8 flex items-center gap-1.5"
          >
            Skip <X size={14} />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
