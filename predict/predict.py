import joblib
import pandas as pd
from preprocessing.cleaning_data import preprocess

# Charger le modèle et les colonnes attendues
model = joblib.load("model/model.pkl")
expected_columns = joblib.load("model/feature_columns.pkl")

def predict(input_dict: dict) -> float:
    # Appliquer preprocessing
    df = preprocess(input_dict)

    # Réindexer les colonnes pour qu’elles correspondent au modèle
    df = df.reindex(columns=expected_columns, fill_value=0)

    # Prédire
    prediction = model.predict(df)
    return float(prediction[0])