from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal, Union
from predict import predict
import joblib
import os
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'model', 'feature_columns.pkl')
expected_columns = joblib.load(model_path)


app = FastAPI()

class PropertyData(BaseModel):
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
def root():
    return {"status": "alive"}

@app.get("/about")
def about():
    return {"message": "Use POST /predict with proper JSON payload to get predictions."}

@app.post("/predict", response_model=Union[float, str])
def make_prediction(property: PropertyData):
    try:
        return predict.predict(property.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")
