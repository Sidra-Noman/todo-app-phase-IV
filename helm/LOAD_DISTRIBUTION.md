# Load Distribution Verification for Todo App

## Verifying Load Distribution Across Backend Replicas

Once multiple backend replicas are running, you can verify that load is being distributed properly.

### 1. Check Pod Distribution
First, verify that multiple pods are running:
```bash
kubectl get pods -l app.kubernetes.io/name=todo-app-backend
```

### 2. Monitor Resource Usage
Monitor CPU and memory usage across all backend pods:
```bash
kubectl top pods -l app.kubernetes.io/name=todo-app-backend
```

### 3. Check Service Endpoints
Verify that the service is routing to all backend pods:
```bash
kubectl get endpoints todo-app-backend
```

### 4. Application-Level Monitoring
If your application logs requests with pod names, you can check logs to see requests being served by different pods:
```bash
kubectl logs -l app.kubernetes.io/name=todo-app-backend --since=10m | grep -i "request\|handling"
```

### 5. Load Testing
Generate load and observe how it's distributed:
```bash
# Watch pods during load testing
kubectl get pods -w -l app.kubernetes.io/name=todo-app-backend

# In another terminal, generate load
hey -z 1m -c 10 http://todo-app-backend:8000/api/health
```

### 6. Metrics Collection
If Prometheus is available, you can check metrics for balanced load:
```bash
# Check if Prometheus is available
kubectl get svc | grep prometheus

# Query request rate per pod
sum by(pod) (rate(http_requests_total[1m]))
```

### Expected Results
- Requests should be distributed approximately evenly across all backend pods
- All pods should show activity during load testing
- No single pod should be significantly more loaded than others
- Response times should remain consistent