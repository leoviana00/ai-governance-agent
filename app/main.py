# app/main.py

from fastapi import FastAPI
from app.api.routes import router
from app.database.repository import init_db

# ==========================================
# Criação da aplicação FastAPI
# ==========================================

app = FastAPI(
    title="AI Agent - Change Intelligence",
    description="Service for risk prediction, governance analysis and DORA metrics",
    version="1.0.0"
)

# ==========================================
# Evento de inicialização (startup)
# ==========================================

@app.on_event("startup")
def on_startup():
    """
    Executado ao subir o serviço

    - garante que a tabela existe
    - evita erro em ambiente novo
    """
    init_db()

# ==========================================
# Registro das rotas
# ==========================================

app.include_router(router)

# ==========================================
# Health check simples (root)
# ==========================================

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "ai-agent",
        "version": "1.0.0"
    }

# ==========================================
# Health check padrão (observabilidade)
# ==========================================

@app.get("/health")
def health():
    return {"status": "ok"}