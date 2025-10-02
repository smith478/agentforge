# LiteLLM + Kubernetes Learning Project

A self-contained project to explore LiteLLM and Kubernetes with a local Ollama model, compatible with OpenAI format.

## Prerequisites

- Docker
- Kubernetes cluster (minikube or Docker Desktop with Kubernetes enabled)
- kubectl

## Project Structure

```
.
├── app.py                      # Flask API with LiteLLM
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container Image definition
└── kubernetes/
    ├── deployment.yaml         # Main app deployment, service, config
    ├── ollama.yaml             # Original Ollama deployment (remote mode)
    ├── ollama-local.yaml       # Ollama with local model sharing
    └── ollama-remote.yaml      # Ollama with fresh model downloads
```

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t litellm-chat:latest .
```

If using minikube, load the image:
```bash
minikube image load litellm-chat:latest
```

### 2. Deploy Ollama

**Option A: Use Local Models**

If you have Ollama models on your local machine, you can share them with Kubernetes:

```bash
kubectl apply -f kubernetes/ollama-local.yaml
```

**Option B: Download models Fresh in Kubernetes**

If you want Kubernetes to download models independently:

```bash
kubectl apply -f kubernetes/ollama-remote.yaml
```

Pull a model:
```bash
# Get the ollama pod name
kubectl get pods -l app=ollama

# Pull a model (e.g., qwen3:8b)
kubectl exec -it <ollama-pod-name> -- ollama pull qwen3:8b
```

**Key Difference:**
- **ollama-local.yaml**: Uses `hostPath` volume to mount your local `~/.ollama` directory - models persist and are shared with your host
- **ollama-remote.yaml**: Uses `emptyDir` volume - models are downloaded fresh and deleted when pod restarts

### 3. Verify Ollama Models

```bash
# List available models in the Ollama pod
kubectl exec -it <ollama-pod-name> -- ollama list
```

### 4. Deploy the Chat API

```bash
kubectl apply -f kubernetes/development.yaml
```
