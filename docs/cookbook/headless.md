# Headless & Docker

## Headless mode

By default, cdpwave launches Chrome in headless mode:

```python
client = await CDPClient.launch(headless=True)  # default
```

For debugging, launch with a visible window:

```python
client = await CDPClient.launch(headless=False)
```

## CI environments

cdpwave automatically adds `--no-sandbox` when it detects CI environments (`CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, `JENKINS_URL`).

## Docker

In Docker containers, Chrome needs `--no-sandbox`. If your container doesn't set `CI` env vars, pass it manually:

```python
client = await CDPClient.launch(
    extra_args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
)
```

### Dockerfile example

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    chromium \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV CDPWAVE_BROWSER_PATH=/usr/bin/chromium

COPY . /app
WORKDIR /app
RUN pip install -e .

CMD ["python", "script.py"]
```

### Docker Compose

```yaml
services:
  app:
    build: .
    environment:
      - CI=true
    volumes:
      - ./output:/app/output
```

## Common Docker flags

| Flag | Why |
|---|---|
| `--no-sandbox` | Required in containers without seccomp |
| `--disable-gpu` | No GPU in most containers |
| `--disable-dev-shm-usage` | Avoid `/dev/shm` size issues |
| `--single-process` | Reduce memory in constrained containers |
