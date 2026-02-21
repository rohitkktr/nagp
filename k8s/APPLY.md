# Kubernetes Manifests - How to Apply

## Prerequisites
- EKS cluster created and running (2 nodes)
- kubeconfig configured
- kubectl installed

## Kubernetes Manifest Files Structure

```
k8s/
├── deployments/                    # Service deployments
│   ├── auth-deployment.yaml
│   ├── cart-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── order-deployment.yaml
│   └── product-deployment.yaml
├── services/                       # Service definitions
│   ├── auth-service.yaml
│   ├── cart-service.yaml
│   ├── frontend-service.yaml
│   ├── order-service.yaml
│   └── product-service.yaml
├── 01-namespaces.yaml              # Frontend and Backend namespaces
├── 02-configmaps.yaml              # Configuration for services
├── 03-secrets.yaml                 # Credentials (update before applying)
└── 08-hpa-frontend.yaml            # Horizontal Pod Autoscaler
```

## Steps to Apply

### 1. Update Secrets (IMPORTANT)
Edit `03-secrets.yaml` with your credentials:
```yaml
DB_PASSWORD: "your-secure-password"
JWT_SECRET: "your-jwt-secret"
DB_USER: "your-db-user"
```

Also update Docker Hub authentication (base64 encoded).

### 2. Update Image URLs
Edit all deployment files with your Docker Hub username:
- `deployments/auth-deployment.yaml` - Replace `your-username`
- `deployments/product-deployment.yaml` - Replace `your-username`
- `deployments/cart-deployment.yaml` - Replace `your-username`
- `deployments/order-deployment.yaml` - Replace `your-username`
- `deployments/frontend-deployment.yaml` - Replace `your-username`

### 3. Apply Manifests (in order)

```bash
# Create namespaces
kubectl apply -f 01-namespaces.yaml

# Create ConfigMaps
kubectl apply -f 02-configmaps.yaml

# Create Secrets
kubectl apply -f 03-secrets.yaml

# Deploy Backend Services
kubectl apply -f deployments/auth-deployment.yaml
kubectl apply -f deployments/product-deployment.yaml
kubectl apply -f deployments/cart-deployment.yaml
kubectl apply -f deployments/order-deployment.yaml

# Deploy Frontend
kubectl apply -f deployments/frontend-deployment.yaml

# Create Services
kubectl apply -f services/auth-service.yaml
kubectl apply -f services/product-service.yaml
kubectl apply -f services/cart-service.yaml
kubectl apply -f services/order-service.yaml
kubectl apply -f services/frontend-service.yaml

# Enable HPA
kubectl apply -f 08-hpa-frontend.yaml
```

### Or Apply All at Once
```bash
# Apply everything recursively
kubectl apply -f .
```

## Verify Deployment

### Check Namespaces
```bash
kubectl get namespaces
```

### Check Deployments
```bash
# Frontend
kubectl get deployments -n frontend

# Backend
kubectl get deployments -n backend
```

### Check Pods
```bash
# Frontend
kubectl get pods -n frontend

# Backend
kubectl get pods -n backend
```

### Check Services
```bash
# Frontend LoadBalancer URL
kubectl get svc -n frontend
kubectl get svc nagp-frontend -n frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Backend Services (internal)
kubectl get svc -n backend
```

### Check HPA Status
```bash
kubectl get hpa -n frontend
kubectl describe hpa frontend-hpa -n frontend
```

## Accessing Services

### Frontend (External)
```
http://<frontend-loadbalancer-hostname>
```

### Backend Services (Internal)
```
http://auth-service.backend.svc.cluster.local:8000
http://product-service.backend.svc.cluster.local:8001
http://cart-service.backend.svc.cluster.local:8002
http://order-service.backend.svc.cluster.local:8003
```

## Troubleshooting

### Pods Not Running
```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

### Image Pull Errors
```bash
kubectl get events -n <namespace>
```

### Services Not Responding
```bash
# Test connectivity from frontend pod
kubectl exec -it <frontend-pod> -n frontend -- sh
curl http://auth-service.backend.svc.cluster.local:8000/docs
```

## Delete Deployment

```bash
# Delete all resources
kubectl delete -f .

# Or delete namespaces (deletes everything in them)
kubectl delete namespace frontend backend
```
