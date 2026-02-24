import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import ExcelJS from 'exceljs';
import { saveAs } from 'file-saver';
import { Download, FileUp, CheckCircle2 } from 'lucide-react'; // Opcjonalne ikony

const ExcelExportTool = ({ dataFromJson }) => {
  const [templateFile, setTemplateFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] },
    multiple: false,
    onDrop: (acceptedFiles) => setTemplateFile(acceptedFiles[0]),
  });

    const generateExcel = async () => {
    if (!templateFile) return;
    setIsProcessing(true);

    try {
        const workbook = new ExcelJS.Workbook();
        const arrayBuffer = await templateFile.arrayBuffer();
        await workbook.xlsx.load(arrayBuffer);
        
        const worksheet = workbook.getWorksheet(1);

        // Iterujemy po danych z JSONa
        dataFromJson.forEach((row, index) => {
        // Startujemy od wiersza 22, więc dodajemy index do 22
        const currentRow = 22 + index;

        // Mapowanie kluczy z JSON do kolumn E, F, G, H
        worksheet.getCell(`E${currentRow}`).value = row.genPolarH_act;
        worksheet.getCell(`F${currentRow}`).value = row.genPolarH_stop;
        worksheet.getCell(`G${currentRow}`).value = row.genPolarV_act;
        worksheet.getCell(`H${currentRow}`).value = row.genPolarV_stop;

        // Opcjonalnie: upewnij się, że formatowanie jest liczbą, by formuły (np. Average) działały
        const cells = [`E${currentRow}`, `F${currentRow}`, `G${currentRow}`, `H${currentRow}`];
        cells.forEach(ref => {
            worksheet.getCell(ref).numFmt = '0'; // Formatowanie jako liczba całkowita
        });
        });

        // Automatyczne przeliczenie formuł (jak Average of Rx sensitivity w wierszu 34)
        // Uwaga: ExcelJS nie przelicza formuł sam, zrobi to Excel po otwarciu pliku.

        const buffer = await workbook.xlsx.writeBuffer();
        saveAs(new Blob([buffer]), `Raport_Anteny_${Date.now()}.xlsx`);
        
    } catch (error) {
        console.error("Błąd eksportu:", error);
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