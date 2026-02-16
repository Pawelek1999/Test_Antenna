import React from 'react';

const PdfButton = () => {
    const handlePrint = () => {
        window.print();
    };

    return (
        <button 
            onClick={handlePrint} 
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4 shadow transition-colors print:hidden"
        >
            Drukuj / Zapisz jako PDF
        </button>
    );
};

export default PdfButton;