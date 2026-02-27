from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import time
import json
import os
import io
from pathlib import Path
import openpyxl
from testowy import run_antenna_test  # Import funkcji testowej z testowy.py
from test_state import TestState, RESULT_FILE
from paths import CONFIG


app = FastAPI()

# --- Konfiguracja CORS ---
# Pozwala frontendowi (React) na komunikację z backendem
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORT_TEMPLATE_PATH = CONFIG / "report_template.xlsx"
# Ścieżka do pliku konfiguracyjnego z częstotliwościami, używanego przez frontend
BACKEND_DIR = Path(__file__).resolve().parent
FREQUENCY_JSON_PATH = BACKEND_DIR.parent / "Frontend" / "public" / "frequency.json"
test_state = TestState()

@app.post("/start-test")
async def start_test(background_tasks: BackgroundTasks):
    if test_state.is_active():
        return JSONResponse(status_code=409, content={"message": "Test jest już w toku."})

    # Usuń stary plik wyników, jeśli istnieje
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)
    
    test_state.start()
    background_tasks.add_task(run_antenna_test, test_state)
    return {"message": "Test uruchomiony w tle"}

@app.post("/stop-test")
async def stop_test():
    """Zatrzymuje aktualnie działający test."""
    if not test_state.is_active():
        return {"message": "Żaden test nie jest aktualnie uruchomiony."}
    
    test_state.stop()
    return {"message": "Wysłano sygnał zatrzymania testu."}

@app.get("/check-status")
async def check_status():
    return {"is_running": test_state.is_active(), "results_ready": os.path.exists(RESULT_FILE)}

@app.get("/download-data")
async def download_data():
    if not os.path.exists(RESULT_FILE):
        return JSONResponse(status_code=404, content={"message": "Brak wyników"})
    
    with open(RESULT_FILE, "r") as f:
        data = json.load(f)
    return data


def _fill_workbook_with_results(workbook: openpyxl.Workbook, test_results: list):
    """Helper function to populate an Excel workbook with test results."""
    sheet = workbook.worksheets[0]  # Select the first sheet

    # --- Populate data ---
    start_row = 22
    for index, row_data in enumerate(test_results):
        current_row = start_row + index
        # Column mapping: E=5, F=6, G=7, H=8
        sheet.cell(row=current_row, column=5).value = row_data.get("genPolarH_act")
        sheet.cell(row=current_row, column=6).value = row_data.get("genPolarH_stop")
        sheet.cell(row=current_row, column=7).value = row_data.get("genPolarV_act")
        sheet.cell(row=current_row, column=8).value = row_data.get("genPolarV_stop")


def _generate_excel_response(workbook: openpyxl.Workbook) -> StreamingResponse:
    """Saves a workbook to a memory buffer and returns it as a StreamingResponse."""
    output = io.BytesIO()
    workbook.save(output)
    # --- Weryfikacja ---
    # Sprawdzamy i drukujemy w konsoli backendu rozmiar bufora po zapisie.
    print(f"Plik Excel wygenerowany w pamięci. Rozmiar bufora: {output.tell()} bajtów.")
    output.seek(0)

    filename = f"Raport_Anteny_{int(time.time())}.xlsx"
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@app.post("/drag-excel")
async def upload_and_generate_excel(file: UploadFile = File(...)):
    """
    Generates an Excel report by populating a user-uploaded template.
    """
    if not os.path.exists(RESULT_FILE):
        raise HTTPException(status_code=404, detail="Brak wyników testu do wyeksportowania.")

    with open(RESULT_FILE, "r") as f:
        test_results = json.load(f)

    try:
        content = await file.read()
        workbook = openpyxl.load_workbook(io.BytesIO(content))

        _fill_workbook_with_results(workbook, test_results)

        return _generate_excel_response(workbook)

    except Exception as e:
        print(f"Błąd generowania Excela z szablonu: {e}")
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {str(e)}")


@app.get("/download-report")
async def download_excel_report():
    """
    Generates and returns an Excel report using a server-side template.
    """
    if not os.path.exists(RESULT_FILE):
        raise HTTPException(status_code=404, detail="Brak wyników testu do wyeksportowania.")

    if not os.path.exists(REPORT_TEMPLATE_PATH):
        raise HTTPException(status_code=500, detail=f"Brak pliku szablonu na serwerze: {REPORT_TEMPLATE_PATH}")

    with open(RESULT_FILE, "r") as f:
        test_results = json.load(f)

    try:
        workbook = openpyxl.load_workbook(REPORT_TEMPLATE_PATH)
        _fill_workbook_with_results(workbook, test_results)
        return _generate_excel_response(workbook)

    except Exception as e:
        print(f"Błąd generowania raportu Excel: {e}")
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {str(e)}")


@app.post("/update-frequencies-from-excel")
async def update_frequencies_from_excel(file: UploadFile = File(...)):
    """
    Parsuje plik Excel w celu aktualizacji konfiguracji częstotliwości.
    Odczytuje dane z wierszy 2-8 i kolumn T-Y, a następnie nadpisuje
    plik 'Frontend/public/frequency.json'.
    """
    try:
        content = await file.read()
        workbook = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
        sheet = workbook.active

        frequencies_data = []
        
        # Mapowanie: Indeks kolumny Excela -> (klucz JSON, funkcja konwertująca typ)
        COLUMN_MAPPING = {
            20: ("id", int),                     # Kolumna T
            21: ("protocol", str),               # Kolumna U
            22: ("country", str),                # Kolumna V
            23: ("frequency_mhz", float),        # Kolumna W
            24: ("wire_loss_db", float),         # Kolumna X
            25: ("antenna_factor_dbm_1", float), # Kolumna Y
        }

        # Iteracja po wierszach od 2 do 8
        for row_index in range(2, 9):
            # Pomiń wiersz, jeśli komórka ID (kolumna T) jest pusta
            id_cell_value = sheet.cell(row=row_index, column=20).value
            if id_cell_value is None or str(id_cell_value).strip() == "":
                continue

            item = {}
            for col_index, (key, type_converter) in COLUMN_MAPPING.items():
                cell = sheet.cell(row=row_index, column=col_index)
                cell_value = cell.value

                if cell_value is None and key != 'id':
                    item[key] = None
                    continue

                try:
                    item[key] = type_converter(cell_value)
                except (ValueError, TypeError):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Nieprawidłowa wartość '{cell_value}' w komórce {cell.coordinate}. Oczekiwano typu: {type_converter.__name__}."
                    )
            
            frequencies_data.append(item)

        # Zapisz nowe dane do pliku JSON
        with open(FREQUENCY_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(frequencies_data, f, indent=2, ensure_ascii=False)

        return {"message": f"Plik frequency.json został pomyślnie zaktualizowany. Wczytano {len(frequencies_data)} wpisów."}

    except HTTPException as e:
        raise e # Przekaż dalej wyjątki HTTP z logiką walidacji
    except Exception as e:
        print(f"Błąd przetwarzania pliku Excel z konfiguracją częstotliwości: {e}")
        raise HTTPException(status_code=500, detail=f"Wystąpił błąd serwera podczas przetwarzania pliku: {str(e)}")