# From CI/CD to Change Intelligence  
## Applying AI and DORA Metrics to Govern Deployments

---

## Overview

Este projeto implementa uma plataforma completa de **Change Intelligence**, combinando:

- ⚙️ CI/CD (Jenkins)
- 🤖 Machine Learning (AI Agent)
- 📊 Métricas DORA
- 🛡️ Governança de mudanças
- 📈 Observabilidade (Grafana)

O objetivo é transformar deploys em **insights inteligentes**, permitindo:

- reduzir incidentes  
- melhorar governança  
- aumentar previsibilidade de mudanças  

---

## Problema

Times de engenharia frequentemente:

- deployam sem visibilidade de risco  
- não correlacionam mudanças com incidentes  
- não possuem governança estruturada  
- não utilizam dados para melhorar entrega  

---

## Solução

Criar um pipeline que:

```console
Captura → Analisa → Aprende → Visualiza → Governa
```


---

## Arquitetura

```console
             ┌────────────────────┐
             │     Developer       │
             └─────────┬──────────┘
                       │ commit
                       ▼
             ┌────────────────────┐
             │      Jenkins        │
             │   CI/CD Pipeline    │
             └─────────┬──────────┘
                       │
    ┌──────────────────┼──────────────────┐
    ▼                                     ▼
┌──────────────────┐ ┌────────────────────┐
│ Change Telemetry │ │ Deploy Application │
└─────────┬────────┘ └─────────┬──────────┘
          │                    │
          ▼                    ▼
┌────────────────────────────────────────────────┐
│ AI Agent (FastAPI)                             │
│ - Risk Prediction                              │
│ - Governance Analysis                          │
│ - Dataset Storage                              │
└───────────────┬────────────────────────────────┘
                ▼
┌────────────────────┐
│ PostgreSQL         │
│ change_events      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Grafana            │
│ Observability Layer│
└────────────────────┘
```


---

## Stack Tecnológica

| Camada            | Tecnologia           |
|------------------|---------------------|
| CI/CD            | Jenkins             |
| Backend AI       | Python + FastAPI    |
| Machine Learning | Scikit-learn        |
| Banco de Dados   | PostgreSQL          |
| Observabilidade  | Grafana             |
| Containerização  | Docker              |

---

## Fluxo do Sistema

1. Developer faz commit  
2. Jenkins executa pipeline  
3. Pipeline coleta métricas de mudança  
4. Evento enviado para AI Agent (`/change-event`)  
5. AI calcula risco  
6. Deploy é realizado  
7. Feedback enviado (`/incident-feedback`)  
8. Dados persistidos  
9. Modelo treinado  
10. Grafana exibe métricas  

---

## AI Agent

Responsável por:

- Classificar risco de deploy  
- Avaliar governança  
- Armazenar histórico  
- Treinar modelo de ML  

---

## Machine Learning

### Features utilizadas

- files_changed  
- lines_added  
- lines_removed  
- modules_affected  
- semantic_commit  
- self_approved  
- branch_type  
- change_type  

---

### Output

- `risk_probability`  
- `risk_level` (LOW / MEDIUM / HIGH)  

---

## Métricas DORA

### ✔ Lead Time

Tempo entre commit e deploy  

---

### ✔ Deployment Frequency

Quantidade de deploys por período  

---

### ✔ Change Failure Rate

% de deploys com incidente  

---

## Governança de Mudanças

### Métricas

- Semantic Commit Rate  
- Self Approval Rate  
- Governance Violation Rate  
- Governance Score  

---

### Exemplos de Violação

- commit fora do padrão  
- auto aprovação  
- mudança de alto risco  

---

## Dashboards (Grafana)

### 🔹 Delivery Performance

- Lead Time  
- Deployment Frequency  
- Failure Rate  

---

### 🔹 Governance

- Semantic Commit %
- Self Approval %
- Violation Rate
- Governance Score

---

### 🔹 Risk Intelligence

- Risk distribution  
- Risk vs Incident  
- Prediction accuracy  

---

### 🔹 Change Intelligence

- Commit vs Incident  
- Approval vs Incident  
- Risk vs Failure  

---

## Principais Endpoints

| Endpoint                  | Descrição                    |
|--------------------------|------------------------------|
| POST /change-event       | registra mudança             |
| POST /incident-feedback  | registra incidente           |
| POST /predict            | prediz risco                 |
| POST /train              | treina modelo                |
| GET /model/evaluate      | avalia modelo                |
| POST /dataset/reset      | limpa dataset                |
| POST /dataset/generate-demo | gera dados fake          |

---

## Execução

### 🔹 Subir ambiente

```bash
docker compose up -d
```

## 🔹 Acessos

| Serviço  | URL                                            |
| -------- | ---------------------------------------------- |
| AI Agent | [http://localhost:8000](http://localhost:8000) |


## Exemplos de Insights
- Deploys auto-aprovados geram mais incidentes
- Commits fora do padrão aumentam risco
- Mudanças de alto risco impactam falhas
- Governança reduz instabilidade

## Conceitos Aplicados
- DORA Metrics
- DevOps
- AIOps
- Observabilidade
- Engenharia de Confiabilidade (SRE)
- Machine Learning aplicado a operações

## Diferenciais
- Integração completa CI/CD + AI + Observabilidade
- Modelo preditivo de risco de deploy
- Governança baseada em dados
- Dashboards acionáveis
- Simulação de cenários reais