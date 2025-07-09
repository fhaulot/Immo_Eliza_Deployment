# Immo_Eliza_Deployement

```
Immo_eliza_deployment/ NEED CORRECTION
│
├── app.py
├── Dockerfile
├── README.md
├── requirements.txt
│
├── model/
│   └── model.pkl  # Saved ML model (via joblib/pickle)
│   └── run_model_trainer.py
│
├── preprocessing/
│   └── cleaning_data.py
│
├── predict/
│   └── prediction.py
│
└── streamlit_app.py

```

# ImmoEliza Price Prediction API

## 🚀 API Endpoints

| Method | Route       | Description                              |
|--------|-------------|------------------------------------------|
| GET    | `/`         | Home page with basic information         |
| GET    | `/health`  | Health check endoint for monitoring     |
| GET    | `/docs-interactive`  | Interactive documentation with testing capabilities|
| GET    | `/model/info`  | Information about the loaded model       |
| POST   | `/predict`  | Accepts property data and returns predicted price in EUR. All parameters are optional - missing values will be filled with defaults. |

## 🧾 JSON Input Format

```json
{
    "bedroomCount": 2,
    "bathroomCount": 1,
    "habitableSurface": 100,
    "toiletCount": 1,
    "terraceSurface": 0,
    "gardenSurface": 0,
    "totalParkingCount": 0,
    "province": "Brussels",
    "type": "APARTMENT",
    "subtype": "APARTMENT",
    "epcScore": "C",
    "hasAttic": false,
    "hasGarden": false,
    "hasAirConditioning": false,
    "hasArmoredDoor": true,
    "hasVisiophone": false,
    "hasTerrace": false,
    "hasOffice": false,
    "hasSwimmingPool": false,
    "hasFireplace": false,
    "hasBasement": false,
    "hasDressingRoom": false,
    "hasDiningRoom": false,
    "hasLift": false,
    "hasHeatPump": false,
    "hasPhotovoltaicPanels": false,
    "hasLivingRoom": true,
    "postCode": "1000"
}
```

## 🧠 What streamlit_app.py Does (Big Picture)

It’s a frontend interface that allows users to enter house details. It sends these inputs to the FastAPI server, which holds your machine learning model and returns the predicted price.

Here’s the flow:

```User → Streamlit frontend → FastAPI API → Model → Prediction → Back to user```

### How It Connects to the Model
- streamlit_app.py does not touch the model directly
- It sends a request to FastAPI using requests.post(...)
- FastAPI handles:
- Input validation (pydantic)
- Preprocessing (preprocess())
- Model prediction (predict())
- Then FastAPI returns a JSON response → Streamlit displays it

```
+------------------+       HTTP POST       +-----------------+        +--------------+
|  Streamlit UI    |  ──────────────────▶  |   FastAPI API   |  ───▶  |   ML Model   |
| (streamlit_app)  |     house features    |   (app.py)       |        |  (pkl)    |
+------------------+                      +-----------------+        +--------------+
         ▲                                            ▼
         └──────────  prediction response  ◀──────────┘
```

## How to Run It All NEED CORRECTION TO THE STREAMLIT PART

1.	Install dependencies

    ```
    pip install -r requirements.txt
    ```

2.	Train model (once)

    ```
    python model/predict.py
    ```

3.	Run FastAPI backend

    ```
    uvicorn app:app --reload
    ```

4.	In another terminal, run Streamlit

    ```
    streamlit run streamlit_app.py
    ```
