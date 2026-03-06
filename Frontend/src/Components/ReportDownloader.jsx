import React, { useState } from 'react';
import { saveAs } from 'file-saver';
import { Download } from 'lucide-react';

const ReportDownloader = ({ testResults, isTesting }) => {
  const [isProcessing, setIsProcessing] = useState(false);

  // Sprawdź, czy istnieją jakiekolwiek wyniki w którymkolwiek z arkuszy
  const hasResults = testResults && testResults.some(r => r.result && r.result.length > 0);

  const generateExcel = async () => {
    if (!hasResults) {
      alert("Brak dostępnych wyników do wyeksportowania.");
      return;
    }
    setIsProcessing(true);

    try {
        // Pobieramy raport wygenerowany na podstawie zapisanego wcześniej szablonu
        const response = await fetch('http://127.0.0.1:8000/generate-report', {
            method: 'GET',
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Błąd serwera: ${response.statusText}`);
        }

        const blob = await response.blob();
        saveAs(blob, `Raport_Anteny_${Date.now()}.xlsx`);
        
    } catch (error) {
        console.error("Błąd eksportu:", error);
        alert(`Wystąpił błąd podczas eksportu: ${error.message}`);
    } finally {
        setIsProcessing(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 flex flex-col justify-center">
      <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center"><Download className="w-4 h-4 mr-2"/> Pobierz Raport</h3>
      <button
        onClick={generateExcel}
        disabled={isProcessing || !hasResults || isTesting}
        className="w-full flex items-center justify-center py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isProcessing ? (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
        ) : (
          "Generuj Excel"
        )}
      </button>
    </div>
  );
};

export default ReportDownloader;
