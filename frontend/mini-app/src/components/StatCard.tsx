// frontend/mini-app/src/components/StatCard.tsx
import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  trend: 'up' | 'down';
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, trend }) => {
  const color = trend === 'up' ? '#FFD700' : '#E3000F';
  const arrow = trend === 'up' ? '↑' : '↓';
  const points = trend === 'up' 
    ? '0,12 10,4 20,8 30,2 40,6 50,0'
    : '0,0 10,8 20,4 30,10 40,6 50,12';

  const numericValue = typeof value === 'string' ? parseFloat(value) : value;

  return (
    <div className="glass-card" style={{ padding: '16px 14px', display: 'flex', flexDirection: 'column', minHeight: '88px', cursor: 'pointer' }}
    onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = 'var(--shadow-hover), var(--gold-glow)'; }}
    onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'var(--shadow)'; }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
        <span style={{ color: 'var(--text-secondary)', fontSize: '11px', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.3px' }}>
          {label}
        </span>
        <span style={{ color, fontSize: '16px', fontWeight: '700' }}>
          {numericValue.toFixed(1)} {arrow}
        </span>
      </div>
      <svg width="100%" height="20" viewBox="0 0 50 14" style={{ marginTop: '6px' }}>
        <polyline
          points={points}
          fill="none"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter={trend === 'up' ? 'drop-shadow(0 0 6px rgba(255,215,0,0.3))' : 'none'}
        />
        <polyline
          points={points}
          fill="none"
          stroke={color}
          strokeWidth="4"
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity="0.15"
        />
      </svg>
    </div>
  );
};

