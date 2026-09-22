"use client";

import { ChevronRight } from "lucide-react";

export interface Crumb {
  label: string;
  onClick?: () => void;
}

export default function Breadcrumb({ crumbs }: { crumbs: Crumb[] }) {
  return (
    <nav className="flex items-center flex-wrap gap-1.5 text-sm mb-8" aria-label="Breadcrumb">
      {crumbs.map((crumb, i) => {
        const isLast = i === crumbs.length - 1;
        return (
          <span key={i} className="flex items-center gap-1.5">
            {crumb.onClick && !isLast ? (
              <button
                onClick={crumb.onClick}
                className="text-navy/70 hover:text-gold transition font-medium"
              >
                {crumb.label}
              </button>
            ) : (
              <span className={isLast ? "text-navy font-semibold" : "text-navy/70"}>
                {crumb.label}
              </span>
            )}
            {!isLast && <ChevronRight size={14} className="text-navy/30" />}
          </span>
        );
      })}
    </nav>
  );
}
