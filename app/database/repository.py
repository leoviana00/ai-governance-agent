# app/database/repository.py

from app.database.connection import get_connection


# ==========================================
# Inicialização do banco
# ==========================================

def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS change_events (

            id SERIAL PRIMARY KEY,

            commit_sha VARCHAR(120),

            commit_timestamp TIMESTAMP,
            deploy_timestamp TIMESTAMP,

            author VARCHAR(120),

            files_changed INT,
            lines_added INT,
            lines_removed INT,
            modules_affected INT,

            change_type VARCHAR(30),
            semantic_commit BOOLEAN,
            branch_type VARCHAR(30),
            self_approved BOOLEAN,

            mr_id VARCHAR(50),
            mr_source_branch VARCHAR(120),
            mr_target_branch VARCHAR(120),

            incident INT DEFAULT 0,

            risk_probability FLOAT,
            risk_level VARCHAR(20),
            risk_source VARCHAR(20),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# ==========================================
# Reset do banco [Cansei de ficar limpando na mão] 
# ==========================================

def reset_database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE change_events RESTART IDENTITY")

    conn.commit()
    cur.close()
    conn.close()


# ==========================================
# Persistir evento
# ==========================================

def add_event(event, prediction=None):

    conn = get_connection()
    cur = conn.cursor()

    metrics = event.get("change_metrics") or {}
    governance = event.get("governance") or {}
    mr = event.get("merge_request") or {}

    commit_sha = event.get("commit_sha")
    commit_timestamp = event.get("commit_timestamp")

    # fallback obrigatório
    risk_probability = None
    risk_level = "UNKNOWN"
    risk_source = None

    if isinstance(prediction, dict):
        risk_probability = prediction.get("risk_probability")
        risk_level = prediction.get("risk_level") or "UNKNOWN"
        risk_source = prediction.get("risk_source")

    cur.execute("""
        INSERT INTO change_events
        (
            commit_sha,
            commit_timestamp,
            author,

            files_changed,
            lines_added,
            lines_removed,
            modules_affected,

            change_type,
            semantic_commit,
            branch_type,
            self_approved,

            mr_id,
            mr_source_branch,
            mr_target_branch,

            incident,
            risk_probability,
            risk_level,
            risk_source
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        commit_sha,
        commit_timestamp,
        event.get("author"),

        metrics.get("files_changed"),
        metrics.get("lines_added"),
        metrics.get("lines_removed"),
        metrics.get("modules_affected"),

        governance.get("change_type"),
        governance.get("semantic_commit"),
        governance.get("branch_type"),
        governance.get("self_approved"),

        mr.get("id"),
        mr.get("source_branch"),
        mr.get("target_branch"),

        event.get("incident", 0),
        risk_probability,
        risk_level,
        risk_source
    ))

    conn.commit()
    cur.close()
    conn.close()


# ==========================================
# Atualizar incidente + deploy
# ==========================================

def update_incident(commit_sha, incident, deploy_timestamp=None):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE change_events
        SET incident = %s,
            deploy_timestamp = %s
        WHERE commit_sha = %s
    """, (incident, deploy_timestamp, commit_sha))

    conn.commit()
    cur.close()
    conn.close()


# ==========================================
# Dataset para ML 
# ==========================================

def load_dataset():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            files_changed,
            lines_added,
            lines_removed,
            modules_affected,

            change_type,
            semantic_commit,
            branch_type,
            self_approved,

            incident
        FROM change_events
        WHERE files_changed IS NOT NULL
    """)

    rows = cur.fetchall()

    dataset = []

    for r in rows:

        # 🔥 PROTEÇÃO EXTRA (evita erro de tipo)
        if not isinstance(r, (list, tuple)) or len(r) < 9:
            continue

        dataset.append({
            "change_metrics": {
                "files_changed": int(r[0]) if r[0] is not None else 0,
                "lines_added": int(r[1]) if r[1] is not None else 0,
                "lines_removed": int(r[2]) if r[2] is not None else 0,
                "modules_affected": int(r[3]) if r[3] is not None else 0,
            },
            "governance": {
                "change_type": r[4],
                "semantic_commit": bool(r[5]) if r[5] is not None else False,
                "branch_type": r[6],
                "self_approved": bool(r[7]) if r[7] is not None else False,
            },
            "incident": int(r[8]) if r[8] is not None else 0
        })

    cur.close()
    conn.close()

    return dataset