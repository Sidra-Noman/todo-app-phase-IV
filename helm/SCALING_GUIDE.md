# Scaling Guide for Todo App Backend

## Horizontal Scaling

The Todo App backend can be scaled horizontally by adjusting the replica count in the Helm values.

### Manual Scaling
To manually scale the backend to 3 replicas:

```bash
helm upgrade todo-backend ./helm/todo-app-backend --set replicaCount=3
```

Or update the values file and run:
```bash
helm upgrade todo-backend ./helm/todo-app-backend -f updated-values.yaml
```

### Auto Scaling
To enable horizontal pod autoscaling:

1. Update the values file to enable autoscaling:
```yaml
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
```

2. Apply the changes:
```bash
helm upgrade todo-backend ./helm/todo-app-backend -f values.yaml
```

### Verification
After scaling, verify the new replica count:

```bash
kubectl get deployment todo-app-backend
kubectl get pods
```

You should see the desired number of replicas running.

### Load Testing
To test the scaling capability, you can generate load with tools like `hey` or `ab`:

```bash
# Install hey load generator
go install github.com/rakyll/hey@latest

# Generate load to test scaling
hey -z 5m -c 10 http://<your-service-url>/api/endpoint
```

Monitor the deployment to ensure it scales appropriately based on resource usage.