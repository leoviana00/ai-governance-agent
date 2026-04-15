from pydantic import BaseModel
from typing import Optional


# ==========================================
# Métricas da mudança
# ==========================================

class ChangeMetrics(BaseModel):

    files_changed: int
    lines_added: int
    lines_removed: int
    modules_affected: int


# ==========================================
# Governança de mudança
# ==========================================

class Governance(BaseModel):

    change_type: Optional[str] = None
    semantic_commit: Optional[bool] = None
    branch_type: Optional[str] = None
    self_approved: Optional[bool] = None


# ==========================================
# Informações do Merge Request
# ==========================================

class MergeRequest(BaseModel):

    id: Optional[str] = None
    source_branch: Optional[str] = None
    target_branch: Optional[str] = None


# ==========================================
# Evento de mudança
# ==========================================

class ChangeEvent(BaseModel):

    commit_sha: Optional[str] = None

    # timestamps DORA
    commit_timestamp: Optional[str] = None

    change_metrics: ChangeMetrics

    governance: Optional[Governance] = None
    merge_request: Optional[MergeRequest] = None

    author: Optional[str] = None
    service: Optional[str] = None
    timestamp: Optional[str] = None


# ==========================================
# Feedback de incidente
# ==========================================

class IncidentFeedback(BaseModel):

    commit_sha: str
    incident: int
    deploy_timestamp: Optional[str] = None


# ==========================================
# Estrutura de resposta de risco
# ==========================================

class RiskPrediction(BaseModel):

    risk_probability: Optional[float]
    risk_level: Optional[str] = None
    risk_source: Optional[str] = None
    reasons: Optional[list] = None