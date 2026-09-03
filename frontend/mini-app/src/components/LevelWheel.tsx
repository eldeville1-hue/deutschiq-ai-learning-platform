// frontend/mini-app/src/components/LevelWheel.tsx
import React, { useEffect, useRef } from 'react';

interface LevelWheelProps {
  level: string;
  percentage: number;
  size?: number;
}

export const LevelWheel: React.FC<LevelWheelProps> = ({ level, percentage, size = 140 }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rotationRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
    ctx.scale(dpr, dpr);

    const radius = size / 2 - 16;
    const centerX = size / 2;
    const centerY = size / 2;

    let animationId: number;

    const draw = () => {
      rotationRef.current += 0.008;
      const rot = rotationRef.current;

      ctx.clearRect(0, 0, size, size);

      // Фоновый круг
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
      gradient.addColorStop(0, 'rgba(251, 191, 36, 0.05)');
      gradient.addColorStop(1, 'rgba(251, 191, 36, 0.01)');
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Основная дуга (прогресс)
      const startAngle = -Math.PI / 2 + rot;
      const endAngle = startAngle + (percentage / 100) * Math.PI * 2;

      // Тень
      ctx.shadowColor = 'rgba(251, 191, 36, 0.3)';
      ctx.shadowBlur = 20;

      const grad = ctx.createLinearGradient(0, 0, size, size);
      grad.addColorStop(0, '#FBBF24');
      grad.addColorStop(0.5, '#FCD34D');
      grad.addColorStop(1, '#F59E0B');
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius - 4, startAngle, endAngle);
      ctx.strokeStyle = grad;
      ctx.lineWidth = 10;
      ctx.lineCap = 'round';
      ctx.stroke();

      ctx.shadowBlur = 0;

      // Вращающиеся точки на дуге (эффект «колеса»)
      const dotCount = 12;
      for (let i = 0; i < dotCount; i++) {
        const angle = startAngle + (i / dotCount) * (endAngle - startAngle);
        const x = centerX + (radius - 14) * Math.cos(angle);
        const y = centerY + (radius - 14) * Math.sin(angle);
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = i % 2 === 0 ? 'rgba(251, 191, 36, 0.6)' : 'rgba(251, 191, 36, 0.2)';
        ctx.fill();
      }

      // Текст уровня в центре
      ctx.shadowColor = 'rgba(251, 191, 36, 0.2)';
      ctx.shadowBlur = 30;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = `bold ${size * 0.22}px Inter, sans-serif`;
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(level, centerX, centerY - 10);

      ctx.font = `${size * 0.11}px Inter, sans-serif`;
      ctx.fillStyle = '#FBBF24';
      ctx.shadowBlur = 10;
      ctx.fillText(`${Math.round(percentage)}%`, centerX, centerY + 26);

      ctx.shadowBlur = 0;

      animationId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationId);
    };
  }, [percentage, level, size]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        width: size,
        height: size,
        display: 'block',
      }}
    />
  );
};

