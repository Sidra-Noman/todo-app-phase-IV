# Kubernetes Setup Instructions for Windows

## Prerequisites

Before running the containerized Todo application on Kubernetes, ensure Docker Desktop is properly configured with Kubernetes support.

### 1. Enable Kubernetes in Docker Desktop

1. Open Docker Desktop
2. Go to Settings (top-right gear icon)
3. Click on "Kubernetes" tab
4. Check "Enable Kubernetes"
5. Click "Apply & Restart"
6. Wait for Docker Desktop to restart with Kubernetes enabled

### 2. Verify Kubernetes is Available

After Docker Desktop restarts with Kubernetes enabled:

```bash
# Verify kubectl can connect to the cluster
kubectl cluster-info

# You should see output showing the Kubernetes master endpoint
```

### 3. Start Minikube with Docker Driver

Once Kubernetes is enabled in Docker Desktop:

```bash
# Start Minikube using the Docker driver
minikube start --driver=docker

# Verify the cluster is running
minikube status
```

### 4. Load Docker Images into Minikube

To make your locally built images available to Minikube:

```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images in Minikube's context (if not already built)
cd backend && docker build -t todo-backend:latest . && cd ..
cd frontend && docker build -t todo-frontend:latest . && cd ..

# Alternatively, if images were built in default context, you can load them:
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 5. Deploy with Helm

```bash
# Install the Helm charts
helm install todo-backend ./helm/todo-app-backend
helm install todo-frontend ./helm/todo-app-frontend

# Verify deployments
kubectl get pods
kubectl get services
```

## Troubleshooting

### If `minikube start --driver=docker` fails:

1. **Check Docker Desktop Kubernetes Status**:
   ```bash
   kubectl cluster-info
   ```

2. **Verify Docker is running**:
   ```bash
   docker ps
   ```

3. **Try using Docker Desktop Kubernetes directly** (without Minikube):
   ```bash
   # Deploy directly to Docker Desktop Kubernetes
   kubectl apply -f helm/todo-app-backend/templates/deployment.yaml
   kubectl apply -f helm/todo-app-backend/templates/service.yaml
   kubectl apply -f helm/todo-app-frontend/templates/deployment.yaml
   kubectl apply -f helm/todo-app-frontend/templates/service.yaml
   ```

### If you get permission errors:

1. Run PowerShell as Administrator
2. Make sure Hyper-V feature is enabled in Windows Features
3. Restart Docker Desktop after enabling features

## Environment Validation

To validate that your environment is properly configured:

```bash
# Check that Docker is running
docker version

# Check that Kubernetes is enabled and accessible
kubectl cluster-info

# Check that Minikube can start (optional, if using Minikube)
minikube status || echo "Minikube not started yet"
```

## Expected Output

After following these steps, you should see:
- Docker Desktop showing Kubernetes as enabled
- `kubectl cluster-info` showing the Kubernetes master endpoint
- Ability to deploy Kubernetes resources using kubectl or Helm
- Successful deployment of the Todo application containers