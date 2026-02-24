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
  const distanceNum = parseNum(distance);
  const valid = Number.isFinite(freq) && freq > 0 && Number.isFinite(distanceNum) && distanceNum > 0;

  // Obliczanie statystyk (Średnia, Min, Max)
  const stats = { h_act: [], h_stop: [], v_act: [], v_stop: [] };
  if (gen_data) {
    gen_data.forEach(row => {
      const add = (arr, val) => { const n = parseNum(val); if (Number.isFinite(n)) arr.push(n); };
      add(stats.h_act, row.genPolarH_act);
      add(stats.h_stop, row.genPolarH_stop);
      add(stats.v_act, row.genPolarV_act);
      add(stats.v_stop, row.genPolarV_stop);
    });
  }

  const calcStats = (arr) => {
    if (arr.length === 0) return { avg: NaN, min: NaN, max: NaN };
    const sum = arr.reduce((a, b) => a + b, 0);
    const min = Math.min(...arr);
    const max = Math.max(...arr);
    return { avg: sum / arr.length, min, max };
  };

  const s_h_act = calcStats(stats.h_act);
  const s_h_stop = calcStats(stats.h_stop);
  const s_v_act = calcStats(stats.v_act);
  const s_v_stop = calcStats(stats.v_stop);

  const getSens = (genVal) => {
    if (!valid || !Number.isFinite(genVal)) return { db: NaN, uv: NaN };
    const db = genVal - wireLoss - (20 * Math.log10(distanceNum)) + (20 * Math.log10(freq)) - antFactor + 75.01;
    const uv = Math.pow(10, db / 20);
    return { db, uv };
  };

  const renderSummaryRow = (label, type) => {
    const h_act = s_h_act[type];
    const h_stop = s_h_stop[type];
    const v_act = s_v_act[type];
    const v_stop = s_v_stop[type];
    const sensH = getSens(h_act);
    const sensV = getSens(v_act);

    return (
      <tr key={label} className="font-bold bg-gray-100 border-t-2 border-gray-300 text-gray-900">
        <td className="border border-gray-300 p-3 text-left print:p-1">{label}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(h_act)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(h_stop)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(v_act)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(v_stop)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensH.db)} dBµV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensH.uv)} µV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensV.db)} dBµV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensV.uv)} µV/m</td>
      </tr>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 border-t-4 border-t-[#FDB913] overflow-hidden print:shadow-none print:border-none print:p-0">
      <h2 className="text-xl font-bold text-[#1A1A1A] mb-6 print:text-lg print:mb-2">Sensitivity values for activation order</h2>
      <div className="overflow-x-auto print:overflow-visible">
      <table 
        className="min-w-full border-collapse border border-gray-300 text-sm text-center print:text-[10px] print:w-full"
        style={{ printColorAdjust: 'exact', WebkitPrintColorAdjust: 'exact' }}
      >
        <thead>
          {/* Poziom 1 */}
          <tr className="bg-[#1A1A1A] text-white">
            <th className="border border-gray-600 p-3 font-medium print:p-1" rowSpan={3}>Angle</th>
            <th className="border border-gray-600 p-3 font-medium print:p-1" colSpan={4}>Generator values</th>
            <th className="border border-gray-600 p-3 font-medium print:p-1" colSpan={4}>Sensitivity value for "activation" order</th>
          </tr>
          {/* Poziom 2 */}
          <tr className="bg-gray-100 text-gray-800">
            <th className="border border-gray-300 p-2 font-medium print:p-1" colSpan={2}>Polar H</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1" colSpan={2}>Polar V</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1" colSpan={2}>Polar H</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1" colSpan={2}>Polar V</th>
          </tr>
          {/* Poziom 3 */}
          <tr className="bg-gray-50 text-xs text-gray-600 uppercase tracking-wider print:text-[9px]">
            <th className="border border-gray-300 p-2 font-medium print:p-1">Activation order</th>
            <th className="border border-gray-300 p-2 font-medium italic print:p-1">Stop order**</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1">Activation order</th>
            <th className="border border-gray-300 p-2 font-medium italic print:p-1">Stop order**</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1">E(dBµV/m)</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1">E(µV/m)</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1">E(dBµV/m)</th>
            <th className="border border-gray-300 p-2 font-medium print:p-1">E(µV/m)</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
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
                <td className="border border-gray-300 p-2 font-semibold bg-gray-50 text-gray-900 print:p-1">{row.angle}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarH_act}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarH_stop}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarV_act}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarV_stop}</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{formatOrDash(sensH_db)} dBµV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{formatOrDash(sensH_uv)} µV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{formatOrDash(sensV_db)} dBµV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{formatOrDash(sensV_uv)} µV/m</td>
              </tr>
            );
            })
          ) : (
            <tr>
              <td className="border border-gray-300 p-4 italic text-gray-500 print:p-2" colSpan={9}>No data available</td>
            </tr>
          )}
          {gen_data && gen_data.length > 0 && (
            <>
              {renderSummaryRow("Średnia", "avg")}
              {renderSummaryRow("Wartość minimalna", "min")}
              {renderSummaryRow("Wartość maksymalna", "max")}
            </>
          )}
        </tbody>
      </table>
      </div>
    </div>
  ); 
};

export default Table;