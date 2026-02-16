import { useState, useEffect } from 'react';

const DifferenceTable = () => {
  const [activation, setActivation] = useState(0);
  const [stopValue, setStopValue] = useState("");
  const [gap, setGap] = useState(0);

  useEffect(() => {
    // Pobieramy wartość bazową Activation z JSON
    fetch("/differenceData.json")
      .then((res) => res.json())
      .then((json) => {
        setActivation(json.activation);
      })
      .catch((err) => console.error("Error loading JSON:", err));
  }, []);

  // Funkcja przeliczająca Gap po wpisaniu Stop
  const handleStopChange = (e) => {
    const val = e.target.value;
    setStopValue(val);
    
    if (val !== "") {
      // Obliczamy Gap jako wartość bezwzględną
      const calculatedGap = Math.abs(activation - parseFloat(val));
      setGap(calculatedGap);
    } else {
      setGap(0);
    }
  };

  return (
    <div className="mt-8 font-sans text-left">
      <h3 className="text-sm font-bold mb-1 underline italic">
        Difference between Activation and Stop order:
      </h3>
      
      <table className="border-collapse border-2 border-black text-sm">
        <tbody>
          <tr>
            <td className="border border-black px-6 py-4 font-bold w-32 text-center" rowSpan={3}>
              Angle / Polar
            </td>
            <td className="border border-black px-4 py-1 bg-white text-center w-32 font-medium">
              Activation
            </td>
            <td className="border border-black px-4 py-1 text-blue-700 font-bold text-center min-w-[120px]">
              {activation} dBm
            </td>
          </tr>
          <tr>
            <td className="border border-black px-4 py-1 bg-white text-center font-medium">
              Stop
            </td>
            <td className="border border-black p-0 bg-[#FFCC99]">
              <input 
                type="number"
                value={stopValue}
                onChange={handleStopChange}
                placeholder="Enter value"
                className="w-full h-full px-4 py-1 text-red-600 font-bold text-center bg-transparent focus:outline-none appearance-none"
              />
            </td>
          </tr>
          <tr>
            <td className="border border-black px-4 py-1 bg-white text-center font-medium">
              Gap
            </td>
            <td className="border border-black px-4 py-1 text-blue-700 font-bold text-center bg-[#E6F3FF]">
              {gap} dB
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default DifferenceTable;