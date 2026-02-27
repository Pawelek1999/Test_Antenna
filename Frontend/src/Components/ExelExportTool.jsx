import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { saveAs } from 'file-saver';
import { Download, FileUp, CheckCircle2 } from 'lucide-react'; // Opcjonalne ikony

const ExcelExportTool = ({ testResults }) => {
  const [templateFile, setTemplateFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    setTemplateFile(file);

    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      // Automatyczna aktualizacja częstotliwości po upuszczeniu pliku
      fetch('http://localhost:8000/update-frequencies-from-excel', {
        method: 'POST',
        body: formData,
      })
        .then(async (res) => {
          const data = await res.json();
          if (!res.ok) {
            throw new Error(data.detail || 'Wystąpił błąd podczas przetwarzania pliku.');
          }
          return data;
        })
        .then((data) => {
          alert(`${data.message}\nOdśwież stronę (F5), aby zobaczyć nowe częstotliwości na liście.`);
        })
        .catch((err) => {
          console.error("Błąd aktualizacji częstotliwości:", err);
          alert(`Nie udało się zaktualizować częstotliwości:\n${err.message}`);
        });
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] },
    multiple: false,
    onDrop,
  });

    const generateExcel = async () => {
    if (!templateFile) return;
    if (!testResults) {
      alert("Brak wyników do wyeksportowania.");
      return;
    }
    setIsProcessing(true);

    try {
        const formData = new FormData();
        formData.append('file', templateFile);

        const response = await fetch('http://localhost:8000/drag-excel', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Błąd serwera: ${response.statusText}`);
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
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg border border-gray-200">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Eksport Wyników do Excela</h2>
      
      {/* Dropzone */}
      <div 
        {...getRootProps()} 
        className={`relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        <FileUp className="mx-auto h-12 w-12 text-gray-400 mb-3" />
        {templateFile ? (
          <div className="flex items-center justify-center text-green-600 font-medium">
            <CheckCircle2 className="mr-2 h-5 w-5" />
            <span>Załadowano: {templateFile.name}</span>
          </div>
        ) : (
          <p className="text-gray-500">Przeciągnij szablon .xlsx tutaj lub kliknij, aby wybrać</p>
        )}
      </div>

      {/* Przycisk Akcji */}
      <button
        onClick={generateExcel}
        disabled={!templateFile || isProcessing}
        className={`mt-6 w-full flex items-center justify-center py-3 px-4 rounded-lg font-semibold text-white transition
          ${!templateFile ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-md'}`}
      >
        {isProcessing ? (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
        ) : (
          <>
            <Download className="mr-2 h-5 w-5" />
            Generuj i pobierz raport
          </>
        )}
      </button>
    </div>
  );
};

export default ExcelExportTool;