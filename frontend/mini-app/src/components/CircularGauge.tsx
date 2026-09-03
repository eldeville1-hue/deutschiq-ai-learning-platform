// frontend/mini-app/src/components/CircularGauge.tsx
import React from 'react';

interface CircularGaugeProps {
  level: string;
  percentage: string;
  size?: number;
}

export const CircularGauge: React.FC<CircularGaugeProps> = ({ level, percentage, size = 140 }) => {
  const radius = 55;
  const strokeWidth = 8;
  const circumference = 2 * Math.PI * radius;
  const progress = parseInt(percentage) / 100;
  const dashOffset = circumference * (1 - progress);

  return (
    <div style={{ width: size, height: size, position: 'relative' }}>
      <svg width={size} height={size} viewBox="0 0 140 140">
        <circle cx="70" cy="70" r={radius} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth={strokeWidth} />
        <circle cx="70" cy="70" r={radius} fill="none" stroke="#FFD700" strokeWidth={strokeWidth} strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={dashOffset} transform="rotate(-90 70 70)" style={{ transition: 'stroke-dashoffset 1s ease-in-out' }} />
        <circle cx="70" cy="70" r={radius} fill="none" stroke="#FFD700" strokeWidth={2} strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={dashOffset} transform="rotate(-90 70 70)" opacity="0.3" filter="blur(6px)" />
        <text x="70" y="62" textAnchor="middle" fill="#FFFFFF" fontSize="22" fontWeight="bold">{level}</text>
        <text x="70" y="88" textAnchor="middle" fill="#FFD700" fontSize="16" fontWeight="600">{percentage}</text>
      </svg>
    </div>
  );
};

