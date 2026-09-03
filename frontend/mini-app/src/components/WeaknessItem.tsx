// frontend/mini-app/src/components/WeaknessItem.tsx
import React from 'react';

export const WeaknessItem: React.FC<{ name: string; percent: number }> = ({ name, percent }) => {
  const color = percent > 30 ? '#E3000F' : percent > 20 ? '#FF8C00' : '#FFD700';
  const glow = percent > 30 ? '0 0 12px rgba(227,0,15,0.15)' : '0 0 12px rgba(255,140,0,0.1)';
  return (
    <div style={{ marginBottom: '12px', padding: '14px 16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.04)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ color: 'rgba(255,255,255,0.85)', fontSize: '14px', fontWeight: '500' }}>{name}</span>
        <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: '13px', fontWeight: '600' }}>{percent}%</span>
      </div>
      <div className="progress-bar" style={{ height: '4px' }}>
        <div className="progress-bar-fill" style={{ width: `${percent}%`, background: color, boxShadow: glow }} />
      </div>
    </div>
  );
};

