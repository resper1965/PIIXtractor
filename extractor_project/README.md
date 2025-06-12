# Extractor Project

This project organizes the extraction workflow.

## Requirements

- Python 3.10+

Create and activate a virtual environment and install dependencies from the
repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

Then use the script inside this folder to process archives:

```bash
cd extractor_project
python extractor_drive.py path/to/your.zip
```

The contents are extracted into `tmp/`. After processing, the results are saved
as CSV, JSON and SQLite files inside the `data/` directory.
