# app/ml/trainer.py

import os
import pickle

from sklearn.ensemble import RandomForestClassifier

from app.database.repository import load_dataset
from app.features.feature_builder import build_features

MODEL_FILE = "storage/model.pkl"


def train_model():

    # ----------------------------------
    # Carregar dataset
    # ----------------------------------
    dataset = load_dataset()

    # 🔥 DEBUG (pode remover depois)
    print("DEBUG dataset type:", type(dataset))
    if dataset:
        print("DEBUG dataset[0] type:", type(dataset[0]))

    # ----------------------------------
    # Construir features (CORRETO)
    # ----------------------------------
    X, y = build_features(dataset)  # ✅ SEMPRE dataset inteiro

    # ----------------------------------
    # Validação
    # ----------------------------------
    if not X or not y:
        raise ValueError("Dataset inválido após feature engineering")

    # ----------------------------------
    # Treinar modelo
    # ----------------------------------
    model = RandomForestClassifier(n_estimators=100)

    model.fit(X, y)

    # ----------------------------------
    # Salvar modelo
    # ----------------------------------
    os.makedirs("storage", exist_ok=True)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    return model