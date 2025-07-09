# Intro_deployement

```
immoeliza-api/
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
| GET    | `/`         | Health check, returns `alive`           |
| GET    | `/predict`  | Returns JSON structure description      |
| POST   | `/predict`  | Accepts JSON input and returns prediction|

## 🧾 JSON Input Format

```json
{
  "data": {
    "area": 120,
    "property-type": "HOUSE",
    "rooms-number": 4,
    "zip-code": 1000
  }
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
| (streamlit_app)  |     house features    |   (app.py)       |        |  (joblib)    |
+------------------+                      +-----------------+        +--------------+
         ▲                                            ▼
         └──────────  prediction response  ◀──────────┘
```

## How to Run It All

1.	Install dependencies

    ```
    pip install -r requirements.txt
    ```

2.	Train model (once)

    ```
    python model/run_model_trainer.py
    ```

3.	Run FastAPI backend

    ```
    uvicorn app:app --reload
    ```

4.	In another terminal, run Streamlit

    ```
    streamlit run streamlit_app.py
    ```
