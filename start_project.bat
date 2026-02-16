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

:: Helper VBS do uruchamiania komend w tle (dla serwerow)
echo Set WshShell = CreateObject("WScript.Shell") > run_cmd_hidden.vbs
echo WshShell.Run WScript.Arguments(0), 0, False >> run_cmd_hidden.vbs

:: 1. Uruchomienie Backendu
cscript //nologo run_cmd_hidden.vbs "cmd /c cd Backend && call venv\Scripts\activate && uvicorn main:app --reload"

:: 2. Uruchomienie Frontendu
cscript //nologo run_cmd_hidden.vbs "cmd /c cd Frontend && npm run dev"

:: Czekamy chwile na start serwerow
timeout /t 4 /nobreak >nul

:: 3. Uruchomienie przegladarki w trybie aplikacji i oczekiwanie na jej zamkniecie
:: Uzywamy --user-data-dir, aby wymusic nowa instancje (dzieki temu skrypt czeka na zamkniecie tego konkretnego okna)
start /wait msedge --app=http://localhost:5173 --user-data-dir="%TEMP%\AntenaTestProfile"

:: 4. Sprzatanie po zamknieciu przegladarki
taskkill /F /IM node.exe /T
taskkill /F /IM python.exe /T

:: Usuwanie plikow tymczasowych
del run_invisible.vbs
del run_cmd_hidden.vbs