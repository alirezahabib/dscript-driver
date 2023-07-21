@echo off

cd %~dp0

@REM SET SCRIPT_PATH=%~dp0\dscript_gui.py

@REM REM Check if the venv directory exists
@REM f not exist "venv\Scripts\activate" (
@REM     echo Creating venv...
@REM     python -m venv venv
@REM     if errorlevel 1 (
@REM         echo Error creating venv
@REM         exit /b 1
@REM     )
@REM )

REM call venv\Scripts\activate

echo.
echo Info: Run `pip install -r requirements.txt` to install dependencies
echo.
echo Info: Running dscript_gui.py with streamlit
echo.

streamlit run dscript_gui.py

@REM call deactivate
