# Use NVIDIA PyTorch image (CUDA/cuDNN preinstalled)
ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:25.05-py3
FROM ${BASE_IMAGE}

# System prep
ENV DEBIAN_FRONTEND=noninteractive

# Create an app dir
WORKDIR /app

# Copy only requirements first for better Docker layer caching
COPY requirements.txt /app/requirements.txt


RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Python deps
# Tip: prefer faiss-cpu in requirements.txt to avoid CUDA wheel compatibility issues.
RUN pip install --upgrade --no-cache-dir pip setuptools wheel && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip cache purge

# Now copy the rest of the project
# (includes: app.py / inference.py / vllm_backed_model.py / sample_text.py, etc.)
COPY . /app

# Caches & runtime env
ENV HF_HOME=/cache/huggingface \
    TRANSFORMERS_CACHE=/cache/huggingface \
    TORCH_NCCL_ASYNC_ERROR_HANDLING=1 \
    NCCL_P2P_DISABLE=0 \
    NCCL_IB_DISABLE=1 \
    # Defaults that you can override at `docker run`:
    HOST=0.0.0.0 \
    PORT=8000 \
    BACKEND=vllm \
    HF_MODEL_ID=meta-llama/Llama-3.1-8B-Instruct

# Expose API port
EXPOSE 8000

# Healthcheck hits your /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -fsS http://localhost:${PORT}/health || exit 1


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header", "--timeout-keep-alive", "65"]
