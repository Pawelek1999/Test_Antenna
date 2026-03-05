import React, { createContext, useState, useContext, useEffect } from 'react';

const ConfigContext = createContext();

export const useConfig = () => useContext(ConfigContext);

export const ConfigProvider = ({ children }) => {
  const [hardwareConfig, setHardwareConfig] = useState({
    analog_channel: 3,
    voltage_threshold_v: 4.5,
    safe_stop_power_dbm: -20.0
  });

  const [runtimeParams, setRuntimeParams] = useState({
    start_power_dbm: -50.0,
    end_power_dbm: 10.0,
    power_step_db: 1.0,
    start_table_position: 0,
    start_malt_height: 150,
    silent_search_reduction_db: 5.0
  });

  const [testConfig, setTestConfig] = useState([]);

  const [frequenciesData, setFrequenciesData] = useState([]);

  const fetchFrequencies = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/frequencies");
        if (response.ok) {
            const data = await response.json();
            setFrequenciesData(data);
        } else {
            console.error("Błąd pobierania częstotliwości:", response.statusText);
            setFrequenciesData([]); // Ustaw pustą tablicę w razie błędu
        }
    } catch (error) {
        console.error("Błąd sieci podczas pobierania częstotliwości:", error);
        setFrequenciesData([]); // Ustaw pustą tablicę w razie błędu
    }
  };

  const refreshConfig = async () => {
    try {
      const [hwRes, rtRes, tcRes] = await Promise.all([
        fetch('http://127.0.0.1:8000/get-hardware-config'),
        fetch('http://127.0.0.1:8000/get-runtime-params'),
        fetch('http://127.0.0.1:8000/get-test-config')
      ]);

      if (hwRes.ok) {
        const data = await hwRes.json();
        if (data && Object.keys(data).length > 0) setHardwareConfig(data);
      }
      if (rtRes.ok) {
        const data = await rtRes.json();
        if (data && Object.keys(data).length > 0) setRuntimeParams(data);
      }
      if (tcRes.ok) {
        const data = await tcRes.json();
        if (Array.isArray(data) && data.length > 0) setTestConfig(data);
      }
    } catch (error) {
      console.error("Błąd odświeżania konfiguracji:", error);
    }
  };

  useEffect(() => {
    refreshConfig();
    fetchFrequencies();
  }, []);

  return (
    <ConfigContext.Provider value={{
      hardwareConfig, setHardwareConfig,
      runtimeParams, setRuntimeParams,
      testConfig, setTestConfig,
      frequenciesData,
      fetchFrequencies,
      refreshConfig
    }}>
      {children}
    </ConfigContext.Provider>
  );
};
