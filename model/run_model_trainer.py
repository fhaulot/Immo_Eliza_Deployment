# run_model_trainer.py (temporary file)
from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib
import os

df = pd.DataFrame({
    "area": [50, 100, 150],
    "property-type": [0, 1, 0],
    "rooms-number": [2, 4, 5],
    "zip-code": [1000, 2000, 3000],
    "price": [200000, 400000, 600000]
})

X = df[["area", "property-type", "rooms-number", "zip-code"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.joblib")