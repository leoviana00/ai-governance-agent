# app/services/change_service.py

from app.ml.predictor import predict_risk
from app.database.repository import add_event

# ==========================================
# Processamento do evento de mudança
# ==========================================

def process_change_event(event: dict):
    """
    Fluxo principal:
    1. Prediz risco
    2. Persiste evento
    """

    # Predição de risco
    prediction = predict_risk(event)

    # Persistência no banco
    add_event(event, prediction)

    return prediction