# Quickstart Guide: Todo App Kubernetes Deployment

## Overview
This guide provides instructions for deploying the containerized Todo app to a local Kubernetes cluster using Minikube and Helm.

## Prerequisites

### System Requirements
- Docker Desktop with Kubernetes enabled OR Minikube installed
- Helm 3.x installed
- kubectl installed
- kubectl-ai (optional, for AI-assisted commands)
- Docker AI (Gordon) enabled (optional, for AI-assisted Docker operations)

### Environment Setup
1. Ensure Docker Desktop is running
2. Start Minikube with Docker driver:
   ```bash
   minikube start --driver=docker
   ```
3. Verify cluster connectivity:
   ```bash
   kubectl cluster-info
   ```

### Required Tools Installation
```bash
# Install Helm (if not already installed)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify installations
helm version
kubectl version --client
docker --version
```

## Container Images Preparation

### Option 1: Build Images Locally
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Build the backend container image:
   ```bash
   docker build -t todo-backend:latest .
   ```

3. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

4. Build the frontend container image:
   ```bash
   docker build -t todo-frontend:latest .
   ```

### Option 2: Using Docker AI (Gordon)
1. Use Docker AI to generate optimized Dockerfiles:
   ```bash
   # Gordon can assist with Dockerfile creation and optimization
   gordon suggest dockerfile --context ./backend
   gordon suggest dockerfile --context ./frontend
   ```

2. Build the images using optimized Dockerfiles:
   ```bash
   docker build -t todo-backend:latest -f ./backend/Dockerfile .
   docker build -t todo-frontend:latest -f ./frontend/Dockerfile .
   ```

## Loading Images into Minikube

1. Set Docker environment to point to Minikube:
   ```bash
   eval $(minikube docker-env)
   ```

2. Rebuild images in Minikube's Docker context:
   ```bash
   cd backend && docker build -t todo-backend:latest . && cd ..
   cd frontend && docker build -t todo-frontend:latest . && cd ..
   ```

## Helm Chart Installation

### Backend Helm Chart
1. Navigate to the Helm charts directory:
   ```bash
   cd helm/todo-app-backend
   ```

2. Install the backend chart:
   ```bash
   helm install todo-backend . \
     --set image.repository=todo-backend \
     --set image.tag=latest \
     --set replicaCount=1
   ```

### Frontend Helm Chart
1. Navigate to the frontend chart directory:
   ```bash
   cd ../todo-app-frontend
   ```

2. Install the frontend chart:
   ```bash
   helm install todo-frontend . \
     --set image.repository=todo-frontend \
     --set image.tag=latest \
     --set replicaCount=1
   ```

## Configuration Setup

### Environment Variables
Configure environment variables using Helm values:

```bash
# Update backend with database URL and API keys
helm upgrade todo-backend . \
  --set env.DATABASE_URL="postgresql://user:pass@postgres:5432/todo_db" \
  --set env.COHERE_API_KEY="your-cohere-key" \
  --set env.BETTER_AUTH_SECRET="your-auth-secret"
```

### Secrets Management
Create Kubernetes secrets for sensitive information:

```bash
# Create a secret for API keys
kubectl create secret generic todo-secrets \
  --from-literal=cohere_api_key="your-cohere-api-key" \
  --from-literal=database_url="postgresql://user:pass@postgres:5432/todo_db" \
  --from-literal=auth_secret="your-auth-secret"
```

## Service Access

### Check Service Status
Verify that all services are running:

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments
```

### Access the Application
1. Get the frontend service URL:
   ```bash
   minikube service todo-frontend --url
   ```

2. Or expose the service locally:
   ```bash
   kubectl port-forward svc/todo-frontend 3000:80
   ```

## Scaling the Application

### Scale Backend Services
Increase the number of backend replicas:

```bash
# Scale to 3 replicas
helm upgrade todo-backend ./todo-app-backend \
  --set replicaCount=3

# Or use kubectl directly
kubectl scale deployment todo-backend --replicas=3
```

### Using kubectl-ai for Scaling
```bash
# AI-assisted scaling command
kubectl-ai scale deployment todo-backend --to 3
```

## Health Monitoring

### Check Application Health
```bash
# Check pod status
kubectl get pods -o wide

# Check pod logs
kubectl logs -l app=todo-backend

# Check deployment status
kubectl rollout status deployment/todo-backend
```

### AI-Assisted Monitoring
```bash
# Use kubectl-ai to check cluster health
kubectl-ai get pods --show-status
kubectl-ai describe deployment todo-backend
```

## Troubleshooting

### Common Issues
1. **Images not found**: Ensure you ran `eval $(minikube docker-env)` before building images
2. **Service not accessible**: Check if the service port matches the container port
3. **Configuration errors**: Verify that ConfigMaps and Secrets are correctly applied

### Debug Commands
```bash
# Check Minikube status
minikube status

# Get detailed pod information
kubectl describe pod <pod-name>

# Check cluster events
kubectl get events --sort-by='.lastTimestamp'

# Tail pod logs
kubectl logs -f <pod-name>
```

## Cleanup

### Uninstall Helm Releases
```bash
helm uninstall todo-frontend
helm uninstall todo-backend
```

### Stop Minikube
```bash
minikube stop
```

### Optional: Delete Minikube Cluster
```bash
minikube delete
```

## Advanced Operations

### Using AI-Assisted DevOps
```bash
# Use kagent for advanced operations
kagent deploy --chart todo-backend --values production-values.yaml

# Use kubectl-ai for complex queries
kubectl-ai get pods --selector app=todo-backend --output jsonpath='{.items[*].status.phase}'
```

### Custom Configuration
Modify values.yaml files to customize your deployment:

```yaml
# Example values.yaml customization
image:
  repository: todo-backend
  tag: latest
  pullPolicy: IfNotPresent

replicaCount: 2

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

env:
  DATABASE_URL: "postgresql://user:pass@postgres:5432/todo_db"
  COHERE_API_KEY: "your-cohere-key"
```

Apply custom configuration:
```bash
helm upgrade todo-backend ./todo-app-backend -f custom-values.yaml
```