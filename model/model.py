# Importing modules and librairies needed for the prediction

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
import joblib
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join(parent_dir, "preprocessing", "preprocessed_data.csv")
df = pd.read_csv(csv_path)
"""
We use OS to get a stable path for the preprocessing file. We need to use 3 lines to be in the correct folder. Then we read the CSV with the 
data and start the splitting part to train and test the preprocessed data. 
"""

X = df.drop("price", axis=1)
y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
"""
We define X and y, X as the data used to predict y the price. Reason why we need to drop the column price for X and put it in the y as y is
the prediction. Then we split between the training and the testing part. We use here a 20 % part of the data to test our prediction. 
"""

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42))
])
pipeline.fit(X_train, y_train)

"""
We use pipeline to create a sequence of transformations and the model. We use an imputer to fill missing values with the mean,
a scaler to standardize the features, and an XGBRegressor as the model for prediction
Then we fit the pipeline with the training data (X_train and y_train). The XGBoost regressor is used with 100 estimators. We haven't put the
results but the R² is around 0.79 wich is the best result we had after testing linear regression, random forest, polynomial and gradient boost
"""

# Sauvegarder le modèle et les colonnes
joblib.dump(pipeline, "model/model.pkl")
joblib.dump(X_train.columns.tolist(), "model/feature_columns.pkl")
"""
We save the model in a pickle file to stabilise and fix him. This way will be able to load the model later for prediction without retraining it.
We also save the feature columns used in the model to ensure that the input data for prediction has the same structure as the training data.
This is important because the model expects the same features it was trained on.
"""
