from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import joblib
from typing import Union, Literal, Optional
import predict
from fastapi import HTTPException
import predict

# Set port to the env variable PORT to make it easy to choose the port on the server
# If the Port env variable is not set, use port 8000
PORT = os.environ.get("PORT", 8000)
app = FastAPI(port=PORT)

class propertydata(BaseModel):
    subtype: Optional[Literal["APARTMENT", "HOUSE"]] = "HOUSE"
    bedroomCount: int = 4
    province: str = "Namur"
    postCode: int = 5330
    habitableSurface: float = 125.00
    buildingCondition: Optional[Literal["AS_NEW", "GOOD", "JUST_RENOVATED", "TO_RENOVATE", "TO_BE_DONE_UP", "TO_RESTORE"]] = "AS_NEW"
    gardenSurface: Optional[float] = 53.00
    hasTerrace: Optional[bool] = True
    epcScore: Optional[str] = "C"
    hasParking: Optional[bool] = True



@app.get("/")
async def root():
    """Route that return 'Alive!' if the server runs."""
    return {"Status": "Alive!"}

@app.get("/about")
def about():
    return {
        "title": "Property Price Prediction API",
        "description": "This API predicts the price of properties (houses or apartments) based on various features such as construction year, area, location, and more.",
        "usage_instructions": [
            "To get an accurate prediction, make sure to enter the correct location (locality) and zip code.",
            "The location and zip code are used to fetch the latitude and longitude, which are important for accurate price estimation.",
            "Please double-check that the locality name matches exactly, and ensure the zip code corresponds to that locality.",
            "Incorrect or missing location information may lead to inaccurate or failed predictions."
        ],
        "note": "Be careful when entering the location and zip code to ensure accurate results. The more precise your inputs, the better the prediction accuracy.",
    }


@app.post("/predict", response_model=Union[float, str])
def predict(property_details: propertydata):
    try:
        # Call the correct function from predict.py
        prediction = predict.dump(property_details)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


"""
Server started at http://127.0.0.1:8000
Documentation at http://127.0.0.1:8000/docs
"""

