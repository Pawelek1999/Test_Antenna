import { useState } from 'react';

const DifferenceTable = ({ gen_data }) => {
  const [stopValue, setStopValue] = useState("");

  // Obliczanie wartości Activation (Minimum z genPolarH_act i genPolarV_act)
  const getActivation = () => {
    if (!gen_data || gen_data.length === 0) return "Enter value";
    
    let minVal = Infinity;
    let found = false;

    gen_data.forEach(row => {
      const h = parseFloat(row.genPolarH_act);
      const v = parseFloat(row.genPolarV_act);
      
      if (!isNaN(h)) { minVal = Math.min(minVal, h); found = true; }
      if (!isNaN(v)) { minVal = Math.min(minVal, v); found = true; }
    });

    return found ? minVal : "Enter value";
  };

  const activation = getActivation();

  // Obliczanie Gap
  const gap = (activation !== "Enter value" && stopValue !== "" && !isNaN(parseFloat(stopValue)))
    ? Math.abs(activation - parseFloat(stopValue))
    : 0;

  // Funkcja przeliczająca Gap po wpisaniu Stop
  const handleStopChange = (e) => {
    setStopValue(e.target.value);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 border-t-4 border-t-[#FDB913] h-full">
      <h3 className="text-lg font-bold text-[#1A1A1A] mb-2">
        Difference Analysis
      </h3>
      <p className="text-sm text-gray-500 mb-6 italic">Difference between Activation and Stop order</p>
      
      <div className="overflow-hidden rounded-lg border border-gray-200">
        <table className="w-full text-sm text-left border-collapse">
          <tbody className="divide-y divide-gray-200">
          <tr>
            <td className="bg-gray-50 px-4 py-4 font-semibold text-gray-700 w-32 text-center border-r border-gray-200" rowSpan={3}>
              Angle / Polar
            </td>
            <td className="px-4 py-3 bg-white text-center font-medium text-gray-600 border-r border-gray-200">
              Activation
            </td>
            <td className="px-4 py-3 text-[#1A1A1A] font-bold text-center min-w-[120px]">
              {activation === "Enter value" ? activation : `${activation} dBm`}
            </td>
          </tr>
          <tr>
            <td className="px-4 py-3 bg-white text-center font-medium text-gray-600 border-r border-gray-200">
              Stop
            </td>
            <td className="p-2 bg-gray-50">
              <input 
                type="number"
                value={stopValue}
                onChange={handleStopChange}
                placeholder="Enter value"
                className="w-full px-3 py-1.5 text-gray-900 font-bold text-center bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#FDB913] focus:border-transparent transition-shadow"
              />
            </td>
          </tr>
          <tr>
            <td className="px-4 py-3 bg-white text-center font-medium text-gray-600 border-r border-gray-200">
              Gap
            </td>
            <td className="px-4 py-3 text-[#1A1A1A] font-bold text-center bg-gray-50">
              {typeof gap === 'number' ? gap.toFixed(2) : gap} dB
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>
  );
};

export default DifferenceTable;