// frontend/mini-app/src/components/Card.tsx
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  gold?: boolean;
  hover?: boolean;
  onClick?: () => void;
  style?: React.CSSProperties;
}

export const Card: React.FC<CardProps> = ({ 
  children, 
  className = '', 
  gold = false, 
  hover = true, 
  onClick,
  style 
}) => {
  const baseClass = gold ? 'glass-card-gold' : 'glass-card';
  const hoverClass = hover ? 'card-hover' : '';
  
  return (
    <div 
      className={`${baseClass} ${hoverClass} ${className}`}
      onClick={onClick}
      style={style}
    >
      {children}
    </div>
  );
};

