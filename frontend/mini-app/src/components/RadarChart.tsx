import React from 'react';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface RadarChartProps {
  data: {
    labels: string[];
    values: number[];
  };
  maxValue?: number;
  label?: string;
  height?: number;
  compact?: boolean;
}

export const RadarChart: React.FC<RadarChartProps> = ({
  data,
  maxValue = 10,
  label = 'Оценка',
  height = 220,
  compact = false,
}) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: label,
        data: data.values,
        backgroundColor: compact ? 'rgba(130, 174, 248, 0.16)' : 'rgba(251, 191, 36, 0.15)',
        borderColor: compact ? '#82AEF8' : '#FBBF24',
        borderWidth: 2,
        pointBackgroundColor: compact ? '#82AEF8' : '#FBBF24',
        pointBorderColor: '#FFFFFF',
        pointHoverBackgroundColor: '#FFFFFF',
        pointHoverBorderColor: '#FBBF24',
      },
    ],
  };

  const options = {
    scales: {
      r: {
        beginAtZero: true,
        max: maxValue,
        ticks: {
          stepSize: 2,
          color: 'rgba(255,255,255,0.4)',
          backdropColor: 'transparent',
          display: !compact,
        },
        grid: {
          color: 'rgba(255,255,255,0.06)',
        },
        angleLines: {
          color: 'rgba(255,255,255,0.06)',
        },
        pointLabels: {
          color: 'rgba(255,255,255,0.7)',
          font: {
            size: compact ? 9 : 11,
            weight: '500' as any,
          },
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(11, 17, 32, 0.9)',
        titleColor: '#FFFFFF',
        bodyColor: '#FBBF24',
        borderColor: 'rgba(255,255,255,0.06)',
        borderWidth: 1,
      },
    },
    animation: { duration: 500 },
    maintainAspectRatio: false,
  };

  return (
    <div style={{ width: '100%', height: `${height}px`, position: 'relative' }}>
      <Radar data={chartData} options={options} />
    </div>
  );
};
