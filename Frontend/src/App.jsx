import AntenaChoice from "./Components/AntenaChoice.jsx";
import { useState, useEffect, useRef } from "react";
import FrequencyChoice from "./Components/FrequencyChoice.jsx";
import ChartAntena from "./Components/ChartAntena.jsx";
import Table from "./Components/Table.jsx";
import DifferenceTable from "./Components/DifferenceTable.jsx";
import DistanceInput from "./Components/DistanceInput.jsx";
import PdfButton from "./Components/PdfButton.jsx";
import TestControl from "./Components/TestControl.jsx";
import somfyLogo from "./assets/Somfy_Logo.png";


function App() {
  const [selectedAntena, setSelectedAntena] = useState(null);
  const [antennasData, setAntennasData] = useState([]);

    useEffect(() => {
      fetch("/antennas.json")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => setAntennasData(data))
        .catch((error) => console.error("Błąd pobierania danych:", error));
    }, []);
  
const [distance, setDistance] = useState(3);
const [frequenciesData, setFrequenciesData] = useState([]);
const [selectedFrequency, setSelectedFrequency] = useState(null);

    useEffect(() => {
        fetch("/frequency.json")
            .then((response) => response.json())
            .then((data) => setFrequenciesData(data))
            .catch((error) => console.error("Błąd pobierania danych:", error));
    }, []);

// --- Logika Testu Anteny ---
  const [isTesting, setIsTesting] = useState(false);
  const [testResults, setTestResults] = useState(null);
  const pollingInterval = useRef(null);

  // Funkcja do sprawdzania statusu testu
  const checkTestStatus = async () => {
    try {
      const res = await fetch("http://localhost:8000/check-status");
      const statusData = await res.json();
      
      // Test zakończył się pomyślnie i wyniki są gotowe
      if (statusData.results_ready) {
        clearInterval(pollingInterval.current);
        const resultRes = await fetch("http://localhost:8000/download-data");
        const resultData = await resultRes.json();
        setTestResults(resultData);
        setIsTesting(false);
        console.log("Test zakończony, wyniki pobrane.");
      } 
      // Test przestał działać (został zatrzymany lub zakończył się błędem)
      else if (!statusData.is_running) {
        clearInterval(pollingInterval.current);
        setIsTesting(false);
        console.log("Test został zatrzymany lub zakończył się bez wyników.");
      }
      // W przeciwnym razie test wciąż trwa, nic nie robimy
    } catch (err) {
      console.error("Błąd podczas sprawdzania statusu:", err);
      clearInterval(pollingInterval.current);
      setIsTesting(false);
    }
  };

  const handleStartTest = async () => {
    // Sprawdzenie, czy test już nie jest w toku
    if (isTesting) return;

    setIsTesting(true);
    setTestResults(null); // Czyścimy poprzednie wyniki
    try {
      // 1. Uruchom test na backendzie
      const startRes = await fetch("http://localhost:8000/start-test", { method: "POST" });
      if (!startRes.ok) {
        // Jeśli backend zwrócił błąd (np. 409 Conflict), obsłuż go
        const errorData = await startRes.json();
        throw new Error(errorData.message || "Nie można uruchomić testu.");
      }
      
      // 2. Rozpocznij odpytywanie co 2 sekundy
      pollingInterval.current = setInterval(checkTestStatus, 2000); // Zmniejszono interwał dla lepszej responsywności

    } catch (error) {
      console.error("Nie udało się uruchomić testu:", error);
      alert(error.message); // Pokaż błąd użytkownikowi
      setIsTesting(false);
    }
  };

  const handleStopTest = async () => {
    if (!isTesting) return;

    try {
      await fetch("http://localhost:8000/stop-test", { method: "POST" });
      clearInterval(pollingInterval.current);
      setIsTesting(false);
      console.log("Wysłano żądanie zatrzymania testu.");
      // Nie czyścimy wyników, na wypadek gdyby użytkownik chciał zobaczyć częściowe dane (jeśli backend by to wspierał)
    } catch (error) {
      console.error("Nie udało się zatrzymać testu:", error);
      // Mimo błędu, zatrzymujemy UI
      clearInterval(pollingInterval.current);
      setIsTesting(false);
    }
  };

  // Czyszczenie interwału przy odmontowaniu komponentu
  useEffect(() => { return () => clearInterval(pollingInterval.current); }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4 sm:px-6 lg:px-8 print:p-0 print:bg-white">

      <div className="max-w-7xl mx-auto flex justify-between items-center mb-6">
        <img src={somfyLogo} alt="Somfy" className="h-20" />
        <div className="print:hidden">
          <PdfButton />
        </div>
      </div>

      <div id="printable" className="max-w-7xl mx-auto space-y-8 print:max-w-none print:w-full print:m-0">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 border-t-4 border-t-[#FDB913] p-6 space-y-6 print:break-inside-avoid print:shadow-none print:border-none print:p-0">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-50 rounded-lg p-4">
              <AntenaChoice 
                antennasData={antennasData} 
                selectedAntena={selectedAntena} 
                onAntenaSelect={setSelectedAntena} 
              />
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <FrequencyChoice 
                frequenciesData={frequenciesData} 
                selectedFrequency={selectedFrequency} 
                onFrequencySelect={setSelectedFrequency}
              />
            </div>
          </div>
          <div className="border-t border-gray-100 pt-6">
            <DistanceInput 
              distance={distance} 
              setDistance={setDistance} 
            />
          </div>
        </div>

        <div className="print:break-before-page">
          <Table 
            gen_data={testResults} 
            freq_data={selectedFrequency}
            distance={distance}
          />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start print:break-inside-avoid">
          <DifferenceTable gen_data={testResults} />
          <ChartAntena selectedAntena={selectedAntena} gen_data={testResults} />
        </div>

        <div className="print:hidden">
          <TestControl 
            handleStartTest={handleStartTest} 
            handleStopTest={handleStopTest} 
            isTesting={isTesting} 
          />
        </div>
      </div>
    </div>

  )
}

export default App;
