from test_state import TestState
import time
import json
from drivers.test_calculation.sensitivity_value import calculate_sensitivity
from pathlib import Path


def run_antenna_test(state: TestState, result_file_path: Path):
    """Symulacja pracy anteny w tle dla wszystkich konfiguracji z we_config.json."""
    we_config_path = result_file_path.parent / "we_config.json"
    
    if not we_config_path.exists():
        print(f"Błąd: Nie znaleziono pliku konfiguracji {we_config_path}")
        state.stop()
        return

    try:
        with open(we_config_path, "r", encoding="utf-8") as f:
            we_config = json.load(f)
    except Exception as e:
        print(f"Błąd odczytu we_config.json: {e}")
        state.stop()
        return

    print(f"Rozpoczynanie sekwencji testów ({len(we_config)} konfiguracji)...")

    for config_item in we_config:
        if not state.is_active():
            print("Test zatrzymany przez użytkownika.")
            return

        sheet_id = config_item.get("sheet")
        obj_id = config_item.get("id")
        params = config_item.get("test_params", {})

        print(f"Testowanie: Sheet {sheet_id}, ID {obj_id}...")

        # Symulacja czasu trwania pomiaru dla jednego arkusza (np. 5s)
        for _ in range(5):
            if not state.is_active():
                return
            time.sleep(1)

        # Przykładowe dane wynikowe (szkielet)
        data = [
            {"angle": "0°", "genPolarH_act": -10, "genPolarH_stop": 0, "genPolarV_act": 0, "genPolarV_stop": 0},
            {"angle": "30°", "genPolarH_act": 120, "genPolarH_stop": 60, "genPolarV_act": 90, "genPolarV_stop": 50},
            {"angle": "60°", "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40},
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
    
        # Parametry do obliczeń pobrane z konfiguracji
        calc_freq = params.get("frequency_hz", 409987500) / 1000000.0  # Hz -> MHz
        calc_distance = params.get("distance", 3.0)
        calc_wire_loss = params.get("wire_loss_db", 4.79)
        calc_ant_factor = params.get("antenna_factor_dbm_1", 17.8)

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

        # Zapis do pliku result.json dla bieżącej konfiguracji
        try:
            all_sheets_data = []
            # Sprawdź czy plik istnieje, jeśli tak - wczytaj
            if result_file_path.exists():
                with open(result_file_path, "r", encoding="utf-8") as f:
                    try:
                        all_sheets_data = json.load(f)
                    except json.JSONDecodeError:
                        all_sheets_data = []

            # Jeśli plik nie istniał lub był pusty, zainicjalizuj strukturę z we_config
            if not all_sheets_data:
                for cfg in we_config:
                    f_hz = cfg.get("test_params", {}).get("frequency_hz", 0)
                    all_sheets_data.append({
                        "sheet": cfg.get("sheet"),
                        "id": cfg.get("id"),
                        "antenna": cfg.get("antenna", ""),
                        "frequency_mhz": f_hz / 1000000.0,
                        "result": []
                    })

            updated = False
            for sheet in all_sheets_data:
                if sheet.get("sheet") == sheet_id and sheet.get("id") == obj_id:
                    sheet["result"] = data
                    # Aktualizacja pól informacyjnych
                    sheet["antenna"] = config_item.get("antenna", "")
                    sheet["frequency_mhz"] = params.get("frequency_hz", 0) / 1000000.0
                    updated = True
                    break
            
            # Zapisz całość (tryb 'w' utworzy plik jeśli nie istnieje)
            with open(result_file_path, "w", encoding="utf-8") as f:
                json.dump(all_sheets_data, f, indent=2, ensure_ascii=False)
                print(f"Zapisano wyniki dla Sheet {sheet_id}, ID {obj_id}")

        except Exception as e:
            print(f"Krytyczny błąd zapisu: {e}")
            state.stop()
            return

    state.stop() # Oznacz test jako zakończony
    print("Wszystkie testy zakończone.")