
# Support Automation Platform — Kubernetes Deployment Guide  
### Minikube → Docker Hub → Helm → AWS EKS

---

# 1. Introduction

This document explains the complete Kubernetes deployment workflow for the **Support Automation Platform**, covering:

- Building & pushing Docker images  
- Deploying to **Minikube** locally  
- Using **Helm** for Kubernetes packaging  
- Deploying to **AWS EKS**  
- Testing, debugging, and validating the application end-to-end  

---

# 2. Architecture Overview

```
Streamlit UI Pod (frontend)
       |
       v
FastAPI Backend Pod
       |
       +-------------------------+
       |                         |
AWS RDS           Neo4j         Elasticsearch
       |
API Gateway → Lambda → Amazon Bedrock
```

Service Types:

| Component | Type |
|----------|------|
| Frontend | NodePort/LoadBalancer |
| Backend | ClusterIP |

---

# 3. Docker Image Workflow

## Build Images
```
cd backend
docker build -t support-backend:1.0 .

cd frontend
docker build -t support-frontend:1.1 .
```

## Tag Images
```
docker tag support-backend:1.0 docshishir/support-backend:1.0
docker tag support-frontend:1.1 docshishir/support-frontend:1.1
```

## Push to Docker Hub
```
docker push docshishir/support-backend:1.0
docker push docshishir/support-frontend:1.1
```

---

# 4. Minikube Deployment

## Install Tools
```
choco install minikube
choco install kubernetes-cli
choco install kubernetes-helm
```

## Start Minikube
```
minikube start --driver=docker
```

---

# 5. Helm Chart Setup

Structure:
```
support-automation/
  Chart.yaml
  values.yaml
  templates/
```

values.yaml:
```yaml
backend:
  image: "docshishir/support-backend:1.0"
  port: 8000

frontend:
  image: "docshishir/support-frontend:1.1"
  port: 8501
```

Install Helm chart:
```
helm install support-automation ./support-automation
```

---

# 6. Access the App in Minikube

Frontend:
```
minikube service support-frontend
```

Backend Swagger:
```
kubectl port-forward deployment/support-backend 8000:8000
http://localhost:8000/docs
```

---

# 7. Restarting Minikube

```
minikube start
helm upgrade support-automation ./support-automation
kubectl get pods
```

---

# 8. Debugging

Logs:
```
kubectl logs deployment/support-frontend
kubectl logs deployment/support-backend
```

DNS Test:
```
kubectl exec -it deployment/support-frontend -- sh
wget -qO- http://support-backend:8000/health
```

---

# 9. EKS Deployment

## Create Cluster
```
eksctl create cluster --name support-eks --region us-east-1 --nodes 3
```

## Connect kubectl
```
aws eks update-kubeconfig --name support-eks --region us-east-1
```

## Deploy via Helm
```
helm install support-automation ./support-automation
```

---

# 10. Production Env Variables

Use ConfigMaps + Secrets:
```yaml
envFrom:
  - configMapRef:
      name: support-config
  - secretRef:
      name: support-secrets
```

---

# End of Document
