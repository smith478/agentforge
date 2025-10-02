# agentforge
Exploring agents

This shows how to set up a Google's ADK (Agent Development Kit) project using Ollama models locally, using **uv** for Python package / environment management.

---

## What is this

- **ADK**: Google’s Agent Development Kit, to build agents (LLM agents, workflow agents, etc.). 
- **Ollama**: A local or custom LLM provider (assume you have Ollama installed/configured).  
- **uv**: A Python tool for environment / dependency management.

---

## Prerequisites

- Python 3.10+ installed  
- Ollama installed and at least one model pulled locally (e.g. `ollama pull llama2` or similar)  
- `uv` installed globally or via pip so that you can run it (e.g. `pip install uv` or via your OS package manager)  


---

## Setup Instructions

```bash
# 1. Initialize uv environment
# This creates a virtual environment managed by uv, and a uv.toml (or update it) to track dependencies
uv init

# 2. Add dependencies
uv add google-adk

# If there is a Python client or connector for Ollama, add it. If not, you might use a generic HTTP client.
# Example: let's assume using `ollama` python package (if exists) or using requests
uv add requests

# 3. Activate the environment
uv activate

# 4. (Optional) Pin versions in uv.toml, lock file
# uv will manage dependency locking
```
