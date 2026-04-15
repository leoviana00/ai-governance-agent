# app/ml/predictor.py

import pickle
import os

MODEL_FILE = "storage/model.pkl"


# ==========================================
# Carregar modelo
# ==========================================

def load_model():

    if not os.path.exists(MODEL_FILE):
        return None

    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)


# ==========================================
# Classificação de risco
# ==========================================

def classify_risk(prob):

    if prob is None:
        return "UNKNOWN"

    if prob < 0.35:
        return "LOW"

    if prob < 0.65:
        return "MEDIUM"

    return "HIGH"


# ==========================================
# Regras heurísticas
# ==========================================

def rule_based_risk(metrics):

    files_changed = metrics["files_changed"]
    lines_added = metrics["lines_added"]
    modules = metrics["modules_affected"]

    reasons = []

    # LOW
    if files_changed <= 2 and lines_added <= 50 and modules <= 1:
        reasons.append("small_change")
        return 0.1, reasons

    # MEDIUM
    if 2 <= modules <= 3:
        reasons.append("moderate_scope")
        return 0.5, reasons

    if 80 <= lines_added < 300:
        reasons.append("moderate_code_change")
        return 0.55, reasons

    # HIGH
    if modules >= 4:
        reasons.append("many_modules_affected")
        return 0.85, reasons

    if lines_added >= 500:
        reasons.append("large_code_change")
        return 0.8, reasons

    return None, reasons


# ==========================================
# Predição principal
# ==========================================

def predict_risk(event):

    metrics = event.get("change_metrics", {})
    governance = event.get("governance") or {}

    reasons = []

    # --------------------------------------
    # 1 - regras
    # --------------------------------------

    rule_probability, rule_reasons = rule_based_risk(metrics)

    if rule_probability is not None:

        return {
            "risk_probability": rule_probability,
            "risk_level": classify_risk(rule_probability),
            "risk_source": "rules",
            "reasons": rule_reasons
        }

    # --------------------------------------
    # 2 - modelo ML
    # --------------------------------------

    model = load_model()

    # 🔥 fallback se modelo não existir
    if not model:

        fallback_prob = 0.5  # MEDIUM padrão

        return {
            "risk_probability": fallback_prob,
            "risk_level": classify_risk(fallback_prob),
            "risk_source": "fallback_no_model",
            "reasons": ["no_model_default"]
        }

    # --------------------------------------
    # FEATURES BASE
    # --------------------------------------

    files_changed = metrics.get("files_changed", 0)
    lines_added = metrics.get("lines_added", 0)
    lines_removed = metrics.get("lines_removed", 0)
    modules_affected = metrics.get("modules_affected", 0)

    # --------------------------------------
    # GOVERNANÇA
    # --------------------------------------

    semantic_commit = 1 if governance.get("semantic_commit") else 0
    self_approved = 1 if governance.get("self_approved") else 0

    if self_approved:
        reasons.append("self_approved")

    if governance.get("semantic_commit") is False:
        reasons.append("non_semantic_commit")

    # --------------------------------------
    # CHANGE TYPE
    # --------------------------------------

    change_type = governance.get("change_type")

    is_feat = 1 if change_type == "feat" else 0
    is_fix = 1 if change_type == "fix" else 0
    is_refactor = 1 if change_type == "refactor" else 0

    # --------------------------------------
    # BRANCH TYPE
    # --------------------------------------

    branch_type = governance.get("branch_type")

    is_hotfix = 1 if branch_type == "hotfix" else 0
    is_feature_branch = 1 if branch_type == "feature" else 0

    # --------------------------------------
    # VETOR FINAL (11 FEATURES)
    # --------------------------------------

    X = [[
        files_changed,
        lines_added,
        lines_removed,
        modules_affected,

        semantic_commit,
        self_approved,

        is_feat,
        is_fix,
        is_refactor,

        is_hotfix,
        is_feature_branch
    ]]

    probability = model.predict_proba(X)[0][1]

    # --------------------------------------
    # AJUSTE FINO POR GOVERNANÇA
    # --------------------------------------

    if self_approved:
        probability += 0.05

    if governance.get("semantic_commit") is False:
        probability += 0.03

    probability = min(probability, 1.0)

    return {
        "risk_probability": float(probability),
        "risk_level": classify_risk(probability),
        "risk_source": "ml",
        "reasons": reasons
    }