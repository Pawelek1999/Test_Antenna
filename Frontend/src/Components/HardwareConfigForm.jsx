import React, { useState } from 'react';
import { Save, Cpu, RotateCcw } from 'lucide-react';
import { useConfig } from '../Components/ConfigContext';

const HardwareConfigForm = ({ onSaveSuccess }) => {
  const { hardwareConfig, setHardwareConfig } = useConfig();

  const [isSaving, setIsSaving] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setHardwareConfig(prev => ({
      ...prev,
      // analog_channel parsujemy jako int, resztę jako float
      [name]: name === 'analog_channel' ? parseInt(value, 10) : parseFloat(value)
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/save-hardware-config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(hardwareConfig),
      });

      if (!response.ok) {
        throw new Error('Błąd zapisu');
      }

      const data = await response.json();
      alert(data.message);
      if (onSaveSuccess) {
        onSaveSuccess();
      }
    } catch (error) {
      console.error("Błąd:", error);
      alert("Nie udało się zapisać konfiguracji sprzętowej.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    setHardwareConfig({
      analog_channel: 3,
      voltage_threshold_v: 4.5,
      safe_stop_power_dbm: -20.0
    });
  };

  return (
    <div className="max-w-xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center mb-4 text-gray-800">
          <Cpu className="w-5 h-5 mr-2" />
          <h2 className="text-lg font-bold">Konfiguracja Sprzętowa</h2>
        </div>

        <div className="space-y-4">
          {/* Analog Channel */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Analog Channel</label>
            <input
              type="number"
              name="analog_channel"
              value={hardwareConfig.analog_channel}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Voltage Threshold */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Voltage Threshold (V)</label>
            <input
              type="number"
              name="voltage_threshold_v"
              value={hardwareConfig.voltage_threshold_v}
              onChange={handleChange}
              step="0.1"
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Safe Stop Power */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Safe Stop Power (dBm)</label>
            <input
              type="number"
              name="safe_stop_power_dbm"
              value={hardwareConfig.safe_stop_power_dbm}
              onChange={handleChange}
              step="0.1"
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
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
          className="flex-1 flex items-center justify-center py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition shadow-md disabled:bg-gray-400"
        >
          <Save className="w-4 h-4 mr-2" />
          {isSaving ? 'Zapisywanie...' : 'Zapisz i kontynuuj'}
        </button>
      </div>
    </div>
  );
};

export default HardwareConfigForm;