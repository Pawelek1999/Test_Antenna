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

// Rejestracja niezbędnych elementów Chart.js
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

function ChartAntena({ selectedAntena }) {
  
  // Pobieramy limit z wybranej anteny lub ustawiamy domyślny 40, jeśli nic nie wybrano
  const chartTitle = selectedAntena ? `Wykres dla: ${selectedAntena.nazwa}` : "Wykres czułości (Wybierz częstotliwość)";

  const limitSOMFY = new Array(12).fill(selectedAntena ? selectedAntena.parametry.down_limit : 10);
  
  {/* const polarH = new Array(12).fill(0); 
  const result = ?; */}

  const data = {
    labels: ['0°', '30°', '60°', '90°', '120°', '150°', '180°', '210°', '240°', '270°', '300°', '330°'],
    datasets: [
      {
        label: 'Limit SOMFY',
        // Tutaj podstawiasz wartości z JSONa (np. stałą granicę)
        data: limitSOMFY,
        borderColor: 'red',
        backgroundColor: 'rgba(255, 0, 0, 0.1)',
        borderWidth: 2,
        fill: false,
      },
      {
        label: 'Polar H',
        // Wartości zmierzone pobierane z JSON
        data: [35, 38, 42, 45, 40, 32, 30, 35, 42, 44, 42, 38],
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: false,
        borderWidth: 1,
      }
    ],
  };

  const options = {
    scales: {
      r: {
        angleLines: { display: true },
        suggestedMin: 0,
        suggestedMax: 80, // Skala jest do 80 dBµV/m
        ticks: { stepSize: 20 }
      }
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4 bg-white rounded-lg shadow">
      <h3 className="text-center font-bold mb-4">{chartTitle}</h3>
      <Radar data={data} options={options} />
    </div>
  );
}

export default ChartAntena;