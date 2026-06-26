"""
run.py — Project launcher. Run this file to start the app.
Usage: python run.py
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", app_path, "--server.port=8501"],
        check=True,
    )
