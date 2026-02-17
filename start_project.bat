@echo off
:: Ustawienie katalogu skryptu jako katalogu roboczego
cd /d "%~dp0"

:: Sprawdzenie czy skrypt uruchomiony jest w trybie ukrytym
if "%1"=="hidden" goto :main_logic

:: --- Sekcja uruchamiania w trybie ukrytym (Bootstrap) ---
:: Tworzymy launcher VBS, ktory uruchomi ten skrypt ponownie, ale bez okna konsoli
echo Set WshShell = CreateObject("WScript.Shell") > run_invisible.vbs
echo WshShell.Run """%~f0"" hidden", 0, False >> run_invisible.vbs

:: Uruchomienie skryptu w tle i zamkniecie widocznego okna
start run_invisible.vbs
exit

:main_logic
:: --- Glowna logika (dziala w tle) ---

<<<<<<< HEAD
=======
:: 0. Czyszczenie starych procesow (na wypadek gdyby poprzednie nie zostaly zamkniete)
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1

>>>>>>> f66bc84c21a712048cbcc39241ab10ef6a651822
:: Helper VBS do uruchamiania komend w tle (dla serwerow)
echo Set WshShell = CreateObject("WScript.Shell") > run_cmd_hidden.vbs
echo WshShell.Run WScript.Arguments(0), 0, False >> run_cmd_hidden.vbs

<<<<<<< HEAD
:: 1. Uruchomienie Backendu
cscript //nologo run_cmd_hidden.vbs "cmd /c cd Backend && call venv\Scripts\activate && uvicorn main:app --reload"

:: 2. Uruchomienie Frontendu
cscript //nologo run_cmd_hidden.vbs "cmd /c cd Frontend && npm run dev"

:: Czekamy chwile na start serwerow
timeout /t 4 /nobreak >nul
=======
:: Wykrywanie srodowiska Python (venv lub globalny)
if exist "%~dp0Backend\venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0Backend\venv\Scripts\python.exe"
) else (
    if exist "%~dp0Backend\.venv\Scripts\python.exe" (
        set "PY_CMD=%~dp0Backend\.venv\Scripts\python.exe"
    ) else (
        set "PY_CMD=python"
    )
)

:: 1. Przygotowanie skryptu startowego dla Backendu (unika problemow z cudzyslowami)
(
echo @echo off
echo cd Backend
echo echo Uruchamianie przy uzyciu: "%PY_CMD%" ^> ..\backend.log
echo "%PY_CMD%" -u -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 ^>^> ..\backend.log 2^>^&1
) > start_backend_temp.bat

:: Uruchomienie Backendu w tle
cscript //nologo run_cmd_hidden.vbs "cmd /c start_backend_temp.bat"

:: 2. Uruchomienie Frontendu (z logowaniem do pliku frontend.log w katalogu glownym)
cscript //nologo run_cmd_hidden.vbs "cmd /c (cd Frontend && npm run dev) > ..\frontend.log 2>&1"

:: Czekamy dluzej na start serwerow (Vite i Uvicorn potrzebuja chwili)
timeout /t 10 /nobreak >nul
>>>>>>> f66bc84c21a712048cbcc39241ab10ef6a651822

:: 3. Uruchomienie przegladarki w trybie aplikacji i oczekiwanie na jej zamkniecie
:: Uzywamy --user-data-dir, aby wymusic nowa instancje (dzieki temu skrypt czeka na zamkniecie tego konkretnego okna)
start /wait msedge --app=http://localhost:5173 --user-data-dir="%TEMP%\AntenaTestProfile"

:: 4. Sprzatanie po zamknieciu przegladarki
taskkill /F /IM node.exe /T
taskkill /F /IM python.exe /T

:: Usuwanie plikow tymczasowych
del run_invisible.vbs
<<<<<<< HEAD
del run_cmd_hidden.vbs
=======
del run_cmd_hidden.vbs
del start_backend_temp.bat
>>>>>>> f66bc84c21a712048cbcc39241ab10ef6a651822
