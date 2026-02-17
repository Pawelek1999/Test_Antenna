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

function ChartAntena({ selectedAntena, gen_data }) {
  
  // Pobieramy limit z wybranej anteny lub ustawiamy domyślny 40, jeśli nic nie wybrano
  const chartTitle = selectedAntena ? `Wykres dla: ${selectedAntena.nazwa}` : "Wykres czułości (Wybierz częstotliwość)";

  const limitSOMFY = new Array(12).fill(selectedAntena ? selectedAntena.parametry.down_limit : 10);
  
  {/* const polarH = new Array(12).fill(0); 
  const result = ?; */}
  
  const labels = ['0°', '30°', '60°', '90°', '120°', '150°', '180°', '210°', '240°', '270°', '300°', '330°'];

  const polarHData = labels.map(label => {
    if (!gen_data) return 0;
    const row = gen_data.find(r => r.angle === label);
    if (row) {
      const val = parseFloat(row.genPolarH_act);
      return Number.isFinite(val) ? val : 0;
    }
    return 0;
  });

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Limit SOMFY',
        // Tutaj podstawiasz wartości z JSONa dla Anten (np. stałą granicę)
        data: limitSOMFY,
        borderColor: 'red',
        backgroundColor: 'rgba(255, 0, 0, 0.1)',
        borderWidth: 2,
        fill: false,
      },
      {
        label: 'Polar H',
        // Wartości zmierzone pobierane z JSON
        data: polarHData,
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: false,
        borderWidth: 3,
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
    <div className="w-full bg-white rounded-xl shadow-lg p-6 border border-gray-100 border-t-4 border-t-[#FDB913]">
      <h3 className="text-center text-lg font-bold text-[#1A1A1A] mb-6">{chartTitle}</h3>
      <div className="relative aspect-square max-w-md mx-auto">
        <Radar data={data} options={options} />
      </div>
    </div>
  );
}

export default ChartAntena;