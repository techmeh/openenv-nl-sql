# Stage 1: builder
ARG BASE_IMAGE=ghcr.io/meta-pytorch/openenv-base:latest
FROM ${BASE_IMAGE} AS builder
# Dockerfile
ENV ENABLE_WEB_INTERFACE=true
WORKDIR /app

# Copy requirements first so Docker can cache pip install
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /app/env/.venv \
 && . /app/env/.venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the rest of your source code (server/, openenv/, etc.)
COPY . .

# Stage 2: runtime
FROM ${BASE_IMAGE}

WORKDIR /app

# Copy the virtual environment and env folder from builder
COPY --from=builder /app/env/.venv /app/.venv
COPY --from=builder /app/env /app/env
COPY --from=builder /app/server /app/server
COPY --from=builder /app/database /app/database
COPY --from=builder /app/openenv.yaml /app/openenv.yaml
COPY --from=builder /app/models.py /app/models.py

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Healthcheck for Hugging Face Spaces
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start FastAPI with uvicorn
ENTRYPOINT ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]