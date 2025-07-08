from typing import Dict, Any
import numpy as np

class PreprocessingError(Exception):
    """Custom exception for preprocessing errors."""
    pass

def preprocess(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess the raw input data dictionary before feeding it into the model.
    
    Parameters:
    - data: dict with house features, keys correspond to the input JSON fields.
    
    Returns:
    - dict: cleaned and preprocessed data ready for model consumption.
    
    Raises:
    - PreprocessingError: if required fields are missing or invalid.
    """
    # Required fields and their types
    required_fields = {
        "area": int,
        "property-type": str,
        "rooms-number": int,
        "zip-code": int
    }
    
    # Check required fields existence and type
    for field, ftype in required_fields.items():
        if field not in data:
            raise PreprocessingError(f"Missing required field: '{field}'")
        if not isinstance(data[field], ftype):
            raise PreprocessingError(f"Field '{field}' must be of type {ftype.__name__}")
    
    # Validate 'property-type' values
    valid_property_types = {"APARTMENT", "HOUSE", "OTHERS"}
    if data["property-type"] not in valid_property_types:
        raise PreprocessingError(f"Invalid property-type '{data['property-type']}', must be one of {valid_property_types}")
    
    # Optional fields with defaults or cleaning
    processed = {}
    
    # Required fields (copied as-is)
    processed["area"] = data["area"]
    processed["property_type"] = data["property-type"]
    processed["rooms_number"] = data["rooms-number"]
    processed["zip_code"] = data["zip-code"]
    
    # Optional fields with defaults or fill NaN/None
    processed["land_area"] = data.get("land-area")
    processed["garden"] = data.get("garden", False)
    processed["garden_area"] = data.get("garden-area", 0)
    processed["equipped_kitchen"] = data.get("equipped-kitchen", False)
    processed["full_address"] = data.get("full-address", "")
    processed["swimming_pool"] = data.get("swimming-pool", False)
    processed["furnished"] = data.get("furnished", False)
    processed["open_fire"] = data.get("open-fire", False)
    processed["terrace"] = data.get("terrace", False)
    processed["terrace_area"] = data.get("terrace-area", 0)
    processed["facades_number"] = data.get("facades-number", 1)
    processed["building_state"] = data.get("building-state", "GOOD")
    
    # Additional validation or fill for optional fields
    # Convert None values to default where applicable
    for key in ["land_area", "garden_area", "terrace_area", "facades_number"]:
        if processed[key] is None:
            processed[key] = 0
    
    # Convert booleans if None (should already be covered)
    for key in ["garden", "equipped_kitchen", "swimming_pool", "furnished", "open_fire", "terrace"]:
        if processed[key] is None:
            processed[key] = False
    
    # Validate building_state values if given
    valid_building_states = {"NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"}
    if processed["building_state"] not in valid_building_states:
        raise PreprocessingError(f"Invalid building_state '{processed['building_state']}', must be one of {valid_building_states}")
    
    return processed

## It is aboout how to this
# from preprocessing.cleaning_data import preprocess, PreprocessingError

# def make_prediction(raw_data):
#     try:
#         cleaned_data = preprocess(raw_data)
#     except PreprocessingError as e:
#         # Raise or handle the error (e.g. return HTTP error)
#         raise ValueError(f"Preprocessing error: {str(e)}")
    
#     # Now cleaned_data is a dict with all fields ready for feature transformation
#     # Convert to model input format (e.g., feature vector) here or call another preprocessing step
#     X = transform_features(cleaned_data)
#     prediction = model.predict([X])[0]
#     return float(prediction)

