import joblib
import os

# Load the model once when the module is imported to avoid loading on every request
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model", "model.joblib")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")

def predict(preprocessed_data):
    """
    Predict the price of a house given preprocessed input features.
    
    Parameters:
    - preprocessed_data: dict or list-like, preprocessed features ready for model input.
    
    Returns:
    - float: predicted price
    """
    # Convert dict to ordered list/vector if needed by the model
    # Here we assume model expects a list of feature values in the right order
    if isinstance(preprocessed_data, dict):
        # Define the order of features expected by the model (must match training!)
        feature_order = [
            "area",
            "rooms_number",
            "zip_code",
            "property_type",
            "garden",
            "terrace",
            # Add more features if your model uses them, in exact order
        ]
        
        try:
            features = [preprocessed_data[feature] for feature in feature_order]
        except KeyError as e:
            raise ValueError(f"Missing feature for prediction: {e}")
    else:
        # Assume it's already a list or array-like
        features = preprocessed_data

    # Model expects a 2D array: one sample with N features
    prediction = model.predict([features])[0]
    
    return float(prediction)
