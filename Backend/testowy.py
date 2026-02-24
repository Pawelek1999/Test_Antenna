from test_state import TestState, RESULT_FILE
import time
import json


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
    
    with open(RESULT_FILE, "w") as f:
        json.dump(data, f)
    
    state.stop() # Oznacz test jako zakończony
    print("Test zakończony. Wyniki zapisane.")