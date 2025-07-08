from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal, Union
from predict import predict
import joblib
import os
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'model', 'feature_columns.pkl')
expected_columns = joblib.load(model_path)
"""
Loading libraries and models. Also the current path for the model and the expected columns.
We use it to ensure that the input data for prediction has the same structure as the training data.
"""

app = FastAPI()
"""
Creating the FastAPI app (local)
"""
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
"""
Creating the basemodel from pydantic to define the differents features for the future POST requests and typing them. We used some value 
"by default" that will alow to test the api and different set after, seeing if the model works.
"""

@app.get("/")
def root():
    return {"Welcome to the Belgian property prediction price tool! For more informations about this prediction model, you may go on the https://intro-deployement.onrender.com//docs "
    "route and try the /predict request to use this tool"}
"""
We use a get request to see if the api is working. Ang get the developer to the documentation. 
"""

@app.post("/predict", response_model=Union[float, str])
def make_prediction(property: PropertyData):
    try:
        return predict.predict(property.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")
"""
The heart of our project. We are calling the basemodel as an input (You may do it with curl but I prefer to do it directly on the docs of
the fast API). It put the basemodel in the predict.py who will call the preprocessing and then will apply the model on the input basemodel. 
If something wen't wrong, it will raise an error. Then, it will return a float."""

# The API was pushed on Render : https://intro-deployement.onrender.com/docs
