import React, { useState, useEffect } from 'react';
import { Save, FileJson, Layers, Radio, Ruler } from 'lucide-react';
import { useConfig } from '../Components/ConfigContext';

const TestConfigForm = ({ onSaveSuccess }) => {
  const { setTestConfig, testConfig, frequenciesData } = useConfig();
  const [sheetCount, setSheetCount] = useState(1);
  // Tablica przechowująca wybrane ID częstotliwości dla każdego arkusza
  const [selectedFreqIds, setSelectedFreqIds] = useState([null, null, null]);
  const [antennas, setAntennas] = useState([]);
  const [selectedAntenna, setSelectedAntenna] = useState("");
  const [distance, setDistance] = useState(3);
  const [isSaving, setIsSaving] = useState(false);

  // Pobierz dostępne anteny
  useEffect(() => {
    fetch("/antennas.json")
      .then((res) => res.json())
      .then((data) => {
        setAntennas(data);
        // Ustaw domyślną antenę jeśli lista nie jest pusta
        if (data.length > 0) setSelectedAntenna(data[0].nazwa || data[0]);
      })
      .catch((err) => console.error("Błąd pobierania anten:", err));
  }, []);

  const availableFrequencies = frequenciesData || [];

  const handleSheetCountChange = (e) => {
    const count = parseInt(e.target.value, 10);
    setSheetCount(count);
  };

  const handleFreqChange = (index, freqId) => {
    const newSelected = [...selectedFreqIds];
    newSelected[index] = parseInt(freqId, 10);
    setSelectedFreqIds(newSelected);
  };

  const formatDate = (date) => {
    const d = date.getDate().toString().padStart(2, '0');
    const m = (date.getMonth() + 1).toString().padStart(2, '0');
    const y = date.getFullYear();
    const hh = date.getHours().toString().padStart(2, '0');
    const mm = date.getMinutes().toString().padStart(2, '0');
    return `${d}.${m}.${y} ${hh}:${mm}`;
  };

  // Funkcja generująca konfigurację na podstawie stanu formularza
  const generateConfig = () => {
    if (!selectedAntenna) return [];
    // Nie blokujemy generowania pustej tablicy w trakcie edycji, ale do zapisu wymagamy poprawności

    // Generowanie struktury JSON
    const configObjects = [];
    const currentDate = formatDate(new Date());

    for (let i = 0; i < sheetCount; i++) {
      const freqId = selectedFreqIds[i];
      const freqData = availableFrequencies.find(f => f.id === freqId);

      if (freqData) {
        configObjects.push({
          sheet: i + 1,
          id: i + 1,
          date: currentDate,
          description: `EMC sensitivity sweep test for ${freqData.frequency_mhz} MHz band`,
          antenna: selectedAntenna,
          test_params: {
            frequency_hz: Math.round(freqData.frequency_mhz * 1000000), // Konwersja MHz -> Hz
            wire_loss_db: freqData.wire_loss_db,
            antenna_factor_dbm_1: freqData.antenna_factor_dbm_1,
            distance: distance,
            angles: [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
            polarizations: ["V", "H"]
          }
        });
      }
    }
    return configObjects;
  };

  // Aktualizuj globalny kontekst przy każdej zmianie w formularzu
  useEffect(() => {
    const newConfig = generateConfig();
    setTestConfig(newConfig);
  }, [sheetCount, selectedFreqIds, selectedAntenna, distance, availableFrequencies]);

  const handleSave = async () => {
    if (!selectedAntenna) {
      alert("Wybierz antenę.");
      return;
    }

    // Walidacja: czy wybrano częstotliwość dla każdego aktywnego arkusza
    for (let i = 0; i < sheetCount; i++) {
      if (!selectedFreqIds[i]) {
        alert(`Wybierz częstotliwość dla Arkusza ${i + 1}`);
        return;
      }
    }

    setIsSaving(true);
    
    try {
      const response = await fetch('http://localhost:8000/save-test-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testConfig), // Używamy aktualnego stanu z kontekstu (lub wygenerowanego)
      });

      if (!response.ok) throw new Error('Błąd zapisu');
      
      const data = await response.json();
      alert(data.message);
      if (onSaveSuccess) {
        onSaveSuccess();
      }
    } catch (error) {
      console.error("Błąd:", error);
      alert("Nie udało się zapisać konfiguracji testu.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col">
      <div className="flex items-center mb-4 text-gray-800">
        <FileJson className="w-5 h-5 mr-2" />
        <h2 className="text-lg font-bold">Konfiguracja Testu (Multi-Sheet)</h2>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1 flex items-center">
            <Radio className="w-3 h-3 mr-1" /> Antena
          </label>
          <select
            value={selectedAntenna}
            onChange={(e) => setSelectedAntenna(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">-- Wybierz --</option>
            {antennas.map((ant, idx) => {
              const val = ant.nazwa || ant;
              return <option key={idx} value={val}>{val}</option>;
            })}
          </select>
        </div>
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1 flex items-center">
            <Ruler className="w-3 h-3 mr-1" /> Dystans (m)
          </label>
          <input
            type="number"
            value={distance}
            onChange={(e) => setDistance(parseFloat(e.target.value))}
            step="0.1"
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center">
          <Layers className="w-4 h-4 mr-1" /> Liczba Arkuszy (Sheets)
        </label>
        <select
          value={sheetCount}
          onChange={handleSheetCountChange}
          className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        >
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
        </select>
      </div>

      <div className="space-y-3 flex-grow">
        {Array.from({ length: sheetCount }).map((_, index) => (
          <div key={index} className="p-3 bg-gray-50 rounded-lg border border-gray-100">
            <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Arkusz {index + 1} - Częstotliwość</label>
            <select
              value={selectedFreqIds[index] || ""}
              onChange={(e) => handleFreqChange(index, e.target.value)}
              className="w-full p-2 text-sm border border-gray-300 rounded-md"
            >
              <option value="">-- Wybierz --</option>
              {availableFrequencies.map((freq) => (
                <option key={freq.id} value={freq.id}>
                  {freq.frequency_mhz} MHz ({freq.protocol} - {freq.country})
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>

      <button onClick={handleSave} disabled={isSaving} className="mt-6 w-full flex items-center justify-center py-2 px-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition shadow-md disabled:bg-gray-400">
        <Save className="w-4 h-4 mr-2" /> {isSaving ? 'Zapisywanie...' : 'Zapisz i kontynuuj'}
      </button>
    </div>
  );
};

export default TestConfigForm;
