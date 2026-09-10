import React from 'react';

type BrandMarkProps = { className?: string; label?: string };

export const BrandMark: React.FC<BrandMarkProps> = ({ className = '', label }) => (
  <span className={`dq-brand-mark ${className}`.trim()} role={label ? 'img' : undefined} aria-label={label} aria-hidden={label ? undefined : true}>
    <svg viewBox="0 0 64 64" focusable="false">
      <circle className="dq-brand-ring" cx="28" cy="35" r="18" />
      <path className="dq-brand-accent" d="M40.7 22.3A18 18 0 0 1 40.7 47.7" />
      <path className="dq-brand-tail" d="M39.5 46.5 48 55" />
      <rect className="dq-brand-dot" x="48" y="7" width="9" height="9" rx="2.5" />
    </svg>
  </span>
);
