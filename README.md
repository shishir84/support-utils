
# 📘 Support Automation Platform
### Unified L&D Support, Issue Resolution & Analytics Platform — Deployable on AWS EKS

## 🚀 Overview
Support Automation is a full-stack platform built using **Streamlit (UI)** and **FastAPI (Backend)**, supporting:

- Learning History  
- Learning Hours  
- Login Issues  
- Content Completion  
- Work Profile  
- Learning Analytics Table  
- AI insights via **Amazon Bedrock** (API Gateway → Lambda)

Supports both:
- **Dummy mode** (JSON files for development)
- **Production mode** (RDS, Neo4j, Elasticsearch, Bedrock)

Runs fully inside **Amazon EKS** with ConfigMaps, Secrets, ALB Ingress, and autoscaling support.

---

# 🧱 1. Architecture (EKS Deployment)

## High-Level System Architecture

```
Internet
   |
AWS ALB (Ingress)
   |
-------------------------------------
|                                   |
Streamlit UI (Pod)  <-->  FastAPI Backend (Pod)
|                                   |
|                                   |
|         -----------------------------
|         |            |             |
AWS RDS   Neo4j Aura   Elasticsearch   API Gateway → Lambda → Bedrock
```

---

# 🧩 2. Project Folder Structure

```
support-automation/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── validators/
│   ├── core/
│   │   ├── settings.py
│   │   └── config.py
│   ├── db/
│   │   ├── rds_client.py
│   │   ├── neo4j_client.py
│   │   └── es_client.py
│   ├── bedrock/
│   │   └── bedrock_client.py
│   └── data/
│
├── frontend/
│   ├── Login.py
│   ├── Home.py
│   ├── pages/
│   ├── utils/
│   └── components/
│
├── k8s/
│   ├── base/
│   └── overlays/
│
├── README.md
└── requirements.txt
```

---

# 🐳 3. Dockerfiles

## Backend (FastAPI)

```
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Frontend (Streamlit)

```
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "Login.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

---

# ⚙️ 4. Kubernetes (EKS)

## ConfigMap

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: support-automation-config
data:
  USE_DUMMY_DATA: "0"
  RDS_HOST: "your-rds-endpoint"
  RDS_DB: "learning"
  ES_ENDPOINT: "your-es-endpoint"
  NEO4J_URI: "bolt://neo4j.url:7687"
  BEDROCK_API_URL: "your-api-gw-url"
```

## Secrets

```
apiVersion: v1
kind: Secret
metadata:
  name: support-automation-secrets
type: Opaque
data:
  RDS_USER: <base64>
  RDS_PASSWORD: <base64>
  NEO4J_USER: <base64>
  NEO4J_PASSWORD: <base64>
  BEDROCK_API_KEY: <base64>
```

## FastAPI Deployment

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: support-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: support-api
  template:
    metadata:
      labels:
        app: support-api
    spec:
      containers:
        - name: fastapi
          image: <ECR>/support-backend:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: support-automation-config
            - secretRef:
                name: support-automation-secrets
```

## Streamlit Deployment

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: support-ui
spec:
  replicas: 2
  selector:
    matchLabels:
      app: support-ui
  template:
    metadata:
      labels:
        app: support-ui
    spec:
      containers:
        - name: streamlit
          image: <ECR>/support-frontend:latest
          ports:
            - containerPort: 8501
          env:
            - name: API_URL
              value: "http://support-api:8000"
```

---

# 🔌 5. API Overview

```
/auth/login
/learning-history/single/{id}
/learning-hours/single/{id}
/login-issue/single/{id}
/content-completion/single/{id}
/work-profile/single/{id}
/analytics/single/{id}
```

All endpoints support bulk POST versions also.

---

# 🔐 6. Environment Variables

```
USE_DUMMY_DATA=1 or 0
RDS_HOST=
RDS_USER=
RDS_PASSWORD=
NEO4J_URI=
NEO4J_USER=
NEO4J_PASSWORD=
ES_ENDPOINT=
BEDROCK_API_URL=
BEDROCK_API_KEY=
```

---

# 🚀 7. How to Deploy

## 1. Build Docker Images

```
docker build -t support-backend backend/
docker build -t support-frontend frontend/
```

## 2. Push to ECR

```
docker push <ECR>/support-backend
docker push <ECR>/support-frontend
```

## 3. Deploy to EKS

```
kubectl apply -k k8s/overlays/prod
```

---

# 🎯 Summary

✔ UI + API fully containerized  
✔ Production-ready for EKS  
✔ Dummy + real data toggle  
✔ Supports RDS, Neo4j, Elasticsearch  
✔ Bedrock integrated via Lambda  
✔ Modular, scalable architecture  

---

# 🙌 Contributors Guide

1. Start backend → test via Swagger  
2. Run frontend → test API calls  
3. For Kubernetes changes → update overlays  
4. Always commit Dockerfile + k8s manifests updates  

---

# End of Documentation
