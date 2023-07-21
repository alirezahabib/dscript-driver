@echo off

cd %~dp0

SET SCRIPT_PATH=%~dp0\dscript_gui.py

REM Check if the venv directory exists
f not exist "venv\Scripts\activate" (
    echo Creating venv...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating venv
        exit /b 1
    )
)

call venv\Scripts\activate

pip show streamlit >nul 2>&1 || (
    echo.
    echo Info: streamlit not found, installing now
    echo.
    pip install streamlit
)

echo.
echo Info: Running dscript_gui.py with streamlit
echo.

streamlit run dscript_gui.py

call deactivate
