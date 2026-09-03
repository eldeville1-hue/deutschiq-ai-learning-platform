// frontend/mini-app/src/components/Badge.tsx
import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'gold' | 'red' | 'gray';
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'gray' }) => {
  const variants = {
    gold: 'badge-gold',
    red: 'badge-red',
    gray: 'badge-gray',
  };
  
  return <span className={`badge ${variants[variant]}`}>{children}</span>;
};

