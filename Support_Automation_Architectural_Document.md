
# 🏛️ Support Automation Platform – Architectural Documentation  
_Comprehensive System, Deployment, Integration & Runtime Architecture_

---

# 📌 1. Introduction

This Architectural Document describes **how the Support Automation Platform is structured, deployed, scaled, and integrated** with AWS services and external systems. It is intended for:

- **Software Architects**
- **Platform Engineers**
- **Developers onboarding the project**
- **SRE / DevOps teams managing the deployment**
- **Stakeholders needing a systems overview**

This document complements the **Implementation Document** by focusing exclusively on the *architecture*, including:

- Logical architecture  
- Component architecture  
- Deployment architecture  
- Service interaction diagrams  
- Data flow diagrams  
- Backend integration architecture  
- EKS infrastructure architecture  

---

# 🧱 2. High-Level System Architecture

```
User (Browser)
   |
   v
Streamlit UI (Frontend)
   |
   v
FastAPI Backend (API Orchestrator)
   |
   +--------------+--------------+---------------+
   |              |              |               |
   v              v              v               v
AWS RDS       Neo4j DB     Elasticsearch   API Gateway → Lambda → Bedrock
```

### Component Purpose Summary

| Component | Purpose |
|----------|---------|
| **Streamlit UI** | Provides login, dashboard, module interfaces, bulk upload, results table, file download. |
| **FastAPI Backend** | Orchestrates requests, validates input, queries DBs, calls AI, returns normalized results. |
| **AWS RDS** | Stores Learning History, Hours, Completion Data. |
| **Neo4j** | Stores Work Profile graph (relationships, hierarchy, roles). |
| **Elasticsearch** | Stores Login Issues, Content search data, activity logs. |
| **API Gateway + Lambda + Bedrock** | Provides AI summaries, smart insights, generative responses. |

---

# ☸️ 3. EKS Deployment Architecture

```
                     Internet
                        |
                        v
                ┌──────────────────┐
                │ AWS ALB Ingress   │
                └──────────────────┘
                        |
          ┌────────────────────────────────┐
          │        Amazon EKS Cluster       │
          │                                  │
          │   ┌──────────────────────────┐   │
          │   │   Streamlit Deployment   │   │
          │   │  (2–4 replicas, HPA)     │   │
          │   └──────────────────────────┘   │
          │                |                  │
          │                v                  │
          │   ┌──────────────────────────┐   │
          │   │     FastAPI Deployment   │   │
          │   │   (3–6 replicas, HPA)    │   │
          │   └──────────────────────────┘   │
          └──────────────────────────────────┘
                       |
                       | VPC Access
           ┌───────────────┬───────────────┬─────────────────┐
           v               v               v                 v
       AWS RDS        Neo4j Aura     Elasticsearch   API Gateway → Lambda → Bedrock
```

### Key Architecture Notes

- **ALB → Streamlit only** is exposed publicly.
- Streamlit calls FastAPI internally via `ClusterIP` service.
- FastAPI Pods run with **IAM Roles for Service Accounts (IRSA)** for AWS access.
- Pods scale using **Horizontal Pod Autoscalers (HPA)**.
- All DBs run in **private subnets**, accessible only from EKS.

---

# 🧩 4. Internal Component Architecture

## 4.1 Frontend (Streamlit)

```
Login.py → Home.py → Module Pages → API Client → FastAPI
```

Streamlit Components:
- Pages for each module  
- Reusable table renderer  
- Excel uploader component  
- Auth utilities  

---

## 4.2 Backend (FastAPI)

```
Routers → Services → Validators → DB Clients → External Systems
```

FastAPI Layers:

### Router Layer  
Handles endpoint exposure:
```
/auth/login  
/learning-history  
/learning-hours  
/login-issue  
/content-completion  
/work-profile  
/analytics  
```

### Service Layer  
Core business logic:
```
- Dummy mode (JSON)
- Real mode (RDS, Neo4j, Elasticsearch)
- Aggregation logic
- AI calls to Bedrock
```

### Data Access Layer
```
db/rds_client.py  
db/neo4j_client.py  
db/es_client.py  
bedrock/bedrock_client.py  
```

### Validation Layer  
Ensures:
- User IDs valid
- Excel contains required columns  
- Requests formatted correctly  

### Configuration Layer  
```
core/settings.py
core/config.py
```
Keeps:
- Environment settings
- Paths
- Feature toggles (dummy vs real mode)

---

# 🔄 5. Detailed Data Flow

## 5.1 Login Flow

1. User enters credentials in Streamlit.
2. Streamlit POSTs to FastAPI `/auth/login`.
3. FastAPI validates using hardcoded or DB rules.
4. Token returned → session stored in Streamlit.
5. Dashboard loads.

---

## 5.2 Single User Lookup (Any Module)

```
UI → API → Service → Validator → Dummy/Real Backend → Response → UI
```

Detailed Breakdown:

### UI Layer
- User enters WID/UserID.
- Clicks button → API request triggered.

### API Layer
- Router receives `GET /module/single/{user_id}`.
- Calls corresponding service.

### Service Layer
- Validates input.
- If dummy mode: pull JSON.
- If real mode: query DB (RDS, Neo4j, or Elasticsearch).

### Response Layer
- Data normalized into response model.
- Returned to UI.
- Rendered in table or downloadable CSV.

---

## 5.3 Bulk Upload Flow

```
UI Excel Upload → API Bulk Endpoint → Read Rows → For Each User → Service → Aggregate → Return
```

### Key Behavior:
- API efficiently loops through each ID.
- Each call routed through service layer.
- Results aggregated and returned as list of objects.

---

## 5.4 AI Summary (Bedrock)

1. FastAPI forms prompt (context = user history/hours/etc.)
2. Sends JSON payload to API Gateway.
3. Lambda receives → Calls Bedrock model.
4. Model returns text summary.
5. Lambda returns JSON back to FastAPI.
6. FastAPI adds `ai_summary` field to response.

---

# 🗂 6. Folder Structure With Architectural Purpose

```
backend/
│
├── main.py                 → Entry point (FastAPI instance)
│
├── routers/                → API endpoints for each module
│   ├── learning_history_router.py
│   ├── ...
│
├── services/               → Business logic (dummy + real)
│   ├── learning_history_service.py
│   ├── ...
│
├── db/                     → Data integration layer
│   ├── rds_client.py
│   ├── neo4j_client.py
│   └── es_client.py
│
├── bedrock/                → AI integration layer
│   └── bedrock_client.py
│
├── validators/             → Input validation components
│   └── ...
│
├── core/                   → Global app config
│   ├── settings.py
│   └── config.py
│
└── data/                   → Dummy JSON files
```

```
frontend/
│
├── Login.py                → Login page & authentication
├── Home.py                 → Dashboard tiles, logout button
│
├── pages/                  → UI modules
│   ├── LearningHistory.py
│   ├── ...
│
├── utils/                  → API client, auth utilities
│   ├── api_client.py
│   ├── auth_utils.py
│
└── components/             → Reusable widgets
    ├── uploader.py
    └── table_renderer.py
```

```
k8s/
│
├── base/                   → Default manifests
│   ├── deployments
│   ├── services
│   ├── ingress
│   ├── configmap
│   └── secrets
│
└── overlays/               → Dev / QA / Prod
```

---

# 🔐 7. Security Architecture

## 7.1 Kubernetes Security

- FastAPI pod uses **IRSA** to access AWS services.
- Streamlit pod is publicly exposed via ALB.
- FastAPI pod is internal-only (`ClusterIP`).
- Secrets stored in **Kubernetes Secrets**.
- Configurations stored in **ConfigMaps**.
- TLS termination at ALB.

## 7.2 Data Security

- RDS — Private subnet, SG restricted to EKS nodes.
- Neo4j — Secured with authentication + limited IP access.
- Elasticsearch — IAM-signed requests if AWS OpenSearch.
- Bedrock — access controlled by IAM policy for Lambda.

---

# ⚙️ 8. Scalability Architecture

## Horizontal Scaling
- Streamlit: 2–4 replicas (UI load)
- FastAPI: 3–6 replicas (API load)
- Autoscaling based on:
  - CPU usage
  - Memory usage
  - Request latency

## Stateless Architecture
- Both UI and API are stateless → easy scaling.

## Storage Scaling
- RDS uses Multi-AZ failover.
- Elasticsearch auto-scales horizontally with domain.
- Neo4j Aura auto-scales cluster.

---

# 🛠 9. Observability Architecture

## Logging
- FastAPI logs streamed to CloudWatch.
- Streamlit logs captured via Kubernetes logs.

## Metrics
- Prometheus Operator (optional)
- HPA metrics for scaling

## Alerts
- CPU/memory saturation
- Pod restart loops
- RDS connection failures
- Bedrock API failures

---

# 🎯 10. Summary

This architectural document covers:

- System architecture  
- Deployment architecture (EKS)  
- Component responsibilities  
- Data flows  
- AI integration  
- Kubernetes patterns  
- Scalability and observability  
- Security architecture  

It complements the Implementation Document to give **complete clarity** on how the system works at every layer.

