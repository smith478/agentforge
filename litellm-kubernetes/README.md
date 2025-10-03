# LiteLLM + Kubernetes Learning Project

A self-contained project to explore LiteLLM and Kubernetes with a local Ollama model, compatible with OpenAI format.

## High-Level Concepts

This project demonstrates several key concepts:

- **Model Abstraction with LiteLLM:** LiteLLM acts as a universal adapter, allowing the application to communicate with various LLM providers (Ollama, OpenAI, Gemini) through a single, consistent API. This simplifies the code and makes it easy to switch between models without significant refactoring.
- **Containerization with Docker:** The Flask application is packaged into a lightweight, portable Docker image. This ensures that the application and its dependencies are isolated and can run consistently across different environments.
- **Declarative Deployments with Kubernetes:** Kubernetes is used to orchestrate the deployment and management of the application and its components. The desired state of the application is defined in YAML files, and Kubernetes works to maintain that state.
- **Dynamic Configuration with ConfigMaps and Secrets:** Instead of hardcoding model information, the application is configured at runtime using Kubernetes ConfigMaps (for non-sensitive data like model names) and Secrets (for sensitive data like API keys). This allows for on-the-fly updates without rebuilding the Docker image or redeploying the application.
- **Service Discovery in Kubernetes:** The chat API discovers and communicates with the Ollama service using Kubernetes' built-in DNS resolution (`ollama.default.svc.cluster.local`). This allows the components to find each other without needing to know their specific IP addresses.
- **Data Persistence with Volumes:** The project illustrates two approaches for managing model data in Kubernetes:
    - `hostPath` volumes for persisting data on the host machine (useful for development and sharing local models).
    - `emptyDir` volumes for ephemeral, pod-specific storage (useful for temporary data that doesn't need to persist).

## Prerequisites

- Docker
- Kubernetes cluster (minikube or Docker Desktop with Kubernetes enabled)
- kubectl

## Project Structure

```
.
├── .env                        # For storing API keys
├── app.py                      # Flask API with LiteLLM
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container Image definition
├── GEMINI.md                   # Project documentation
└── kubernetes/
    ├── deployment.yaml         # Main app deployment, service, config
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
kubectl apply -f kubernetes/deployment.yaml
```

### 5. Test the API

Get the service URL:
```bash
# For minikube
minikube service litellm-chat-service --url

# For Docker Desktop
kubectl get service litellm-chat-service
```

Test with curl:
```bash
curl -X POST http://<service-url>/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is Kubernetes?"}
    ],
    "temperature": 0.7
  }'
```

## Switching Between Providers

LiteLLM makes it easy to switch between different AI providers. Just update the ConfigMap and Secret:

### For OpenAI (GPT-4):

```bash
kubectl patch configmap litellm-config --type merge -p '{"data":{"model_name":"gpt-4","api_base":"https://api.openai.com/v1/"}}'
kubectl patch secret litellm-secret --type merge -p '{"stringData":{"api_key":"'''$(grep OPENAI_API_KEY .env | cut -d '=' -f2)'''"}}'
kubectl rollout restart deployment litellm-chat-api
```

### For Google Gemini (Gemini 2.5 Pro):

```bash
kubectl patch configmap litellm-config --type merge -p '{"data":{"model_name":"gemini/gemini-2.5-pro","api_base":""}}'
kubectl patch secret litellm-secret --type merge -p '{"stringData":{"api_key":"'''$(grep GEMINI_API_KEY .env | cut -d '=' -f2)'''"}}'
kubectl rollout restart deployment litellm-chat-api
```

### Back to Ollama:

```bash
kubectl patch configmap litellm-config --type merge -p '{"data":{"model_name":"ollama/qwen3:8b","api_base":"http://ollama.default.svc.cluster.local:11434"}}'
kubectl patch secret litellm-secret --type merge -p '{"stringData":{"api_key":""}}'
kubectl rollout restart deployment litellm-chat-api
```

## Monitoring & Debugging

### Check Pod Status

To see the status of your pods:
```bash
kubectl get pods -l app=litellm-chat-api
kubectl get pods -l app=ollama
```

### View Logs

To view the logs for the chat API or Ollama:
```bash
# Get the pod name
kubectl get pods -l app=litellm-chat-api

# View logs
kubectl logs <litellm-pod-name>

# Follow logs in real-time
kubectl logs -f <litellm-pod-name>
```

### Interactive Shell

To get an interactive shell inside a container:
```bash
# Get the pod name
kubectl get pods -l app=litellm-chat-api

# Exec into the pod
kubectl exec -it <litellm-pod-name> -- /bin/sh
```

## Cleanup

To delete all the resources created in this project:
```bash
kubectl delete deployment litellm-chat-api ollama
kubectl delete service litellm-chat-service ollama
kubectl delete configmap litellm-config
kubectl delete secret litellm-secret
```
