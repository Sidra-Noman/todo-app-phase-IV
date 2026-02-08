# Configuration Management for Todo App

## Updating Configuration Without Container Rebuild

One of the key benefits of using ConfigMaps and Secrets in Kubernetes is the ability to update application configuration without rebuilding container images.

## Backend Configuration Updates

### 1. Updating ConfigMap Values
To update the backend configuration without rebuilding the container:

```bash
# Edit the ConfigMap directly
kubectl edit configmap todo-app-backend-config

# Or patch the ConfigMap
kubectl patch configmap todo-app-backend-config -p '{"data":{"LOG_LEVEL":"debug"}}'
```

### 2. Updating Secret Values
To update sensitive configuration:

```bash
# Create a new secret with updated values
kubectl create secret generic todo-app-backend-secrets \
  --from-literal=cohere-api-key="new-api-key" \
  --from-literal=better-auth-secret="new-auth-secret" \
  --dry-run=client -o yaml | kubectl apply -f -
```

### 3. Rolling Updates
Changes to ConfigMaps and Secrets don't automatically propagate to running pods. To apply the changes:

#### Option A: Restart the deployment
```bash
kubectl rollout restart deployment/todo-app-backend
```

#### Option B: Force a rolling update
```bash
kubectl patch deployment todo-app-backend -p "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"timestamp\":\"$(date +'%s')\"}}}}}"
```

## Frontend Configuration Updates

Similar process for the frontend:

```bash
# Update ConfigMap
kubectl patch configmap todo-app-frontend-config -p '{"data":{"THEME":"dark"}}'

# Apply changes with rolling update
kubectl rollout restart deployment/todo-app-frontend
```

## Best Practices for Configuration Updates

### 1. Use Immutable ConfigMaps for Critical Settings
For settings that shouldn't change frequently, consider using immutable ConfigMaps:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-app-backend-immutable-config
data:
  # Critical settings that rarely change
immutable: true
```

### 2. Version Configuration Changes
Keep track of configuration changes by using versioned ConfigMaps:

```bash
# Create versioned ConfigMap
kubectl create configmap todo-app-backend-config-v2 --from-file=config.yaml

# Update deployment to use new ConfigMap
helm upgrade todo-backend ./helm/todo-app-backend --set configMap.version=v2
```

### 3. Validate Configuration Before Applying
Always validate configuration changes:

```bash
# Dry-run the ConfigMap update
kubectl create configmap test-config --from-literal=key=value --dry-run=client -o yaml

# Check if the deployment validates with new config
kubectl create configmap temp-config --from-literal=test-key=test-value --dry-run=server
```

### 4. Monitor Configuration Changes
After applying configuration changes, monitor the application:

```bash
# Check rollout status
kubectl rollout status deployment/todo-app-backend

# Monitor logs for configuration-related errors
kubectl logs -f deployment/todo-app-backend --since=10m

# Check events for configuration issues
kubectl get events --sort-by='.lastTimestamp'
```

## Automated Configuration Updates

### Using GitOps
With tools like ArgoCD or Flux, configuration updates can be automated:

```yaml
# example ArgoCD Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: todo-app-backend
spec:
  source:
    path: helm/todo-app-backend
    repoURL: https://github.com/your-org/todo-app
    targetRevision: HEAD
    helm:
      valueFiles:
        - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: todo-app
```

### Using External Configuration Stores
Consider using external configuration stores like:

- HashiCorp Vault for secrets
- Consul for application configuration
- AWS Systems Manager Parameter Store (for AWS EKS)
- Azure Key Vault (for AKS)

## Verification Steps

After updating configuration:

1. Verify the ConfigMap/Secret was updated:
   ```bash
   kubectl get configmap todo-app-backend-config -o yaml
   ```

2. Check if the new configuration is reflected in the pods:
   ```bash
   kubectl exec -it deployment/todo-app-backend -- env | grep YOUR_CONFIG_VAR
   ```

3. Monitor application behavior:
   ```bash
   kubectl logs deployment/todo-app-backend --since=5m
   ```

4. Verify the application functions correctly with new configuration