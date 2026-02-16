function FrequencyChoice({ frequenciesData, selectedFrequency, onFrequencySelect }) {

    const handleFrequencySelect = (frequency) => {
        const id = parseInt(frequency.target.value);
        const found = frequenciesData.find (f => f.id === id);
        onFrequencySelect(found);
    };

    return (
        <div>
            <h2 className="text-xl font-bold mb-4">Wybierz Częstotliwość:</h2>
            <select 
                className="border border-gray-300 rounded-md p-2 w-full mb-4"
                onChange={handleFrequencySelect}
            >

                {/* Rozwijane menu (Select) */}
                <option value="">Wybierz Częstotliwość</option>
                {frequenciesData.map((frequency) => (
                    <option key={frequency.id} value={frequency.id}>
                        MHz: {frequency.frequency_mhz} Country: {frequency.country}
                    </option>
                ))}
            </select>

            {/* Wyświetlanie wybranej częstotliwości */}
            {selectedFrequency ? (
                <div className="border border-gray-300 rounded-md p-4">
                    <h3 className="text-lg font-semibold mb-2">{selectedFrequency.country}</h3>
                    <ul className="list-disc list-inside">
                        <li>Protocol: {selectedFrequency.protocol}</li>
                        <li>Frequency MHz: {selectedFrequency.frequency_mhz}</li>
                        <li>Wire Lose dB: {selectedFrequency.wire_loss_db}</li>
                        <li>Antenna Factor dBm-1: {selectedFrequency.antenna_factor_dbm_1}</li>
                    
                    </ul>
                </div>
            ) : (<p>Nie wybrano częstotliwości.</p>)}
        </div>);
}

export default FrequencyChoice;