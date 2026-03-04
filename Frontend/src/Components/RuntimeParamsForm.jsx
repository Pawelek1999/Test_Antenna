import React, { useState } from 'react';
import { Save, Settings, RotateCcw } from 'lucide-react';

const DEFAULT_PARAMS = {
  start_power_dbm: -50.0,
  end_power_dbm: 10.0,
  power_step_db: 1.0,
  start_table_position: 0,
  start_malt_height: 150,
  silent_search_reduction_db: 5.0
};

const RuntimeParamsForm = () => {
  // Domyślne wartości zgodne z wymaganiami
  const [params, setParams] = useState(DEFAULT_PARAMS);

  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParams(prev => ({
      ...prev,
      [name]: parseFloat(value) // Konwersja na liczbę
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/save-runtime-params', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });

      if (!response.ok) {
        throw new Error('Błąd zapisu');
      }

      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Błąd:", error);
      alert("Nie udało się zapisać parametrów.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    setParams(DEFAULT_PARAMS);
  };

  return (
    <div className="max-w-xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center mb-4 text-gray-800">
        <Settings className="w-5 h-5 mr-2" />
        <h2 className="text-lg font-bold">Parametry Testu (Runtime)</h2>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Start Power */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Power (dBm)</label>
          <input
            type="number"
            name="start_power_dbm"
            value={params.start_power_dbm}
            onChange={handleChange}
            step="0.1"
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* End Power */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">End Power (dBm)</label>
          <input
            type="number"
            name="end_power_dbm"
            value={params.end_power_dbm}
            onChange={handleChange}
            step="0.1"
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Power Step */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Power Step (dB)</label>
          <input
            type="number"
            name="power_step_db"
            value={params.power_step_db}
            onChange={handleChange}
            step="0.1"
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Silent Search Reduction */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Silent Search Red. (dB)</label>
          <input
            type="number"
            name="silent_search_reduction_db"
            value={params.silent_search_reduction_db}
            onChange={handleChange}
            step="0.1"
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Start Table Position */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Table Pos</label>
          <input
            type="number"
            name="start_table_position"
            value={params.start_table_position}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Start Malt Height */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Malt Height</label>
          <input
            type="number"
            name="start_malt_height"
            value={params.start_malt_height}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      <div className="mt-6 flex gap-3">
        <button
          onClick={handleReset}
          className="flex items-center justify-center py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-lg transition shadow-sm"
          title="Przywróć domyślne"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="flex-1 flex items-center justify-center py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition shadow-md disabled:bg-gray-400"
        >
          <Save className="w-4 h-4 mr-2" />
          {isSaving ? 'Zapisywanie...' : 'Zapisz Parametry'}
        </button>
      </div>
    </div>
  );
};

export default RuntimeParamsForm;
