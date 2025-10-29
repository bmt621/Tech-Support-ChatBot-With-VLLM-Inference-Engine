# Tech Support Chatbot - Complete Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Frontend Setup](#frontend-setup)
- [Performance Tuning](#performance-tuning)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## Overview

This repository contains a production-ready Retrieval-Augmented Generation (RAG) chatbot designed for tech support applications. The system combines semantic search with large language model inference to provide accurate, context-aware technical assistance.

### Key Features

- **High-Performance Inference**: vLLM engine with FP8 quantization
- **Semantic Search**: FAISS-powered retrieval over technical knowledge base
- **Session Management**: Stateful conversations with history tracking
- **Production-Ready API**: FastAPI backend with CORS support
- **Interactive UI**: Streamlit-based chat interface

### Performance Metrics

- **Throughput**: 100+ tokens/second on A100 GPU
- **Latency**: <1s first token, <10s full response
- **Memory**: 8.5GB GPU VRAM (model) + 2GB (KV cache)
- **Concurrency**: 3.91x maximum parallel requests

---

## Architecture

### System Components

```
┌─────────────────┐
│   Streamlit UI  │  (Port 8501)
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI App   │  (Port 8000)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────┐  ┌──────────┐
│FAISS│  │   vLLM   │
│Index│  │  Engine  │
└─────┘  └──────────┘
```

### Core Technologies

#### 1. vLLM Inference Engine

vLLM provides significant advantages over standard HuggingFace transformers:

**PagedAttention Memory Management**
- Dynamic KV cache allocation in non-contiguous blocks
- 55-80% reduction in memory waste vs. contiguous allocation
- Enables longer context windows and higher batch sizes

**Continuous Batching**
- Processes requests as they arrive without waiting for batch completion
- Eliminates head-of-line blocking from long sequences
- 2-3x throughput improvement over static batching

**CUDA Graph Optimization**
- Pre-compiles execution graphs during warmup phase
- Reduces kernel launch overhead by ~20ms per iteration
- Captured in 25 seconds during startup (see logs)

**FP8 Quantization**
- Compresses model weights from BF16 (2 bytes) to FP8 (1 byte)
- Uses Marlin kernel for weight-only compression on non-Hopper GPUs
- Maintains 95%+ quality with 50% memory savings

**Performance Comparison**

| Metric | HuggingFace | vLLM | Improvement |
|--------|-------------|------|-------------|
| Throughput | 30 tok/s | 100+ tok/s | 3.3x |
| Memory Efficiency | Baseline | 55-80% less | 2-5x |
| Concurrent Users | 1-2 | 3-4 | 2x |
| First Token Latency | ~800ms | ~300ms | 2.6x |

#### 2. FAISS Retrieval System

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Index Type**: Flat Inner Product (exact search, cosine similarity)
- **Chunking Strategy**: 400-word chunks with 100-word overlap
- **Top-K Retrieval**: 3 most relevant chunks per query

#### 3. Knowledge Base Structure

Located in `knowledge_base/tech_support.txt`, the KB is automatically:
- Loaded from `sample_text.py` on first run
- Chunked with overlap for context preservation
- Embedded and indexed for semantic search
- Normalized for cosine similarity matching

---

## Prerequisites

### Hardware Requirements

**GPU Specifications**
- NVIDIA GPU with Compute Capability 7.0+ (V100, T4, A10, A100, RTX 20/30/40 series)
- Minimum 16GB VRAM (24GB recommended for full context length)
- PCIe Gen3 x16 or higher for optimal throughput

**System Requirements**
- 32GB RAM (16GB minimum)
- 50GB free disk space (model cache + Docker layers)
- Ubuntu 20.04/22.04 or compatible Linux distribution

### Software Requirements

**Core Dependencies**
```bash
# Check CUDA version (requires 11.8+)
nvidia-smi

# Check Docker version (requires 20.10+)
docker --version

# Check NVIDIA Container Runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Python Environment** (for local development)
- Python 3.10 or 3.11 (Python 3.12 not yet supported by vLLM)
- pip 23.0+
- virtualenv or conda

### API Access

**Hugging Face Token**

1. Create account at https://huggingface.co/
2. Navigate to https://huggingface.co/settings/tokens
3. Create new token with `read` permissions
4. Accept Llama model license:
   - Visit https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
   - Click "Agree and access repository"
   - Wait for approval (usually instant)

```bash
# Set token as environment variable
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## Installation

### Repository Structure

```
tech-support-chatbot/
├── app.py                 # FastAPI server with session management
├── inference.py           # RAG chatbot logic (TechSupportChatbot class)
├── vllm_model.py         # vLLM wrapper with quantization support
├── sample_text.py        # Knowledge base content (KNOWLEDGE_BASE string)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Multi-stage container build
├── frontend.py           # Streamlit chat interface
├── knowledge_base/       # Auto-generated on first run
│   └── tech_support.txt  # Persisted knowledge base
└── __pycache__/          # Python bytecode cache
```

### Step 1: Clone Repository

```bash
git clone git@github.com:bmt621/Tech-Support-ChatBot-With-VLLM-Inference-Engine.git
cd tech-support-chatbot
```

### Step 2: Verify Files

```bash
ls -la
# Expected output:
# -rw-r--r-- app.py
# -rw-r--r-- inference.py
# -rw-r--r-- vllm_model.py
# -rw-r--r-- sample_text.py
# -rw-r--r-- requirements.txt
# -rw-r--r-- Dockerfile
# -rw-r--r-- frontend.py
```

### Step 3: Review Dependencies

The `requirements.txt` should contain:

```txt
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.0

# LLM Inference
vllm==0.6.3.post1
transformers==4.45.0
torch==2.4.1

# Retrieval
sentence-transformers==3.1.1
faiss-cpu==1.8.0

# Frontend
streamlit==1.38.0
requests==2.32.3

# Utilities
numpy==1.26.4
```

**Note**: `faiss-cpu` is used to avoid CUDA version conflicts. GPU acceleration for FAISS is not critical since embedding search is <10ms.

---

## Running the Application

### Option A: Docker Deployment (Recommended)

#### Build Docker Image

```bash
docker build -t tech-support-chatbot:latest .
```

**Build Process** (~8-10 minutes):
1. Base NVIDIA PyTorch image (7GB)
2. System dependencies installation
3. Python packages compilation
4. Application code copy

**Expected output**:
```
[+] Building 487.3s (12/12) FINISHED
 => [internal] load build definition
 => [internal] load .dockerignore
 => [1/6] FROM nvcr.io/nvidia/pytorch:25.05-py3
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt /app/requirements.txt
 => [4/6] RUN apt-get update && apt-get install -y...
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt
 => [6/6] COPY . /app
 => exporting to image
```

#### Run Container

```bash
docker run -d \
  --name chatbot-api \
  --gpus all \
  --shm-size=8g \
  -p 8000:8000 \
  -e HF_TOKEN="${HF_TOKEN}" \
  -e BACKEND="vllm" \
  -e GPU_MEM_UTIL="0.92" \
  -e VLLM_QUANT="fp8" \
  -e RETRIEVAL_TOP_K="3" \
  -v $(pwd)/cache:/cache/huggingface \
  -v $(pwd)/knowledge_base:/app/knowledge_base \
  --restart unless-stopped \
  tech-support-chatbot:latest
```

**Parameter Breakdown**:

| Flag | Purpose | Default |
|------|---------|---------|
| `--gpus all` | Allocate all GPUs | Required |
| `--shm-size=8g` | Shared memory for PyTorch | 64MB → 8GB |
| `-p 8000:8000` | Expose API port | - |
| `-e HF_TOKEN` | Hugging Face authentication | Required |
| `-e BACKEND` | Inference engine (`vllm`/`hf`) | `vllm` |
| `-e GPU_MEM_UTIL` | VRAM allocation fraction | `0.92` |
| `-e VLLM_QUANT` | Quantization method | `fp8` |
| `-e RETRIEVAL_TOP_K` | Context chunks per query | `3` |
| `-v .../cache` | Persist model downloads | - |
| `-v .../knowledge_base` | Persist FAISS index | - |
| `--restart` | Auto-restart policy | `no` |

#### Monitor Startup

```bash
docker logs -f chatbot-api
```

**Initialization Timeline** (75-90 seconds):

```
[00:00] INFO: Started server process [110809]
[00:00] INFO: Waiting for application startup.
[00:01] WARNING: Chunked prefill enabled for models with max_model_len > 32K
[00:02] INFO: Initializing LLM engine (v0.6.3.post1) with config:
        model='meta-llama/Llama-3.1-8B-Instruct'
        quantization=fp8
        kv_cache_dtype=auto
        max_seq_len=131072
[00:05] INFO: Starting to load model meta-llama/Llama-3.1-8B-Instruct...
[00:07] Loading safetensors checkpoint shards: 100% 4/4 [00:05<00:00]
[00:13] WARNING: GPU does not have native FP8 support. Using Marlin kernel...
[00:14] INFO: Loading model weights took 8.4926 GB
[00:14] INFO: # GPU blocks: 32056, # CPU blocks: 2048
[00:14] INFO: Maximum concurrency: 3.91x
[00:15] INFO: Capturing CUDA graphs (may take 1-3 GiB additional memory)
[00:40] INFO: Graph capturing finished in 25 secs
[00:41] INFO: Application startup complete.
[00:41] INFO: Uvicorn running on http://0.0.0.0:8000
```

**Readiness Check**:

```bash
# Wait for healthy status
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
  echo "Waiting for API..."
  sleep 2
done
echo "API is ready!"
```

---

### Option B: Local Development Setup

#### Create Virtual Environment

```bash
# Using venv
python3.10 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# OR using conda
conda create -n chatbot python=3.10
conda activate chatbot
```

#### Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Installation time**: ~15-20 minutes (compiling PyTorch extensions)

#### Configure Environment

```bash
# Create .env file
cat > .env << EOF
HF_TOKEN=hf_your_token_here
BACKEND=vllm
GPU_MEM_UTIL=0.92
VLLM_QUANT=fp8
RETRIEVAL_TOP_K=3
HF_MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
HOST=0.0.0.0
PORT=8000
EOF

# Load variables
export $(cat .env | xargs)
```

#### Start Backend Server

```bash
# Option 1: Using app.py's main block
python app.py

# Option 2: Using uvicorn directly (more control)
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --timeout-keep-alive 65 \
  --log-level info \
  --no-server-header
```

**Server Output**:
```
INFO:     Started server process [45821]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## API Documentation

### Interactive API Docs

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

#### 1. Health Check

**Request**:
```bash
curl http://localhost:8000/health
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "backend": "vllm",
  "model_id": "meta-llama/Llama-3.1-8B-Instruct",
  "sessions": 2
}
```

**Use Cases**:
- Load balancer health checks
- Deployment readiness probes
- Monitoring active session count

---

#### 2. Chat Message

**Request**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My laptop won'\''t boot up, just a black screen",
    "session_id": null
  }'
```

**Parameters**:
- `message` (required): User query string
- `session_id` (optional): UUID from previous interaction; `null` creates new session

**Response** (200 OK):
```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "reply": "Let's troubleshoot your laptop boot issue step by step:\n\n1. **Power Supply Check**\n   - Ensure the power adapter is securely connected\n   - Look for LED indicators on the laptop or charger\n\n2. **Hard Reset**\n   - Disconnect power and remove battery (if removable)\n   - Hold power button for 30 seconds\n   - Reconnect power and try booting\n\n3. **External Display Test**\n   - Connect to an external monitor\n   - Press Windows+P or Fn+Display key\n   - If external display works, likely an LCD/backlight issue\n\nDoes the laptop make any sounds (fans, beeps) when you press the power button?"
}
```

**Error Responses**:

```json
// 400 Bad Request - Empty message
{
  "detail": "message cannot be empty"
}

// 500 Internal Server Error - Generation failure
{
  "detail": "generation_error: CUDA out of memory"
}
```

**Conversation Flow**:
```bash
# First message (creates session)
curl -X POST http://localhost:8000/chat \
  -d '{"message": "WiFi keeps disconnecting", "session_id": null}'
# Returns: {"session_id": "abc-123", "reply": "..."}

# Follow-up (maintains context)
curl -X POST http://localhost:8000/chat \
  -d '{"message": "It happens every 5 minutes", "session_id": "abc-123"}'
# Returns: {"session_id": "abc-123", "reply": "Based on the 5-minute pattern..."}
```

---

#### 3. Reset Session

**Request**:
```bash
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  }'
```

**Response** (200 OK):
```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status": "cleared"
}
```

**Use Cases**:
- Clear conversation history
- Free memory for long-running sessions
- Reset context for new topic

---

### Example API Session

```python
import requests

API_BASE = "http://localhost:8000"
session_id = None

# Initial query
response = requests.post(f"{API_BASE}/chat", json={
    "message": "How do I reset my router?",
    "session_id": session_id
})
data = response.json()
session_id = data["session_id"]
print(f"Bot: {data['reply']}\n")

# Follow-up
response = requests.post(f"{API_BASE}/chat", json={
    "message": "Where is the reset button located?",
    "session_id": session_id
})
print(f"Bot: {response.json()['reply']}\n")

# Reset conversation
requests.post(f"{API_BASE}/reset", json={"session_id": session_id})
print("Session cleared!")
```

---

## Frontend Setup

### Launch Streamlit Interface

#### Step 1: Set API Endpoint

```bash
# For local backend
export CHATBOT_API_BASE="http://localhost:8000"

# For remote deployment
export CHATBOT_API_BASE="http://your-server-ip:8000"
```

#### Step 2: Start Streamlit

```bash
streamlit run frontend.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

**Access UI**: http://localhost:8501

#### Step 3: Interface Overview

**Main Features**:
- 💬 Chat input at bottom
- 📜 Scrollable message history
- ⚙️ Sidebar settings panel
  - API base URL configuration
  - 🔁 Health check button
  - 🧹 Reset session button
  - 📊 Live health status JSON

**Usage Flow**:
1. Type message in input box
2. Press Enter or click send
3. Watch real-time streaming response
4. Continue conversation with context
5. Use "Reset Session" to start fresh topic

**Sample Interaction**:

```
You: My printer won't connect to WiFi

Bot: I'll help you troubleshoot the printer WiFi connection. Let's go through these steps:

1. Verify Network Requirements
   - Check if your WiFi is 2.4GHz (many printers don't support 5GHz)
   - Ensure router is broadcasting SSID (not hidden)

2. Restart Devices
   - Power cycle the printer (off for 30 seconds)
   - Restart your WiFi router
   - Wait 2 minutes for network stabilization

3. Reconnect Printer
   - Access printer's control panel
   - Navigate to Network/WiFi settings
   - Select your network and enter password
   - Verify IP address assignment

Are you able to see your WiFi network in the printer's available networks list?

You: Yes, I see it but it fails when I enter the password

Bot: Since the network is visible but authentication fails, this suggests a password or security setting issue. Try these steps:

1. Verify Password
   - Double-check WiFi password (case-sensitive)
   - Avoid using smartphone keyboard - manual entry is more reliable
   - Check for special characters that might not register

2. Check Security Protocol
   - Access router settings at 192.168.1.1 (or 192.168.0.1)
   - Verify WiFi security is WPA2-PSK (most compatible)
   - Temporarily disable MAC address filtering
   - Ensure WPS is enabled if you want to use push-button setup

3. Alternative Connection Methods
   - Try WPS button connection (if available on both devices)
   - Use USB connection temporarily to update printer firmware
   - Consider WiFi Direct for direct device-to-printer connection

Does your router's admin panel show any connection attempts from the printer?
```