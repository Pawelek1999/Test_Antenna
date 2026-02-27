import React, { useState } from 'react';

function Table({ gen_data }) {
  
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

  // Obliczanie statystyk (Średnia, Min, Max)
  const stats = { 
    h_act: [], h_stop: [], v_act: [], v_stop: [],
    sens_h_db: [], sens_h_uv: [], sens_v_db: [], sens_v_uv: []
  };
  if (gen_data) {
    gen_data.forEach(row => {
      const add = (arr, val) => { const n = parseNum(val); if (Number.isFinite(n)) arr.push(n); };
      add(stats.h_act, row.genPolarH_act);
      add(stats.h_stop, row.genPolarH_stop);
      add(stats.v_act, row.genPolarV_act);
      add(stats.v_stop, row.genPolarV_stop);
      add(stats.sens_h_db, row.sens_genPolarH_act_db);
      add(stats.sens_h_uv, row.sens_genPolarH_act_uv);
      add(stats.sens_v_db, row.sens_genPolarV_act_db);
      add(stats.sens_v_uv, row.sens_genPolarV_act_uv);
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
  const s_sens_h_db = calcStats(stats.sens_h_db);
  const s_sens_h_uv = calcStats(stats.sens_h_uv);
  const s_sens_v_db = calcStats(stats.sens_v_db);
  const s_sens_v_uv = calcStats(stats.sens_v_uv);

  const renderSummaryRow = (label, type) => {
    const h_act = s_h_act[type];
    const h_stop = s_h_stop[type];
    const v_act = s_v_act[type];
    const v_stop = s_v_stop[type];
    const sensH_db = s_sens_h_db[type];
    const sensH_uv = s_sens_h_uv[type];
    const sensV_db = s_sens_v_db[type];
    const sensV_uv = s_sens_v_uv[type];

    return (
      <tr key={label} className="font-bold bg-gray-100 border-t-2 border-gray-300 text-gray-900">
        <td className="border border-gray-300 p-3 text-left print:p-1">{label}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(h_act)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(h_stop)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(v_act)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(v_stop)}</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensH_db)} dBµV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensH_uv)} µV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensV_db)} dBµV/m</td>
        <td className="border border-gray-300 p-3 print:p-1">{formatOrDash(sensV_uv)} µV/m</td>
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
            return (
              <tr key={index}>
                <td className="border border-gray-300 p-2 font-semibold bg-gray-50 text-gray-900 print:p-1">{row.angle}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarH_act}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarH_stop}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarV_act}</td>
                <td className="border border-gray-300 p-2 bg-gray-50 text-gray-700 print:p-1">{row.genPolarV_stop}</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{row.sens_genPolarH_act_db} dBµV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{row.sens_genPolarH_act_uv} µV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{row.sens_genPolarV_act_db} dBµV/m</td>
                <td className="border border-gray-300 p-2 text-gray-900 print:p-1">{row.sens_genPolarV_act_uv} µV/m</td>
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