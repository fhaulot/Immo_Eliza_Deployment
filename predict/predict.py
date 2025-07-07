import joblib
import os
import pandas as pd
from preprocessing.cleaning_data import preprocess

# Load model
model = joblib.load(os.path.join("model", "model.pkl"))

def make_prediction(raw_input: dict) -> float:
    """
    Preprocess the input dict and predict the property price.
    """
    try:
        preprocessed_df = preprocess(raw_input)
        prediction = model.predict(preprocessed_df)
        return float(prediction[0])
    except Exception as e:
        raise ValueError(f"Prediction failed: {e}")