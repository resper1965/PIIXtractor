# Extractor Project


This folder holds auxiliary data for the extractor. The pipeline is executed from the project root using a single entry point:
=======
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
python extractor_drive.py
```

Results are stored in the `data/` directory and temporary files are created in `tmp/`.
