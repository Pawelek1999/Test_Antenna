function AntenaChoice({ antennasData, selectedAntena, onAntenaSelect }) {
  

    const handleAntenaSelect = (antena) => {
          const id = parseInt(antena.target.value);
          const znaleziona = antennasData.find (a => a.id === id);
          onAntenaSelect(znaleziona);
      };

    return (
        <div>
            <h2 className="text-xl font-bold mb-4">Wybierz Antenę:</h2>
            
            {/* Rozwijane menu (Select) */}
            <select 
                className="border border-gray-300 rounded-md p-2 w-full mb-4"
                onChange={handleAntenaSelect}
            >
                <option value="">Wybierz Antenę</option>
                {antennasData.map((antena) => (
                    <option key={antena.id} value={antena.id}>
                        {antena.nazwa}
                    </option>
                ))}
            </select>

            {/* Wyświetlanie wybranej anteny */}
            {selectedAntena ? (
                <div className="border border-gray-300 rounded-md p-4">
                    <h3 className="text-lg font-semibold mb-2">{selectedAntena.nazwa}</h3>
                    <ul className="list-disc list-inside">
                        <li>Down limit: {selectedAntena.parametry.down_limit} dBuV/m</li>
                        <li>Upper limit: {selectedAntena.parametry.upper_limit}uV/m</li>
                        <li>Generetor: {selectedAntena.parametry.generator} dBm</li>
                    </ul>
                </div>
            ) : (<p>Nie wybrano anteny.</p>)}
        </div>);
}

export default AntenaChoice;