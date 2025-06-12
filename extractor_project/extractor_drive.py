from pathlib import Path
import os
import sys

# Ensure the root project directory is on the path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from extractor_drive import main

if __name__ == "__main__":
    zip_file = sys.argv[1] if len(sys.argv) > 1 else os.getenv("ZIP_INPUT", "columbiati.zip")
    main(zip_file)
