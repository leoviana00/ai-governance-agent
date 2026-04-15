# app/services/training_service.py

from app.ml.trainer import train_model
from app.ml.evaluator import evaluate_model
from app.database.repository import load_dataset


# ==========================================
# Serviço de treino
# ==========================================

def train_model_service():
    """
    Dispara treinamento do modelo
    """

    try:
        dataset = load_dataset()

        # ----------------------------------
        # Validação mínima
        # ----------------------------------
        if not dataset or len(dataset) < 10:
            return {
                "status": "not_enough_data",
                "records": len(dataset) if dataset else 0
            }

        # ----------------------------------
        # Treinamento
        # ----------------------------------
        train_model()

        return {
            "status": "model_trained",
            "records_used": len(dataset)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==========================================
# Serviço de avaliação
# ==========================================

def evaluate_model_service():
    """
    Avalia o modelo treinado
    """

    try:
        result = evaluate_model()

        # se evaluator já retorna status (ex: not_enough_data)
        if isinstance(result, dict) and result.get("status"):
            return result

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }