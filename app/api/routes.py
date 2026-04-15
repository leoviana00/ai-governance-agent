# app/api/routes.py

from fastapi import APIRouter

# Services
from app.services.change_service import process_change_event
from app.services.incident_service import process_incident_feedback
from app.services.training_service import train_model_service, evaluate_model_service
from app.services.dataset_service import generate_demo_dataset_service, reset_dataset_service

# ML
from app.ml.predictor import predict_risk

# Schemas (validação forte)
from app.models.schemas import ChangeEvent, IncidentFeedback

router = APIRouter(prefix="", tags=["AI Agent"])


# ==========================================
# Health Check
# ==========================================

@router.get("/health")
def health():
    return {"status": "ok"}


# ==========================================
# Endpoint: Change Event
# ==========================================

@router.post("/change-event")
def change_event(event: ChangeEvent):
    """
    Recebe evento de mudança vindo do pipeline
    - valida estrutura automaticamente (Pydantic)
    - calcula risco
    - persiste no banco
    """
    return process_change_event(event.dict())


# ==========================================
# Endpoint: Predict (🔥 CORREÇÃO DO PIPELINE)
# ==========================================

@router.post("/predict")
def predict(event: ChangeEvent):
    """
    Retorna apenas a predição de risco (sem persistência)
    Usado para decisão no pipeline (Jenkins)
    """
    return predict_risk(event.dict())


# ==========================================
# Endpoint: Incident Feedback
# ==========================================

@router.post("/incident-feedback")
def incident_feedback(data: IncidentFeedback):
    """
    Recebe feedback pós deploy
    - marca incidente
    - atualiza deploy timestamp
    """
    return process_incident_feedback(data.dict())


# ==========================================
# Endpoint: Treinar modelo
# ==========================================

@router.post("/train")
def train():
    """
    Treina o modelo de Machine Learning
    """
    return train_model_service()


# ==========================================
# Endpoint: Avaliação do modelo
# ==========================================

@router.get("/model/evaluate")
def evaluate_model():
    """
    Avalia o modelo de ML com base no dataset atual
    """
    return evaluate_model_service()


# ==========================================
# Endpoint: Gerar dados Fake
# ==========================================

@router.post("/dataset/generate-demo")
def generate_demo_dataset(events: int = 500):
    """
    Gera dataset fake balanceado para testes
    """
    return generate_demo_dataset_service(events)


# ==========================================
# Endpoint: Reset dos dados
# ==========================================

@router.post("/dataset/reset")
def reset_dataset():
    """
    Limpa todos os dados do banco
    """
    return reset_dataset_service()