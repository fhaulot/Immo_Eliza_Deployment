from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from preprocessing.cleaning_data import preprocess, PreprocessingError
from predict.prediction import predict

app = FastAPI()

class PropertyInput(BaseModel):
    area: int
    property_type: Literal["APARTMENT", "HOUSE", "OTHERS"] = Field(..., alias="property-type")
    rooms_number: int = Field(..., alias="rooms-number")
    zip_code: int = Field(..., alias="zip-code")
    land_area: Optional[int] = Field(None, alias="land-area")
    garden: Optional[bool] = None
    garden_area: Optional[int] = Field(None, alias="garden-area")
    equipped_kitchen: Optional[bool] = Field(None, alias="equipped-kitchen")
    full_address: Optional[str] = Field(None, alias="full-address")
    swimming_pool: Optional[bool] = Field(None, alias="swimming-pool")
    furnished: Optional[bool] = None
    open_fire: Optional[bool] = Field(None, alias="open-fire")
    terrace: Optional[bool] = None
    terrace_area: Optional[int] = Field(None, alias="terrace-area")
    facades_number: Optional[int] = Field(None, alias="facades-number")
    building_state: Optional[Literal["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"]] = Field(None, alias="building-state")

@app.get("/")
async def root():
    return "alive"

@app.get("/predict")
async def predict_info():
    return JSONResponse(content={
        "description": "POST JSON to /predict with house data in this format",
        "example": {
            "data": {
                "area": 120,
                "property-type": "HOUSE",
                "rooms-number": 3,
                "zip-code": 1000,
                "garden": True,
                "terrace": True,
                "building-state": "GOOD"
            }
        }
    })

@app.post("/predict")
async def predict_route(payload: Dict[str, Any]):
    try:
        if "data" not in payload:
            raise HTTPException(status_code=400, detail="Missing 'data' field in JSON payload.")
        
        raw_data = payload["data"]
        
        # Preprocess and validate
        cleaned = preprocess(raw_data)
        
        # Predict price
        price = predict(cleaned)
        
        return {
            "prediction": price,
            "status_code": 200
        }
    except PreprocessingError as pe:
        raise HTTPException(status_code=422, detail=f"Preprocessing error: {str(pe)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
