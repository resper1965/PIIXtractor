# PIIXtractor
PIIXtractor

## Running with Docker Compose

Build and start the services using:

```bash
docker-compose up --build
```

This starts two containers:

- **extractor**: Flask application listening on port `8000`. The directory `./extractor` is mounted into the container at `/app`.
- **web**: Flask application listening on port `5000` and depends on the extractor service. The directory `./web` is mounted into the container at `/app`.

The services will be available at `http://localhost:8000` for the extractor and `http://localhost:5000` for the web interface.
