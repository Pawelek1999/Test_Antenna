from test_state import TestState, RESULT_FILE
import time
import json
from drivers.test_calculation.sensitivity_value import calculate_sensitivity


def run_antenna_test(state: TestState):
    """Symulacja pracy anteny w tle z możliwością zatrzymania."""
    print("Rozpoczynanie testu anteny (30s)...")
    
    # Pętla symulująca pracę, sprawdzająca co sekundę sygnał zatrzymania
    for _ in range(10):  # 10 sekund symulacji
        if not state.is_active():
            print("Test zatrzymany przez użytkownika.")
            # Nie zapisujemy pliku, test przerwany
            return
        time.sleep(1)
    
    # Przykładowe dane wynikowe
    data = [
        {
    "angle": "0°",
    "genPolarH_act": -10, "genPolarH_stop": 0, "genPolarV_act": 0, "genPolarV_stop": 0
  },
  {
    "angle": "30°",
    "genPolarH_act": 120, "genPolarH_stop": 60, "genPolarV_act": 90, "genPolarV_stop": 50
  },
  {
    "angle": "60°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "90°",
    "genPolarH_act": 100, "genPolarH_stop": 60, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "120°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "150°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "180°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "210°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "240°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "270°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "300°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  },
  {
    "angle": "330°",
    "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
  }
    ]
    
    # Parametry do obliczeń (Wartości przykładowe, powinny być zgodne z ustawieniami testu)
    calc_freq = 409.9875       # MHz
    calc_distance = 3.0     # m
    calc_wire_loss = 4.79    # dB
    calc_ant_factor = 17.8   # dB/m

    # Obliczanie sensitivity i dodawanie do wyników
    for row in data:
        # Dla polaryzacji H (Activation)
        h_db, h_uv = calculate_sensitivity(row.get("genPolarH_act"), calc_freq, calc_distance, calc_wire_loss, calc_ant_factor)
        row["sens_genPolarH_act_db"] = h_db
        row["sens_genPolarH_act_uv"] = h_uv

        # Dla polaryzacji V (Activation)
        v_db, v_uv = calculate_sensitivity(row.get("genPolarV_act"), calc_freq, calc_distance, calc_wire_loss, calc_ant_factor)
        row["sens_genPolarV_act_db"] = v_db
        row["sens_genPolarV_act_uv"] = v_uv

    with open(RESULT_FILE, "w") as f:
        json.dump(data, f)
    
    state.stop() # Oznacz test jako zakończony
    print("Test zakończony. Wyniki zapisane.")