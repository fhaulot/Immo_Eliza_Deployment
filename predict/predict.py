import joblib
from preprocessing.cleaning_data import preprocess  

model = joblib.load("model/model.pkl")
expected_columns = joblib.load("model/feature_columns.pkl")
"""
We load the model and the expected columns from the saved files.
"""

def predict(input_dict: dict) -> float:
    
    df = preprocess(input_dict)
    """
    We apply the preprocessing function to the input dictionnary
    """

    df = df.reindex(columns=expected_columns, fill_value=0)
    """
    We apply the selected columns to the cleaned input data.
    """
    prediction = model.predict(df)
    return float(prediction[0])
    """
    We apply the prediction model
    """
