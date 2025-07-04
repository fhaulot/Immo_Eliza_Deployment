import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor


# Reading new file
df = pd.read_csv(r"C:\Users\fhaul\Documents\GitHub\Immo_Eliza_Regression\preprocessed_data.csv")  

# Ensure 'price' is the target variable and drop it from features
X = df.drop("price", axis=1)  
y = df["price"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Get mean and standard deviation from training set (per feature) and normalize training and testing sets using these values for the training set
X_train_norm = (X_train - X_train.mean()) / X_train.std()  
X_test_norm = (X_test - X_train.mean()) / X_train.std()

# Create pipelines for different regression models
pipelines = {
    "XGBoost" : Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('model', XGBRegressor(random_state=42, n_estimators=100, learning_rate=0.1, max_depth=6))
    ])
}

# Creating a list to store results
results = []

# Looping through each pipeline to fit the model and evaluate performance
for name, pipeline in pipelines.items():
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_train_pred = pipeline.predict(X_train)

    mae_test = mean_absolute_error(y_test, y_pred)
    r2_test = r2_score(y_test, y_pred)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    results.append({
        "Model": name,
        "MAE test": mae_test,
        "R² test": r2_test,
        "MAE train": mae_train,
        "R² train": r2_train
    })

# Creating the sheet to display results
prices_train_pred_df= pd.DataFrame({'actual price (EUR)': y_train, 'predicted price (EUR)': y_train_pred})
prices_test_pred_df= pd.DataFrame({'actual price (EUR)': y_test, 'predicted price (EUR)': y_pred})
results_df = pd.DataFrame(results)
print(results_df)


# keeping the best model for further use
best_model = pipelines["XGBoost"]
joblib.dump(best_model, "model.pkl")

