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
}

export const RadarChart: React.FC<RadarChartProps> = ({
  data,
  maxValue = 10,
  label = 'Оценка',
}) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: label,
        data: data.values,
        backgroundColor: 'rgba(251, 191, 36, 0.15)',
        borderColor: '#FBBF24',
        borderWidth: 2,
        pointBackgroundColor: '#FBBF24',
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
            size: 11,
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
    maintainAspectRatio: false,
  };

  return (
    <div style={{ width: '100%', height: '220px', position: 'relative' }}>
      <Radar data={chartData} options={options} />
    </div>
  );
};

