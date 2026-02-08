#!/bin/bash
# Deployment script for Todo App on Kubernetes
# This script assumes Kubernetes is enabled in Docker Desktop

echo "Starting deployment of Todo App to Kubernetes..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Kubernetes cluster is accessible
echo "Checking Kubernetes connectivity..."
kubectl cluster-info || {
    echo "Cannot connect to Kubernetes cluster. Please ensure:"
    echo "1. Docker Desktop is running"
    echo "2. Kubernetes is enabled in Docker Desktop settings"
    exit 1
}

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "helm is not installed or not in PATH"
    exit 1
fi

echo "Kubernetes cluster is accessible!"

# If minikube is supposed to be used, start it
echo "Starting Minikube with Docker driver..."
minikube start --driver=docker || {
    echo "Failed to start Minikube. Please check Docker Desktop settings."
    echo "Make sure Kubernetes is enabled in Docker Desktop settings."
    exit 1
}

echo "Minikube is running!"

# Load Docker images into Minikube
echo "Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build images if they don't exist
if [[ "$(docker images -q todo-backend:latest 2> /dev/null)" == "" ]]; then
    echo "Building backend image..."
    cd ../backend && docker build -t todo-backend:latest . && cd ../Phase-IV
else
    echo "Backend image already exists"
fi

if [[ "$(docker images -q todo-frontend:latest 2> /dev/null)" == "" ]]; then
    echo "Building frontend image..."
    cd ../frontend && docker build -t todo-frontend:latest . && cd ../Phase-IV
else
    echo "Frontend image already exists"
fi

echo "Deploying Todo App with Helm..."

# Install Helm charts
helm install todo-backend ./helm/todo-app-backend || {
    echo "Failed to install backend chart"
    exit 1
}

helm install todo-frontend ./helm/todo-app-frontend || {
    echo "Failed to install frontend chart"
    exit 1
}

echo "Applications deployed successfully!"
echo "Check status with: kubectl get pods,svc"
echo "Access the frontend: minikube service todo-frontend --url"