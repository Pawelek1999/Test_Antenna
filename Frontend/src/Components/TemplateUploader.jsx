import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FileUp, CheckCircle2 } from 'lucide-react';

const TemplateUploader = ({ onUploadSuccess }) => {
  const [templateFile, setTemplateFile] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    setTemplateFile(file);

    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      // Wysyłamy szablon do backendu
      fetch('http://127.0.0.1:8000/upload-template', {
        method: 'POST',
        body: formData,
      })
        .then(async (res) => {
          const data = await res.json();
          if (!res.ok) throw new Error(data.detail || 'Wystąpił błąd podczas przetwarzania pliku.');
          return data;
        })
        .then((data) => {
          alert(data.message);
          if (onUploadSuccess) {
            onUploadSuccess(); // Odśwież listę częstotliwości
          }
        })
        .catch((err) => {
          console.error("Błąd aktualizacji częstotliwości:", err);
          alert(`Nie udało się zaktualizować częstotliwości:\n${err.message}`);
        });
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] },
    multiple: false,
    onDrop,
  });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 h-full flex flex-col">
      <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center"><FileUp className="w-4 h-4 mr-2"/> Wgraj Szablon Excel</h3>
      <div 
        {...getRootProps()} 
        className={`flex-grow flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-all min-h-[100px]
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        {templateFile ? (
          <div className="flex flex-col items-center text-green-600 font-medium">
            <CheckCircle2 className="h-8 w-8 mb-2" />
            <span className="text-xs break-all">{templateFile.name}</span>
          </div>
        ) : (
          <>
            <FileUp className="h-8 w-8 text-gray-400 mb-2" />
            <p className="text-xs text-gray-500">Przeciągnij szablon .xlsx</p>
          </>
        )}
      </div>
    </div>
  );
};

export default TemplateUploader;
