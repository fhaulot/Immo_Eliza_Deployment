import pandas as pd
import numpy as np
import os

def preprocess(house_data):
    """
    Preprocess new house data for prediction
    Takes house data as input and returns preprocessed data
    """
    print(f"Input data: {house_data}")
    
    # Convert to DataFrame if it's a dict
    if isinstance(house_data, dict):
        df = pd.DataFrame([house_data])
    else:
        df = house_data.copy()
    
    print(f"After DataFrame conversion: {df.shape}")
    
    # Add geographic coordinates if postCode is provided
    if 'postCode' in df.columns:
        df = add_lat_lon(df)
    
    # Clean and encode categorical features
    df = clean_categorical_features(df)
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Ensure all required columns are present
    df = ensure_required_columns(df)
    
    print(f"Final preprocessed data shape: {df.shape}")
    print(f"Final columns: {list(df.columns)}")
    
    return df

def add_lat_lon(df):
    """
    Add latitude and longitude coordinates based on postal codes
    """
    df["postCode"] = df["postCode"].astype(str)
    
    # Try to load geographic data
    try:
        # Look for the file in different possible locations
        possible_paths = [
            "georef-belgium-postal-codes.csv",
            "../georef-belgium-postal-codes.csv",
            "../../georef-belgium-postal-codes.csv",
            "data/georef-belgium-postal-codes.csv",
            "./data/georef-belgium-postal-codes.csv"
        ]
        
        geo_df = None
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Loading geographic data from: {path}")
                geo_df = pd.read_csv(path, delimiter=";")
                break
        
        if geo_df is not None:
            geo_df[["lat", "lon"]] = geo_df["Geo Point"].str.split(",", expand=True)
            geo_df["lat"] = geo_df["lat"].astype(float)
            geo_df["lon"] = geo_df["lon"].astype(float)
            geo_df["postCode"] = geo_df["Post code"].astype(str)
            
            # Merge geographic data
            df = df.merge(geo_df[["postCode", "lat", "lon"]], on="postCode", how="left")
            
            # Fill missing coordinates with median values
            if df[['lat', 'lon']].isna().any().any():
                df['lat'].fillna(df['lat'].median(), inplace=True)
                df['lon'].fillna(df['lon'].median(), inplace=True)
        else:
            print("Warning: Geographic data file not found. Using default coordinates.")
            # Use default coordinates (center of Belgium)
            df['lat'] = 50.8503
            df['lon'] = 4.3517
            
    except Exception as e:
        print(f"Error loading geographic data: {e}")
        # Use default coordinates
        df['lat'] = 50.8503
        df['lon'] = 4.3517
    
    return df

def clean_categorical_features(df):
    """
    Clean and encode categorical features
    """
    # Province encoding
    province_mapping = {
        "Brussels": 1, "Brussels-Capital": 1, "Brussels-Capital Region": 1,
        "Luxembourg": 2,
        "Antwerp": 3, "Anvers": 3,
        "Flemish Brabant": 4, "FlemishBrabant": 4,
        "East Flanders": 5, "EastFlanders": 5,
        "West Flanders": 6, "WestFlanders": 6,
        "Liège": 7, "Liege": 7,
        "Walloon Brabant": 8, "WalloonBrabant": 8,
        "Limburg": 9,
        "Namur": 10,
        "Hainaut": 11,
    }
    
    # Type encoding
    type_mapping = {"APARTMENT": 1, "HOUSE": 2, "apartment": 1, "house": 2}
    
    # Subtype encoding
    subtype_mapping = {
        "APARTMENT": 1, "apartment": 1,
        "HOUSE": 2, "house": 2,
        "FLAT_STUDIO": 3, "FLATSTUDIO": 3, "flat_studio": 3,
        "DUPLEX": 4, "duplex": 4,
        "PENTHOUSE": 5, "penthouse": 5,
        "GROUND_FLOOR": 6, "GROUNDFLOOR": 6, "ground_floor": 6,
        "APARTMENT_BLOCK": 7, "APARTMENTBLOCK": 7,
        "MANSION": 8, "mansion": 8,
        "EXCEPTIONAL_PROPERTY": 9, "EXCEPTIONALPROPERTY": 9,
        "MIXED_USE_BUILDING": 10, "MIXEDUSEBUILDING": 10,
        "TRIPLEX": 11, "triplex": 11,
        "LOFT": 12, "loft": 12,
        "VILLA": 13, "villa": 13,
        "TOWN_HOUSE": 14, "TOWNHOUSE": 14, "town_house": 14,
        "CHALET": 15, "chalet": 15,
        "MANOR_HOUSE": 16, "MANORHOUSE": 16,
        "SERVICE_FLAT": 17, "SERVICEFLAT": 17,
        "KOT": 18, "kot": 18,
        "FARMHOUSE": 19, "farmhouse": 19,
        "BUNGALOW": 20, "bungalow": 20,
        "COUNTRY_COTTAGE": 21, "COUNTRYCOTTAGE": 21,
        "OTHER_PROPERTY": 22, "OTHERPROPERTY": 22,
        "CASTLE": 23, "castle": 23,
        "PAVILION": 24, "pavilion": 24,
    }
    
    # EPC encoding
    epc_mapping = {"A+": 8, "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
    
    # Apply encodings
    if "province" in df.columns:
        df["province_encoded"] = df["province"].map(province_mapping).fillna(1)
        print(f"Province encoded: {df['province_encoded'].iloc[0]}")
    
    if "type" in df.columns:
        df["type_encoded"] = df["type"].map(type_mapping).fillna(1)
        print(f"Type encoded: {df['type_encoded'].iloc[0]}")
    
    if "subtype" in df.columns:
        df["subtype_encoded"] = df["subtype"].map(subtype_mapping).fillna(1)
        print(f"Subtype encoded: {df['subtype_encoded'].iloc[0]}")
    
    if "epcScore" in df.columns:
        df["epcScore_encoded"] = df["epcScore"].map(epc_mapping).fillna(4)
        print(f"EPC encoded: {df['epcScore_encoded'].iloc[0]}")
    
    # Handle boolean features
    boolean_features = [
        "hasAttic", "hasGarden", "hasAirConditioning", "hasArmoredDoor",
        "hasVisiophone", "hasTerrace", "hasOffice", "hasSwimmingPool",
        "hasFireplace", "hasBasement", "hasDressingRoom", "hasDiningRoom",
        "hasLift", "hasHeatPump", "hasPhotovoltaicPanels", "hasLivingRoom"
    ]
    
    for feature in boolean_features:
        if feature in df.columns:
            df[f"{feature}_encoded"] = df[feature].map({True: 1, False: 0}).fillna(0)
            print(f"{feature} encoded: {df[f'{feature}_encoded'].iloc[0]}")
    
    return df

def handle_missing_values(df):
    """
    Handle missing values in the dataset
    """
    # Fill numeric columns with median or default values
    numeric_defaults = {
        'bedroomCount': 2.0,
        'bathroomCount': 1.0,
        'habitableSurface': 100.0,
        'toiletCount': 1.0,
        'terraceSurface': 0.0,
        'gardenSurface': 0.0,
    }
    
    for col, default_val in numeric_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default_val)
    
    return df

def ensure_required_columns(df):
    """
    Ensure all required columns are present with default values
    """
    required_columns = {
        'bedroomCount': 2.0,
        'bathroomCount': 1.0,
        'habitableSurface': 100.0,
        'toiletCount': 1.0,
        'terraceSurface': 0.0,
        'gardenSurface': 0.0,
        'province_encoded': 1.0,
        'type_encoded': 1,
        'subtype_encoded': 1,
        'epcScore_encoded': 4.0,
        'hasAttic_encoded': 0,
        'hasGarden_encoded': 0,
        'hasAirConditioning_encoded': 0,
        'hasArmoredDoor_encoded': 0,
        'hasVisiophone_encoded': 0,
        'hasTerrace_encoded': 0,
        'hasOffice_encoded': 0,
        'hasSwimmingPool_encoded': 0,
        'hasFireplace_encoded': 0,
        'hasBasement_encoded': 0,
        'hasDressingRoom_encoded': 0,
        'hasDiningRoom_encoded': 0,
        'hasLift_encoded': 0,
        'hasHeatPump_encoded': 0,
        'hasPhotovoltaicPanels_encoded': 0,
        'hasLivingRoom_encoded': 1,
        'lat': 50.8503,
        'lon': 4.3517
    }
    
    for col, default_val in required_columns.items():
        if col not in df.columns:
            df[col] = default_val
            print(f"Added missing column {col} with default value {default_val}")
    
    # Remove original categorical columns as they're not needed for prediction
    columns_to_remove = ['postCode', 'province', 'type', 'subtype', 'epcScore']
    for col in columns_to_remove:
        if col in df.columns:
            df = df.drop(col, axis=1)
    
    # Remove original boolean columns as we have encoded versions
    boolean_features = [
        "hasAttic", "hasGarden", "hasAirConditioning", "hasArmoredDoor",
        "hasVisiophone", "hasTerrace", "hasOffice", "hasSwimmingPool",
        "hasFireplace", "hasBasement", "hasDressingRoom", "hasDiningRoom",
        "hasLift", "hasHeatPump", "hasPhotovoltaicPanels", "hasLivingRoom"
    ]
    
    for feature in boolean_features:
        if feature in df.columns:
            df = df.drop(feature, axis=1)
    
    return df