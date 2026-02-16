import json
from typing import List, Dict, Optional

class ResultCollector:
    """
    A helper class to collect and structure test results during execution.

    This class is designed to build the specific JSON structure required for
    the sensitivity measurement report.
    """

    def __init__(self):
        """Initializes the collector with an empty data list."""
        self._data: List[Dict] = []
        self._angle_map: Dict[int, Dict] = {}

    def _get_or_create_angle_entry(self, angle: int) -> Dict:
        """
        Retrieves the dictionary for a given angle or creates a new one if it doesn't exist.
        
        Args:
            angle: The angle in degrees (e.g., 30, 60).
        
        Returns:
            The dictionary entry for that angle.
        """
        if angle in self._angle_map:
            return self._angle_map[angle]
        
        # Create a new entry with default values
        new_entry = {
            "angle": f"{angle}°",
            "genPolarH_act": 0,
            "genPolarH_stop": 0,
            "genPolarV_act": 0,
            "genPolarV_stop": 0
        }
        self._data.append(new_entry)
        self._angle_map[angle] = new_entry
        return new_entry

    def add_measurement(self, angle: int, polarization: str, activation_power: float, stop_power: float) -> None:
        """
        Adds a measurement result for a specific angle and polarization.

        Args:
            angle: The angle in degrees.
            polarization: The polarization, either 'H' for Horizontal or 'V' for Vertical.
            activation_power: The power level where the device activated.
            stop_power: The power level where the device stopped.
        """
        if polarization not in ['H', 'V']:
            raise ValueError("Polarization must be 'H' or 'V'.")

        entry = self._get_or_create_angle_entry(angle)
        
        # Update the specific keys based on polarization
        entry[f"genPolar{polarization}_act"] = activation_power
        entry[f"genPolar{polarization}_stop"] = stop_power

    def to_json(self, indent: int = 2) -> str:
        """
        Serializes the collected data into a JSON string.

        Args:
            indent: The indentation level for the JSON output.

        Returns:
            A JSON-formatted string of the collected results.
        """
        # Sort data by angle before serializing
        self._data.sort(key=lambda x: int(x['angle'][:-1]))
        return json.dumps(self._data, indent=indent)

    def get_data(self) -> List[Dict]:
        """Returns the raw list of collected data dictionaries."""
        self._data.sort(key=lambda x: int(x['angle'][:-1]))
        return self._data
