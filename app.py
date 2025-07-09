from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import sys
import os
from datetime import datetime
import json
import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from preprocessing.preprocess import preprocess
    from predict.predict import predict, load_model
except ImportError:
    from preprocess import preprocess
    from predict import predict, load_model

# Create FastAPI app
app = FastAPI(
    title="Belgian Real Estate Price Prediction API",
    description="Machine learning-based price predictions for Belgian real estate properties using XGBoost",
    version="1.0.0",
    docs_url="/docs",
    docs_from_flash="/docs-interactive",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    try:
        model = load_model()
        print("Model loaded successfully at startup")
    except Exception as e:
        print(f"Warning: Could not load model at startup: {e}")

# Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    bedroomCount: Optional[int] = Field(None, description="Number of bedrooms")
    bathroomCount: Optional[int] = Field(None, description="Number of bathrooms")
    habitableSurface: Optional[int] = Field(None, description="Habitable surface area (m²)")
    toiletCount: Optional[int] = Field(None, description="Number of toilets")
    terraceSurface: Optional[int] = Field(None, description="Terrace surface area (m²)")
    gardenSurface: Optional[int] = Field(None, description="Garden surface area (m²)")
    province: Optional[str] = Field(None, description="Belgian province")
    type: Optional[str] = Field(None, description="Property type (APARTMENT or HOUSE)")
    subtype: Optional[str] = Field(None, description="Property subtype")
    epcScore: Optional[str] = Field(None, description="Energy performance certificate (A+ to G)")
    postCode: Optional[str] = Field(None, description="Postal code")
    hasAttic: Optional[bool] = Field(None, description="Has attic")
    hasGarden: Optional[bool] = Field(None, description="Has garden")
    hasAirConditioning: Optional[bool] = Field(None, description="Has air conditioning")
    hasArmoredDoor: Optional[bool] = Field(None, description="Has armored door")
    hasVisiophone: Optional[bool] = Field(None, description="Has visiophone")
    hasTerrace: Optional[bool] = Field(None, description="Has terrace")
    hasOffice: Optional[bool] = Field(None, description="Has office")
    hasSwimmingPool: Optional[bool] = Field(None, description="Has swimming pool")
    hasFireplace: Optional[bool] = Field(None, description="Has fireplace")
    hasBasement: Optional[bool] = Field(None, description="Has basement")
    hasDressingRoom: Optional[bool] = Field(None, description="Has dressing room")
    hasDiningRoom: Optional[bool] = Field(None, description="Has dining room")
    hasLift: Optional[bool] = Field(None, description="Has lift/elevator")
    hasHeatPump: Optional[bool] = Field(None, description="Has heat pump")
    hasPhotovoltaicPanels: Optional[bool] = Field(None, description="Has solar panels")
    hasLivingRoom: Optional[bool] = Field(None, description="Has living room")

class PredictionResponse(BaseModel):
    predicted_price: float = Field(..., description="Predicted price in EUR")
    currency: str = Field("EUR", description="Currency of the prediction")
    status: str = Field("success", description="Status of the prediction")
    timestamp: str = Field(..., description="Timestamp of the prediction")
    input_summary: Dict[str, Any] = Field(..., description="Summary of input parameters")

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    timestamp: str

class ServiceInfo(BaseModel):
    service: str
    version: str
    status: str
    model_loaded: bool
    endpoints: Dict[str, str]
    timestamp: str

@app.get("/", response_model=ServiceInfo)
async def home():
    """
    Home page with basic information
    """
    return ServiceInfo(
        service="Belgian Real Estate Price Prediction API",
        version="1.0.0",
        status="alive",
        model_loaded=model is not None,
        endpoints={
            "health": "/health",
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "prediction": "/predict",
            "model_info": "/model/info"
        },
        timestamp=datetime.now().isoformat()
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat()
    )

@app.get("/docs-interactive", response_class=HTMLResponse)
async def interactive_docs():
    """
    Interactive documentation with testing capabilities
    """
    docs_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Belgian Real Estate Price Prediction API - Interactive Testing</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
            .method { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
            .method.post { background: #e74c3c; }
            .method.get { background: #27ae60; }
            code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
            pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }
            .example { background: #d5dbdb; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .link-button { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px 5px; }
            .link-button:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏠 Belgian Real Estate Price Prediction API</h1>
            <p>This FastAPI application provides machine learning-based price predictions for Belgian real estate properties using XGBoost.</p>
            
            <h2>📋 API Documentation</h2>
            <p>FastAPI provides automatic interactive documentation:</p>
            <a href="/docs" class="link-button"> UI Documentation</a>
            <a href="/redoc" class="link-button"> ReDoc Documentation</a>
            
            <h2>🧪 Quick Test</h2>
            <p>Test the API with this sample request:</p>
            <textarea id="jsonInput" rows="15" style="width: 100%; font-family: monospace; padding: 10px; border: 1px solid #bdc3c7; border-radius: 5px;">{
  "bedroomCount": 2,
  "bathroomCount": 1,
  "habitableSurface": 85,
  "province": "Brussels",
  "type": "APARTMENT",
  "subtype": "APARTMENT",
  "epcScore": "C",
  "postCode": "1000",
  "hasGarden": false,
  "hasTerrace": false,
  "hasFireplace": false,
  "hasLivingRoom": true
}</textarea>
            <br><br>
            <button onclick="testPrediction()" style="background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">🚀 Test Prediction</button>
            
            <h4>Response:</h4>
            <pre id="response" style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; min-height: 100px;">Click "Test Prediction" to see the response here...</pre>
            
            <script>
            async function testPrediction() {
                const jsonInput = document.getElementById('jsonInput').value;
                const responseDiv = document.getElementById('response');
                
                try {
                    const data = JSON.parse(jsonInput);
                    responseDiv.textContent = 'Making prediction request...';
                    
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: jsonInput
                    });
                    
                    const result = await response.json();
                    responseDiv.textContent = JSON.stringify(result, null, 2);
                    
                } catch (error) {
                    responseDiv.textContent = 'Error: ' + error.message;
                }
            }
            </script>
            
            <h2>🔗 Available Endpoints</h2>
            <div class="endpoint">
                <h3><span class="method get">GET</span> /</h3>
                <p>Service information and available endpoints</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p>Health check endpoint</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method post">POST</span> /predict</h3>
                <p>Main prediction endpoint - accepts JSON with property data</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /model/info</h3>
                <p>Information about the loaded ML model</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=docs_html)

@app.get("/model/info")
async def model_info():
    """
    Information about the loaded model
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Get model information
        model_info_data = {
            "model_type": str(type(model).__name__),
            "status": "loaded",
            "timestamp": datetime.now().isoformat()
        }
        
        # Try to get additional model information if available
        if hasattr(model, 'get_params'):
            model_info_data["parameters"] = model.get_params()
        
        if hasattr(model, 'feature_importances_'):
            # Get top 10 most important features
            feature_names = [
                'bedroomCount', 'bathroomCount', 'habitableSurface', 'toiletCount',
                'terraceSurface', 'gardenSurface', 'province_encoded',
                'type_encoded', 'subtype_encoded', 'epcScore_encoded', 'lat', 'lon'
            ]
            
            if len(model.feature_importances_) <= len(feature_names):
                importances = list(zip(feature_names[:len(model.feature_importances_)], 
                                     model.feature_importances_))
                importances.sort(key=lambda x: x[1], reverse=True)
                model_info_data["top_features"] = importances[:10]
        
        return model_info_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model info: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """
    Main prediction endpoint
    
    Accepts property data and returns predicted price in EUR.
    All parameters are optional - missing values will be filled with defaults.
    """
    try:
        # Check if model is loaded
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded. Please check server logs.")
        
        # Convert Pydantic model to dict
        house_data = request.dict(exclude_none=True)
        
        # Log the incoming request (optional, for debugging)
        print(f"Prediction request received: {json.dumps(house_data, indent=2)}")
        
        # Preprocess the data
        preprocessed_data = preprocess(house_data)
        
        # Make prediction
        predicted_price = predict(preprocessed_data)
        
        if predicted_price is None:
            raise HTTPException(status_code=500, detail="Failed to make prediction. Please check your input data.")
        
        # Create response
        response = PredictionResponse(
            predicted_price=round(predicted_price, 2),
            currency="EUR",
            status="success",
            timestamp=datetime.now().isoformat(),
            input_summary={
                "bedrooms": house_data.get("bedroomCount", "default"),
                "bathrooms": house_data.get("bathroomCount", "default"),
                "surface": house_data.get("habitableSurface", "default"),
                "province": house_data.get("province", "default"),
                "type": house_data.get("type", "default")
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Custom exception handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "status": "error",
            "available_endpoints": ["/", "/health", "/docs", "/redoc", "/predict", "/model/info"]
        }
    )

if __name__ == '__main__':
    print("🏠 Belgian Real Estate Price Prediction API (FastAPI)")
    print("=" * 55)
    print("Starting server...")
    print("Documentation available at: http://localhost:8000/docs")
    print("Test and doc available at: http://localhost:8000/docs-interactive")
    print("Alternative docs at: http://localhost:8000/redoc")
    print("Health check at: http://localhost:8000/health")
    print("Prediction endpoint: http://localhost:8000/predict")
    print("=" * 55)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)