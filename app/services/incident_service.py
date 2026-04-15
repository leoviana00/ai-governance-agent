# app/services/incident_service.py

from app.database.repository import update_incident

# ==========================================
# Processamento do feedback de incidente
# ==========================================

def process_incident_feedback(data: dict):
    """
    Atualiza:
    - incidente
    - deploy timestamp
    """

    update_incident(
        data["commit_sha"],
        data["incident"],
        data.get("deploy_timestamp")
    )

    return {"status": "updated"}