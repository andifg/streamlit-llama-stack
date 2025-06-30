"""CLI entry point for streamlit-llamastack"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit app"""
    app_path = Path(__file__).parent / "app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)] + sys.argv[1:])


if __name__ == "__main__":
    main() 