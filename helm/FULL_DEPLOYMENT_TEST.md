# Full Deployment Process Test Guide

## Pre-deployment Checklist

### 1. Environment Preparation
- [ ] Docker Desktop is running and accessible
- [ ] Minikube is installed and configured
- [ ] Helm 3.x is installed and accessible
- [ ] kubectl is installed and configured
- [ ] Internet connectivity for pulling images
- [ ] Sufficient disk space (>2GB free)
- [ ] Sufficient RAM (>4GB available)

### 2. Repository Preparation
- [ ] Clone the repository: `git clone <repo-url>`
- [ ] Navigate to the project: `cd todo-app/Phase-IV`
- [ ] Verify all required files exist in `helm/` directory

## Deployment Process

### Step 1: Start Minikube
```bash
# Start Minikube with Docker driver
minikube start --driver=docker --memory=4096 --cpus=2

# Verify cluster is running
kubectl cluster-info
```

### Step 2: Build Container Images
```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Verify images were created
docker images | grep todo-
```

### Step 3: Prepare Configuration
```bash
# Create a production values file
cat > production-values.yaml << EOF
# Production-specific configuration
replicaCount: 2

image:
  repository: todo-backend
  tag: latest
  pullPolicy: Never  # Since we're using minikube's local registry

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70

env:
  DATABASE_URL: "postgresql://postgres:5432/todo_db"
  NEXT_PUBLIC_BETTER_AUTH_URL: "http://todo-app-frontend:3000"
  NEXT_PUBLIC_BACKEND_API_URL: "http://todo-app-backend:8000"
EOF
```

### Step 4: Install Database (if needed)
```bash
# Install PostgreSQL using Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql --set auth.postgresPassword=secretpassword
```

### Step 5: Update Secrets
```bash
# Create secrets for sensitive data
kubectl create secret generic todo-app-backend-secrets \
  --from-literal=cohere-api-key=<your-cohere-api-key> \
  --from-literal=better-auth-secret=<your-better-auth-secret> \
  --from-literal=database-password=secretpassword \
  --save-config --dry-run=client -o yaml | kubectl apply -f -

# Verify secrets were created
kubectl get secrets | grep todo-app-backend
```

### Step 6: Deploy Backend
```bash
# Deploy backend service
helm install todo-backend ./helm/todo-app-backend -f production-values.yaml

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app-backend --timeout=300s
```

### Step 7: Deploy Frontend
```bash
# Create frontend values
cat > frontend-values.yaml << EOF
replicaCount: 2

image:
  repository: todo-frontend
  tag: latest
  pullPolicy: Never

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

env:
  NEXT_PUBLIC_BETTER_AUTH_URL: "http://todo-app-frontend:3000"
  NEXT_PUBLIC_BACKEND_API_URL: "http://todo-app-backend:8000"
EOF

# Deploy frontend service
helm install todo-frontend ./helm/todo-app-frontend -f frontend-values.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app-frontend --timeout=300s
```

## Verification Steps

### 1. Check Pod Status
```bash
# Verify all pods are running
kubectl get pods

# Check detailed pod status
kubectl describe pods -l app.kubernetes.io/name=todo-app-backend
kubectl describe pods -l app.kubernetes.io/name=todo-app-frontend
```

### 2. Check Service Status
```bash
# Verify services are created
kubectl get services

# Check service endpoints
kubectl get endpoints todo-app-backend
kubectl get endpoints todo-app-frontend
```

### 3. Check Logs
```bash
# Check backend logs
kubectl logs -l app.kubernetes.io/name=todo-app-backend --tail=50

# Check frontend logs
kubectl logs -l app.kubernetes.io/name=todo-app-frontend --tail=50
```

### 4. Test Application Connectivity
```bash
# Port forward to test the application
kubectl port-forward svc/todo-app-frontend 3000:3000 &
kubectl port-forward svc/todo-app-backend 8000:8000 &

# Test backend health endpoint
curl http://localhost:8000/health

# Test frontend is accessible
curl http://localhost:3000
```

### 5. Test Scaling
```bash
# Scale backend to 3 replicas
helm upgrade todo-backend ./helm/todo-app-backend --set replicaCount=3

# Verify scaling worked
kubectl get pods -l app.kubernetes.io/name=todo-app-backend
```

## Advanced Testing

### 1. Load Testing
```bash
# Install hey load generator
go install github.com/rakyll/hey@latest

# Generate load to test scaling
hey -z 5m -c 10 http://localhost:8000/api/health

# Monitor scaling in another terminal
kubectl get hpa -w
```

### 2. Configuration Update Test
```bash
# Update configuration without rebuilding
kubectl patch configmap todo-app-backend-config --patch='{"data":{"LOG_LEVEL":"debug"}}'

# Restart deployment to pick up config changes
kubectl rollout restart deployment/todo-app-backend

# Verify new configuration is applied
kubectl logs -l app.kubernetes.io/name=todo-app-backend --tail=20
```

## Cleanup Process
```bash
# Uninstall Helm releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Delete secrets
kubectl delete secret todo-app-backend-secrets

# Stop Minikube
minikube stop

# Optionally delete Minikube cluster
minikube delete
```

## Troubleshooting

### Common Issues
- **Images not found**: Ensure `eval $(minikube docker-env)` was run before building
- **Insufficient resources**: Increase Minikube memory/CPU allocation
- **Connection timeouts**: Check firewall settings and port availability
- **Pull errors**: Set `pullPolicy: Never` when using local images

### Diagnostic Commands
```bash
# Check cluster events
kubectl get events --sort-by='.lastTimestamp'

# Describe problematic pods
kubectl describe pods

# Check node resources
kubectl top nodes

# Check pod resources
kubectl top pods
```

## Success Criteria
- [ ] All pods are running and healthy
- [ ] Services are accessible
- [ ] Application responds to requests
- [ ] Scaling works as expected
- [ ] Configuration updates apply correctly
- [ ] Network policies allow proper communication