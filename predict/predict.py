import joblib
import pandas as pd
import os

def predict(preprocessed_data, model_path="model/Immo_ML.pkl"):
    """
    Predict house price using trained XGBoost model
    Takes preprocessed data as input and returns predicted price
    """
    try:
        # Load the model
        model = joblib.load(model_path)
        
        # Convert to DataFrame if it's a dict
        if isinstance(preprocessed_data, dict):
            data = pd.DataFrame([preprocessed_data])
        else:
            data = preprocessed_data.copy()
        
        # Debug: Print the data shape and columns
        print(f"Data shape: {data.shape}")
        print(f"Data columns: {list(data.columns)}")
        print(f"Data dtypes:\n{data.dtypes}")
        print(f"Data values:\n{data.iloc[0].to_dict()}")
        
        # Ensure the data has the correct column order expected by the model
        # This is crucial - the model expects features in a specific order
        expected_columns = [
            'bedroomCount', 'bathroomCount', 'habitableSurface', 'toiletCount',
            'terraceSurface', 'gardenSurface', 'province_encoded',
            'type_encoded', 'subtype_encoded', 'epcScore_encoded', 'hasAttic_encoded',
            'hasGarden_encoded', 'hasAirConditioning_encoded', 'hasArmoredDoor_encoded',
            'hasVisiophone_encoded', 'hasTerrace_encoded', 'hasOffice_encoded',
            'hasSwimmingPool_encoded', 'hasFireplace_encoded', 'hasBasement_encoded',
            'hasDressingRoom_encoded', 'hasDiningRoom_encoded', 'hasLift_encoded',
            'hasHeatPump_encoded', 'hasPhotovoltaicPanels_encoded', 'hasLivingRoom_encoded',
            'lat', 'lon'
        ]
        
        # Reorder columns to match expected order
        data = data[expected_columns]
        
        # Convert to numeric types
        for col in expected_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Fill any NaN values that might have been created
        data = data.fillna(0)
        
        print(f"Final data for prediction:\n{data.iloc[0].to_dict()}")
        
        # Make prediction
        prediction = model.predict(data)
        
        print(f"Raw prediction: {prediction}")
        
        # Return the prediction (single value)
        return float(prediction[0])
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_model(model_path="model/Immo_ML.pkl"):
    """
    Load the trained XGBoost model
    """
    try:
        # Try different possible paths
        possible_paths = [
            model_path,
            "Immo_ML.pkl",
            "../model/Immo_ML.pkl",
            "../../model/Immo_ML.pkl",
            "./model/Immo_ML.pkl"
        ]
        
        model = None
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Loading model from: {path}")
                model = joblib.load(path)
                break
        
        if model is None:
            print(f"Model file not found in any of these locations: {possible_paths}")
            return None
            
        return model
        
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return None