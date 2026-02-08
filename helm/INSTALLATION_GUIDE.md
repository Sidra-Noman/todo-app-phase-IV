# Quickstart: Deploy Todo App to Kubernetes

## Quick Deployment Guide

This guide will help you deploy the Todo App to a local Kubernetes cluster using Minikube and Helm.

### Pre-requisites
- Docker Desktop running
- Minikube installed and running with: `minikube start --driver=docker`
- Helm 3.x installed
- kubectl configured to use minikube context

### Quick Deployment Steps

1. Clone or navigate to the project directory
2. Start Minikube: `minikube start --driver=docker`
3. Build and load Docker images into Minikube:
   ```bash
   eval $(minikube docker-env)
   docker build -t todo-backend:latest ./backend
   docker build -t todo-frontend:latest ./frontend
   ```
4. Install backend chart: `helm install todo-backend ./helm/todo-app-backend`
5. Install frontend chart: `helm install todo-frontend ./helm/todo-app-frontend`
6. Verify deployment: `kubectl get pods,services`
7. Access the application: `minikube service todo-app-frontend --url`

### Verify functionality
- Check pod status: `kubectl get pods`
- Check service endpoints: `kubectl get services`
- View pod logs: `kubectl logs -l app.kubernetes.io/name=todo-app-backend`
- Port forward for local testing: `kubectl port-forward svc/todo-app-frontend 3000:3000`

## Detailed Instructions

## Installation Steps

1. Install backend chart:
```bash
helm install todo-backend ./helm/todo-app-backend
```

2. Install frontend chart:
```bash
helm install todo-frontend ./helm/todo-app-frontend
```

## Verification Steps

1. Check if pods are running:
```bash
kubectl get pods
```

2. Check if services are available:
```bash
kubectl get services
```

3. Port forward to test the application:
```bash
kubectl port-forward svc/todo-app-frontend 3000:3000
kubectl port-forward svc/todo-app-backend 8000:8000
```

4. Access the application at http://localhost:3000

## Troubleshooting

- If pods fail to start, check logs: `kubectl logs <pod-name>`
- If images can't be pulled, ensure they're built and loaded in minikube: `minikube image load <image-name>`
- Check resource availability: `kubectl describe nodes`