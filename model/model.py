import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
import joblib


df = pd.read_csv(r"C:\Users\fhaul\Documents\GitHub\Intro_deployement\preprocessing\preprocessed_data.csv")
X = df.drop("price", axis=1)
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42))
])

pipeline.fit(X_train, y_train)

# Sauvegarder le modèle et les colonnes
joblib.dump(pipeline, "model/model.pkl")
joblib.dump(X_train.columns.tolist(), "model/feature_columns.pkl")

