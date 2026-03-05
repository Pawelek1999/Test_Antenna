import React, { useState } from 'react';
import { FileCheck, RefreshCw, CheckCircle } from 'lucide-react';
import { useConfig } from '../Components/ConfigContext';

const ConfigSummary = ({ onConfirm }) => {
  const { hardwareConfig, runtimeParams, testConfig, refreshConfig } = useConfig();
  const [loading, setLoading] = useState(false);

  const handleMergeAndSave = async () => {
    setLoading(true);
    try {
      // Używamy danych bezpośrednio z kontekstu (które są aktualizowane na bieżąco przez formularze)
      const freshHardwareConfig = hardwareConfig;
      const freshRuntimeParams = runtimeParams;
      const freshTestConfig = testConfig;

      if (!freshHardwareConfig || Object.keys(freshHardwareConfig).length === 0 || 
          !freshRuntimeParams || Object.keys(freshRuntimeParams).length === 0 || 
          !freshTestConfig || freshTestConfig.length === 0) {
        throw new Error("Brakuje danych konfiguracyjnych. Upewnij się, że zapisałeś wszystkie formularze.");
      }

      // 2. Logika scalania: Dla każdego obiektu w testConfig (sheet) dodajemy hardware i runtime params
      const mergedConfig = freshTestConfig.map(sheet => ({
        ...sheet,
        hardware_config: freshHardwareConfig,
        runtime_params: freshRuntimeParams
      }));

      // 3. Zapisz scalony plik
      const response = await fetch('http://127.0.0.1:8000/save-we-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mergedConfig),
      });

      if (!response.ok) throw new Error('Błąd zapisu na serwerze');

      const data = await response.json();
      alert(data.message);
      if (onConfirm) {
        onConfirm();
      }
    } catch (error) {
      console.error("Błąd scalania:", error);
      alert(`Nie udało się zapisać pliku we_config.json: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderJsonPreview = (data, title) => (
    <div className="mb-4">
      <h4 className="text-xs font-bold text-gray-500 uppercase mb-1">{title}</h4>
      <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-32 border border-gray-200">
        {data ? JSON.stringify(data, null, 2) : <span className="text-red-500">Brak danych</span>}
      </pre>
    </div>
  );

  return (
    <div className="max-w-xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4 text-gray-800">
        <div className="flex items-center">
          <FileCheck className="w-5 h-5 mr-2" />
          <h2 className="text-lg font-bold">Podsumowanie Konfiguracji</h2>
        </div>
        <button 
          onClick={refreshConfig} 
          className="p-1 hover:bg-gray-100 rounded-full transition" 
          title="Odśwież dane"
        >
          <RefreshCw className={`w-4 h-4 text-gray-500 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="flex-grow overflow-y-auto pr-1">
        {renderJsonPreview(hardwareConfig, "Hardware Config")}
        {renderJsonPreview(runtimeParams, "Runtime Params")}
        
        <div className="mb-4">
          <h4 className="text-xs font-bold text-gray-500 uppercase mb-1">Test Config (Sheets)</h4>
          {testConfig && testConfig.length > 0 ? (
            <div className="space-y-2">
              {testConfig.map((sheet, idx) => (
                <div key={idx} className="bg-blue-50 p-2 rounded border border-blue-100 text-xs">
                  <span className="font-semibold">Sheet {sheet.sheet}:</span> {sheet.description}
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-gray-100 p-2 rounded text-xs text-red-500 border border-gray-200">
              Brak danych
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-gray-100">
        <p className="text-sm text-gray-600 mb-3 text-center">
          Czy parametry są poprawne?
        </p>
        <button 
          onClick={handleMergeAndSave}
          disabled={loading || !hardwareConfig || !runtimeParams || !testConfig}
          className="w-full flex items-center justify-center py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg transition shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          <CheckCircle className="w-5 h-5 mr-2" />
          Zatwierdź i Generuj we_config.json
        </button>
      </div>
    </div>
  );
};

export default ConfigSummary;
