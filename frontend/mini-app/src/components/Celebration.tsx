// frontend/mini-app/src/components/Celebration.tsx
import React, { useEffect, useState } from 'react';
import Confetti from 'react-confetti';

interface CelebrationProps {
  show: boolean;
  onComplete?: () => void;
  xpGained?: number;
  lessonTitle?: string;
}

export const Celebration: React.FC<CelebrationProps> = ({
  show,
  onComplete,
  xpGained = 50,
  lessonTitle = 'Урок',
}) => {
  const [isVisible, setIsVisible] = useState(show);

  useEffect(() => {
    if (show) {
      setIsVisible(true);
      // Автоматически скрываем через 3.5 секунды
      const timer = setTimeout(() => {
        setIsVisible(false);
        if (onComplete) onComplete();
      }, 3500);
      return () => clearTimeout(timer);
    }
  }, [show, onComplete]);

  if (!isVisible) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1000,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      pointerEvents: 'none',
    }}>
      {/* Конфетти */}
      <Confetti
        width={window.innerWidth}
        height={window.innerHeight}
        recycle={false}
        numberOfPieces={200}
        gravity={0.2}
        colors={['#FFD700', '#E3000F', '#00C853', '#2979FF', '#FF6D00', '#D500F9']}
      />

      {/* Поздравление */}
      <div style={{
        pointerEvents: 'auto',
        background: 'rgba(10, 14, 23, 0.85)',
        backdropFilter: 'blur(20px)',
        borderRadius: '24px',
        padding: '40px 48px',
        maxWidth: '400px',
        textAlign: 'center',
        border: '2px solid rgba(255, 215, 0, 0.2)',
        boxShadow: '0 24px 80px rgba(0, 0, 0, 0.6)',
        animation: 'fadeUp 0.5s ease-out',
      }}>
        <div style={{ fontSize: '64px', marginBottom: '8px' }}>🎉</div>
        <h2 style={{ color: '#FFD700', fontSize: '24px', fontWeight: '700', margin: '0 0 8px 0' }}>
          Урок завершён!
        </h2>
        <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '16px', margin: '0 0 12px 0' }}>
          «{lessonTitle}»
        </p>
        <div style={{
          display: 'inline-block',
          padding: '8px 20px',
          background: 'rgba(255, 215, 0, 0.15)',
          borderRadius: '20px',
          border: '1px solid rgba(255, 215, 0, 0.2)',
        }}>
          <span style={{ color: '#FFD700', fontSize: '18px', fontWeight: '600' }}>
            ⭐ +{xpGained} XP
          </span>
        </div>
        <p style={{ color: 'rgba(255,255,255,0.3)', fontSize: '13px', marginTop: '16px' }}>
          Продолжайте в том же духе! 💪
        </p>
      </div>
    </div>
  );
};

