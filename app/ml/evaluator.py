from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.database.repository import load_dataset
from app.features.feature_builder import build_features
from app.ml.predictor import load_model


def evaluate_model():

    dataset = load_dataset()

    # -----------------------------
    # Validação mínima de dataset
    # -----------------------------
    if not dataset or len(dataset) < 10:
        return {
            "status": "not_enough_data",
            "records": len(dataset) if dataset else 0
        }

    X, y = build_features(dataset)

    # Proteção extra
    if not X or not y:
        return {
            "status": "invalid_dataset_after_processing"
        }

    model = load_model()

    if not model:
        return {
            "status": "model_not_trained"
        }

    # -----------------------------
    # Predição
    # -----------------------------
    y_pred = model.predict(X)

    # -----------------------------
    # Métricas principais
    # -----------------------------
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)

    # -----------------------------
    # Matriz de confusão
    # -----------------------------
    cm = confusion_matrix(y, y_pred).tolist()

    # -----------------------------
    # Classification report
    # -----------------------------
    report = classification_report(y, y_pred, output_dict=True)

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),  # 🔥 NOVO (importante)
        "confusion_matrix": cm,
        "classification_report": report,
        "total_samples": len(y)  # 🔥 útil no Grafana
    }