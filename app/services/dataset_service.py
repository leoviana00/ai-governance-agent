# app/services/dataset_service.py

import random
import uuid
from datetime import datetime, timedelta

from app.database.repository import add_event, update_incident, reset_database
from app.ml.predictor import predict_risk


# ==========================================
# Reset
# ==========================================

def reset_dataset_service():

    reset_database()

    return {
        "status": "database reset"
    }


# ==========================================
# Dataset balanceado
# ==========================================

def generate_demo_dataset_service(events: int = 500):

    authors = ["Leo", "Ana", "José", "Denner"]
    change_types = ["feat", "fix", "refactor"]
    branch_types = ["feature", "hotfix"]

    for _ in range(events):

        commit_sha = str(uuid.uuid4())

        # ----------------------------------
        # TEMPO
        # ----------------------------------

        commit_time = datetime.utcnow() - timedelta(
            minutes=random.randint(10, 10000)
        )

        deploy_time = commit_time + timedelta(
            minutes=random.randint(2, 180)
        )

        # ----------------------------------
        # DISTRIBUIÇÃO CONTROLADA
        # ----------------------------------

        risk_bucket = random.choices(
            ["LOW", "MEDIUM", "HIGH"],
            weights=[0.5, 0.3, 0.2]
        )[0]

        # ----------------------------------
        # MÉTRICAS POR PERFIL
        # ----------------------------------

        if risk_bucket == "LOW":

            metrics = {
                "files_changed": random.randint(1, 2),
                "lines_added": random.randint(10, 80),
                "lines_removed": random.randint(0, 40),
                "modules_affected": 1
            }

        elif risk_bucket == "MEDIUM":

            metrics = {
                "files_changed": random.randint(3, 6),
                "lines_added": random.randint(80, 300),
                "lines_removed": random.randint(40, 150),
                "modules_affected": random.randint(2, 3)
            }

        else:

            metrics = {
                "files_changed": random.randint(7, 12),
                "lines_added": random.randint(300, 1200),
                "lines_removed": random.randint(150, 600),
                "modules_affected": random.randint(3, 6)
            }

        # ----------------------------------
        # GOVERNANÇA
        # ----------------------------------

        governance = {
            "change_type": random.choice(change_types),
            "semantic_commit": random.random() > 0.1,
            "branch_type": random.choice(branch_types),
            "self_approved": random.random() < 0.2
        }

        event = {
            "commit_sha": commit_sha,
            "commit_timestamp": commit_time.isoformat(),
            "author": random.choice(authors),
            "change_metrics": metrics,
            "governance": governance
        }

        # ----------------------------------
        # PREDIÇÃO
        # ----------------------------------

        prediction = predict_risk(event)

        if not prediction:
            prediction = {
                "risk_probability": None,
                "risk_level": "UNKNOWN",
                "risk_source": "fallback"
            }

        # ----------------------------------
        # SALVAR
        # ----------------------------------

        add_event(event, prediction)

        # ----------------------------------
        # INCIDENTE COERENTE
        # ----------------------------------

        risk_level = prediction.get("risk_level")

        if risk_level == "HIGH":
            incident = 1 if random.random() < 0.6 else 0

        elif risk_level == "MEDIUM":
            incident = 1 if random.random() < 0.25 else 0

        elif risk_level == "LOW":
            incident = 1 if random.random() < 0.05 else 0

        else:
            incident = 1 if random.random() < 0.1 else 0

        update_incident(
            commit_sha,
            incident,
            deploy_time.isoformat()
        )

    return {
        "status": "dataset generated",
        "events": events
    }