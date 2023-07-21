import os
import subprocess
import sys


def run_streamlit_app(app_filename):
    # Check if the venv folder exists
    if not os.path.exists("venv"):
        print("Virtual environment not found. Please run 'python -m venv venv' first to create the venv.")
        sys.exit(1)

    activate_script = os.path.join("venv", "Scripts", "activate.bat")
    subprocess.run(activate_script, shell=True)

    subprocess.run("pip install streamlit", shell=True)

    subprocess.run(f"streamlit run {app_filename}", shell=True)

    deactivate_script = os.path.join("venv", "Scripts", "deactivate.bat")
    subprocess.run(deactivate_script, shell=True)


if __name__ == "__main__":
    run_streamlit_app('dscript_gui.py')
