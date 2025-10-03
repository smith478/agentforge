# LiteLLM + Kubernetes Learning Project

This project is a self-contained learning environment for exploring the integration of LiteLLM with Kubernetes. It demonstrates how to deploy a simple Flask-based chat API that can be dynamically configured to use different large language models (LLMs), including local models served via Ollama and remote models from providers like OpenAI and Google Gemini.

## Key Features

- **LiteLLM Integration:** The project uses LiteLLM to provide a unified interface for interacting with various LLMs.
- **Kubernetes Deployment:** The application is containerized using Docker and deployed to a Kubernetes cluster.
- **Dynamic Model Switching:** The chat API can be reconfigured on-the-fly to switch between different LLM providers without requiring a code change or redeployment of the application container.
- **Local and Remote Model Support:** The project includes configurations for using both local models (via Ollama with a `hostPath` volume) and remote models (via Ollama with an `emptyDir` volume, or by connecting to external APIs).

## Learning Objectives

- Understand how to containerize a Python application with Docker.
- Learn the basics of Kubernetes deployments, services, ConfigMaps, and Secrets.
- Explore how to use LiteLLM to abstract away the differences between various LLM APIs.
- Gain experience with deploying and managing a multi-component application in a local Kubernetes environment.
