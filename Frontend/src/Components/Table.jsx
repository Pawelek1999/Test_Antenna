import React, { useState } from 'react';

function Table({ gen_data, freq_data, distance }) {
  
  const parseNum = (v, fallback = NaN) => {
    if (v === null || v === undefined) return fallback;
    if (typeof v === 'string') {
      const cleaned = v.replace(',', '.').replace(/[^0-9.+-eE]/g, '');
      const n = Number(cleaned);
      return Number.isFinite(n) ? n : fallback;
    }
    const n = Number(v);
    return Number.isFinite(n) ? n : fallback;
  };

  const formatOrDash = (v, digits = 2) => {
    return Number.isFinite(v) ? v.toFixed(digits) : '-';
  };

  // Debug
  console.log("Table freq_data:", freq_data);
  console.log("Table distance:", distance);

  const freqMHz = parseNum(freq_data?.frequency_mhz);
  const freq = Number.isFinite(freqMHz) ? freqMHz : NaN; // convert MHz -> Hz
  const wireLoss = parseNum(freq_data?.wire_loss_db, 0);
  const antFactor = parseNum(freq_data?.antenna_factor_dbm_1, 0);

  return (
    <div className="p-6 overflow-x-auto bg-white">
      <h2 className="text-lg font-bold mb-4 underline">Sensitivity values for activation order:</h2>
      <table className="min-w-full border-collapse border border-black text-sm text-center">
        <thead>
          {/* Poziom 1 */}
          <tr>
            <th className="border border-black p-2" rowSpan={3}>Angle</th>
            <th className="border border-black p-2" colSpan={4}>Generator values</th>
            <th className="border border-black p-2" colSpan={4}>Sensitivity value for "activation" order</th>
          </tr>
          {/* Poziom 2 */}
          <tr>
            <th className="border border-black p-2" colSpan={2}>Polar H</th>
            <th className="border border-black p-2" colSpan={2}>Polar V</th>
            <th className="border border-black p-2" colSpan={2}>Polar H</th>
            <th className="border border-black p-2" colSpan={2}>Polar V</th>
          </tr>
          {/* Poziom 3 */}
          <tr className="text-[11px]">
            <th className="border border-black p-1">Activation order</th>
            <th className="border border-black p-1 italic">Stop order**</th>
            <th className="border border-black p-1">Activation order</th>
            <th className="border border-black p-1 italic">Stop order**</th>
            <th className="border border-black p-1">E(dBµV/m)</th>
            <th className="border border-black p-1">E(µV/m)</th>
            <th className="border border-black p-1">E(dBµV/m)</th>
            <th className="border border-black p-1">E(µV/m)</th>
          </tr>
        </thead>
        <tbody>
          {gen_data ? (gen_data.map((row, index) => {
            const genH = parseNum(row.genPolarH_act);
            const genV = parseNum(row.genPolarV_act);
            const distanceNum = parseNum(distance);
            const valid = Number.isFinite(freq) && freq > 0 && Number.isFinite(distanceNum) && distanceNum > 0;

            let sensH_db = NaN;
            let sensV_db = NaN;
            if (valid) {
              sensH_db = genH - wireLoss - (20 * Math.log10(distanceNum)) + (20 * Math.log10(freq)) - antFactor + 75.01;
              sensV_db = genV - wireLoss - (20 * Math.log10(distanceNum)) + (20 * Math.log10(freq)) - antFactor + 75.01;
            }

            const sensH_uv = Number.isFinite(sensH_db) ? Math.pow(10, sensH_db / 20) : NaN;
            const sensV_uv = Number.isFinite(sensV_db) ? Math.pow(10, sensV_db / 20) : NaN;

            return (
              <tr key={index}>
                <td className="border border-black p-2 font-semibold bg-gray-50">{row.angle}</td>
                <td className="border border-black p-2 bg-gray-300">{row.genPolarH_act}</td>
                <td className="border border-black p-2 bg-gray-300">{row.genPolarH_stop}</td>
                <td className="border border-black p-2 bg-gray-300">{row.genPolarV_act}</td>
                <td className="border border-black p-2 bg-gray-300">{row.genPolarV_stop}</td>
                <td className="border border-black p-2">{formatOrDash(sensH_db)} dBµV/m</td>
                <td className="border border-black p-2">{formatOrDash(sensH_uv)} µV/m</td>
                <td className="border border-black p-2">{formatOrDash(sensV_db)} dBµV/m</td>
                <td className="border border-black p-2">{formatOrDash(sensV_uv)} µV/m</td>
              </tr>
            );
            })
            
          ) : (
            <tr>
              <td className="border border-black p-2 italic" colSpan={9}>No data available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Table;