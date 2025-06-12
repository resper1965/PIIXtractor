# Extractor Project

This project organizes the extraction workflow. Use the script inside this
folder to process archives:

```bash
cd extractor_project
python extractor_drive.py path/to/your.zip
```

The contents are extracted into `tmp/`. After processing, the results are saved
as CSV, JSON and SQLite files inside the `data/` directory.
