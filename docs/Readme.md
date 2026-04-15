## Estrutura do projeto

```console
ai-agent/
│
├── app/
│   ├── main.py                     # entrypoint (FastAPI app)
│   │
│   ├── api/                        # camada HTTP (rotas)
│   │   ├── routes.py
│   │   ├── deps.py                 # dependências (opcional)
│   │
│   ├── core/                       # configs globais
│   │   ├── config.py
│   │   ├── settings.py
│   │
│   ├── models/                     # contratos da API (Pydantic)
│   │   ├── schemas.py
│   │
│   ├── services/                   # regras de negócio
│   │   ├── change_service.py       # orquestra change-event
│   │   ├── incident_service.py     # orquestra feedback
│   │   ├── training_service.py     # treino do modelo
│   │
│   ├── ml/                         # camada de machine learning
│   │   ├── predictor.py            # predição
│   │   ├── trainer.py              # treino
│   │   ├── model_loader.py         # load/save modelo
│   │
│   ├── features/                   # engenharia de features (CRÍTICO)
│   │   ├── feature_builder.py
│   │
│   ├── database/
│   │   ├── connection.py           # conexão DB
│   │   ├── repository.py           # queries SQL
│   │
│   ├── domain/                     # regras puras (opcional, nível avançado)
│   │   ├── risk_rules.py           # regras heurísticas
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── helpers.py
│
├── storage/
│   ├── model.pkl                   # modelo treinado
│
├── scripts/
│   ├── generate_dataset.py         # geração fake (opcional)
│
├── tests/                          # testes (opcional mas forte)
│   ├── test_predictor.py
│   ├── test_api.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
```

## 🧠 📐 Arquitetura por camadas

API → Services → Features → ML → Repository → Database

## 🔥 Fluxo completo

```console
POST /change-event
        ↓
api/routes.py
        ↓
services/change_service.py
        ↓
features/feature_builder.py
        ↓
ml/predictor.py
        ↓
database/repository.py
```