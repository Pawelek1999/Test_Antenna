function TestControl({ handleStartTest, handleStopTest, isTesting }) {

    return (
        /* Sekcja Sterowania Anteną */
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md border border-slate-200">
          <h2 className="text-xl font-bold text-slate-800 mb-4">Panel Diagnostyczny Anteny</h2>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={handleStartTest}
              disabled={isTesting}
              className={`px-6 py-3 rounded-md font-semibold text-white transition-colors w-64 text-center ${
                isTesting 
                  ? "bg-slate-400 cursor-not-allowed" 
                  : "bg-blue-600 hover:bg-blue-700 shadow-lg"
              }`}
            >
              {isTesting ? "Test w toku..." : "Uruchom Test Anteny"}
            </button>

            <button
              onClick={handleStopTest}
              disabled={!isTesting}
              className={`px-6 py-3 rounded-md font-semibold text-white transition-colors w-64 text-center ${
                !isTesting 
                  ? "bg-slate-400 cursor-not-allowed" 
                  : "bg-red-600 hover:bg-red-700 shadow-lg"
              }`}
            >
              Zatrzymaj Test
            </button>
          </div>
        </div>
    );
}

export default TestControl;