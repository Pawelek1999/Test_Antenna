import { useState, useEffect, useRef } from "react";
import ChartAntena from "./Components/ChartAntena.jsx";
import Table from "./Components/Table.jsx";
import DifferenceTable from "./Components/DifferenceTable.jsx";
import TestControl from "./Components/TestControl.jsx";
import somfyLogo from "./assets/Somfy_Logo.png";
import TemplateUploader from "./Components/TemplateUploader.jsx";
import ReportDownloader from "./Components/ReportDownloader.jsx";
import RuntimeParamsForm from "./Components/RuntimeParamsForm.jsx";
import HardwareConfigForm from "./Components/HardwareConfigForm.jsx";
import TestConfigForm from "./Components/TestConfigForm.jsx";
import ConfigSummary from "./Components/ConfigSummary.jsx";
import { useConfig } from "./Components/ConfigContext.jsx";


function App() {
  const [configStep, setConfigStep] = useState(1);
  const [antennasData, setAntennasData] = useState([]);
  const [currentSheetView, setCurrentSheetView] = useState(1);

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
  
    // Pobierz dane i funkcję do odświeżania z globalnego kontekstu
    const { frequenciesData, fetchFrequencies } = useConfig();

    const handleTemplateUploadSuccess = () => {
      fetchFrequencies();
      setConfigStep(2);
    };
  
    const nextStep = () => {
      setConfigStep(prev => prev + 1);
    };

// --- Logika Testu Anteny ---
  const [isTesting, setIsTesting] = useState(false);
  const [testResults, setTestResults] = useState(null);
  const pollingInterval = useRef(null);

  // Funkcja do sprawdzania statusu testu
  const checkTestStatus = async () => {
    try {
      const res = await fetch("http://localhost:8000/check-status");
      const statusData = await res.json();
      
      // Jeśli test trwa, ale są już dostępne częściowe wyniki, pobierz je dla podglądu (Live Update)
      if (statusData.is_running && statusData.results_ready) {
        const resultRes = await fetch("http://localhost:8000/download-data");
        const resultData = await resultRes.json();
        setTestResults(resultData);
      }

      // Test zakończył się pomyślnie i wyniki są gotowe
      if (!statusData.is_running && statusData.results_ready) {
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

  const renderWizard = () => (
    <div className="max-w-xl mx-auto py-10">
      {configStep === 1 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold mb-4">Krok 1: Wgraj szablon Excel</h2>
          <p className="text-sm text-gray-600 mb-4">Przeciągnij plik `.xlsx` z szablonem raportu. Spowoduje to odczytanie dostępnych częstotliwości do testów.</p>
          <TemplateUploader onUploadSuccess={handleTemplateUploadSuccess} />
        </div>
      )}
      {configStep === 2 && <HardwareConfigForm onSaveSuccess={nextStep} />}
      {configStep === 3 && <RuntimeParamsForm onSaveSuccess={nextStep} />}
      {configStep === 4 && <TestConfigForm onSaveSuccess={nextStep} />}
      {configStep === 5 && <ConfigSummary onConfirm={nextStep} />}
    </div>
  );

  const renderMainApp = () => {
    // Znajdź dane dla aktualnie wybranego arkusza
    const currentSheetData = testResults?.find(r => r.sheet === currentSheetView);
    const displayResults = currentSheetData ? currentSheetData.result : null;

    // Znajdź obiekt anteny dla wykresu na podstawie nazwy z wyników testu
    const antennaName = currentSheetData?.antenna;
    const antennaObjectForChart = antennasData.find(a => a.nazwa === antennaName);

    // Przygotuj listę dostępnych arkuszy do przełączania widoku
    const availableSheets = testResults
      ?.filter(r => r.result && r.result.length > 0)
      .map(r => r.sheet) || [];
      
    return (
      <div id="printable" className="max-w-7xl mx-auto space-y-8 print:max-w-none print:w-full print:m-0">
        
        <div className="print:hidden">
          <TestControl 
            handleStartTest={handleStartTest} 
            handleStopTest={handleStopTest} 
            isTesting={isTesting} 
          />
        </div>

        {availableSheets.length > 1 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 print:hidden">
            <h3 className="text-sm font-bold text-gray-700 mb-2">Wybierz widok arkusza</h3>
            <div className="flex flex-wrap gap-2">
              {availableSheets.map(sheetNum => (
                <button
                  key={sheetNum}
                  onClick={() => setCurrentSheetView(sheetNum)}
                  className={`px-4 py-2 rounded-md text-sm font-semibold transition ${
                    currentSheetView === sheetNum
                      ? 'bg-indigo-600 text-white shadow'
                      : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                  }`}
                >
                  Arkusz {sheetNum}
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 border-t-4 border-t-[#FDB913] p-6 space-y-6 print:break-inside-avoid print:shadow-none print:border-none print:p-0">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-50 rounded-lg p-4 flex flex-col gap-4">
              <ReportDownloader testResults={testResults} isTesting={isTesting} />
            </div>
          </div>
        </div>

        <div className="print:break-before-page">
          <Table 
            gen_data={displayResults} 
          />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start print:break-inside-avoid">
          <DifferenceTable gen_data={displayResults} />
          <ChartAntena selectedAntena={antennaObjectForChart} gen_data={displayResults} />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans py-10 px-4 sm:px-6 lg:px-8 print:p-0 print:bg-white">

      <div className="max-w-7xl mx-auto flex justify-between items-center mb-6">
        <img src={somfyLogo} alt="Somfy" className="h-20" />
      </div>

      {configStep <= 5 ? renderWizard() : renderMainApp()}
    </div>

  )
}

export default App;
