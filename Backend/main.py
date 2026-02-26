from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import time
import json
import os
import io
import openpyxl
from testowy import run_antenna_test  # Import funkcji testowej z testowy.py
from test_state import TestState, RESULT_FILE

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


test_state = TestState()

# def run_antenna_test(state: TestState):
#     """Symulacja pracy anteny w tle z możliwością zatrzymania."""
#     print("Rozpoczynanie testu anteny (30s)...")
    
#     # Pętla symulująca pracę, sprawdzająca co sekundę sygnał zatrzymania
#     for _ in range(10):  # 10 sekund symulacji
#         if not state.is_active():
#             print("Test zatrzymany przez użytkownika.")
#             # Nie zapisujemy pliku, test przerwany
#             return
#         time.sleep(1)
    
#     # Przykładowe dane wynikowe
#     data = [
#         {
#     "angle": "0°",
#     "genPolarH_act": -10, "genPolarH_stop": 0, "genPolarV_act": 0, "genPolarV_stop": 0
#   },
#   {
#     "angle": "30°",
#     "genPolarH_act": 120, "genPolarH_stop": 60, "genPolarV_act": 90, "genPolarV_stop": 50
#   },
#   {
#     "angle": "60°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "90°",
#     "genPolarH_act": 100, "genPolarH_stop": 60, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "120°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "150°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "180°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "210°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "240°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "270°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "300°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   },
#   {
#     "angle": "330°",
#     "genPolarH_act": 100, "genPolarH_stop": 50, "genPolarV_act": 80, "genPolarV_stop": 40
#   }
#     ]
    
#     with open(RESULT_FILE, "w") as f:
#         json.dump(data, f)
    
#     state.stop() # Oznacz test jako zakończony
#     print("Test zakończony. Wyniki zapisane.")

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

@app.post("/drag-excel")
async def generate_excel(file: UploadFile = File(...)):
    # 1. Sprawdź czy są wyniki testu na serwerze
    if not os.path.exists(RESULT_FILE):
        raise HTTPException(status_code=404, detail="Brak wyników testu do wyeksportowania.")
    
    # 2. Wczytaj wyniki z pliku JSON
    with open(RESULT_FILE, "r") as f:
        test_results = json.load(f)

    try:
        # 3. Wczytaj przesłany szablon Excela do pamięci (bez zapisu na dysk)
        content = await file.read()
        workbook = openpyxl.load_workbook(io.BytesIO(content))
        sheet = workbook.worksheets[0] # Wybierz pierwszy arkusz
        
        # 4. Uzupełnij dane
        start_row = 22
        for index, row_data in enumerate(test_results):
            current_row = start_row + index
            # Mapowanie kolumn: E=5, F=6, G=7, H=8
            sheet.cell(row=current_row, column=5).value = row_data.get("genPolarH_act")
            sheet.cell(row=current_row, column=6).value = row_data.get("genPolarH_stop")
            sheet.cell(row=current_row, column=7).value = row_data.get("genPolarV_act")
            sheet.cell(row=current_row, column=8).value = row_data.get("genPolarV_stop")

        # 5. Zapisz zmodyfikowany plik do bufora pamięci
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)
        
        # 6. Zwróć plik jako strumień
        filename = f"Raport_Anteny_{int(time.time())}.xlsx"
        return StreamingResponse(
            output, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )

    except Exception as e:
        print(f"Błąd generowania Excela: {e}")
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {str(e)}")