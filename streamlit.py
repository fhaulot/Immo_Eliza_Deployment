import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import json

# Import your preprocessing and prediction functions
try:
    from preprocess import preprocess
    from predict import predict, load_model
except ImportError:
    st.error("Please ensure preprocess.py and predict.py are in the same directory as this Streamlit app.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Belgian Real Estate Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .prediction-box {
        background-color: #e8f5e8;
        border: 2px solid #27ae60;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    .prediction-price {
        font-size: 2.5rem;
        color: #27ae60;
        font-weight: bold;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load model on startup
@st.cache_resource
def load_ml_model():
    """Load the machine learning model"""
    model = load_model()
    if model is None:
        st.error("❌ Could not load the ML model. Please ensure 'Immo_ML.pkl' is in the 'model' directory.")
        st.stop()
    return model

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = load_ml_model()
    
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Header
st.markdown('<h1 class="main-header">🏠 Belgian Real Estate Price Prediction</h1>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Get AI-powered price predictions for Belgian properties using machine learning</div>', unsafe_allow_html=True)

# Sidebar for input parameters
st.sidebar.header("🔧 Property Details")

# Basic Information
st.sidebar.subheader("📍 Location & Type")
province = st.sidebar.selectbox(
    "Province",
    ["Brussels", "Luxembourg", "Antwerp", "Flemish Brabant", "East Flanders", 
     "West Flanders", "Liège", "Walloon Brabant", "Limburg", "Namur", "Hainaut"],
    index=0
)

post_code = st.sidebar.text_input("Postal Code", value="1000")

property_type = st.sidebar.selectbox(
    "Property Type",
    ["APARTMENT", "HOUSE"],
    index=0
)

subtype_options = {
    "APARTMENT": ["APARTMENT", "FLAT_STUDIO", "DUPLEX", "PENTHOUSE", "GROUND_FLOOR", 
                  "APARTMENT_BLOCK", "TRIPLEX", "LOFT", "SERVICE_FLAT", "KOT"],
    "HOUSE": ["HOUSE", "MANSION", "VILLA", "TOWN_HOUSE", "CHALET", "MANOR_HOUSE", 
              "FARMHOUSE", "BUNGALOW", "COUNTRY_COTTAGE", "CASTLE", "PAVILION"]
}

subtype = st.sidebar.selectbox(
    "Property Subtype",
    subtype_options[property_type],
    index=0
)

# Property Specifications
st.sidebar.subheader("📐 Property Specifications")
bedroom_count = st.sidebar.slider("Number of Bedrooms", 1, 10, 2)
bathroom_count = st.sidebar.slider("Number of Bathrooms", 1, 5, 1)
toilet_count = st.sidebar.slider("Number of Toilets", 1, 5, 1)
habitable_surface = st.sidebar.slider("Habitable Surface (m²)", 20, 500, 85)

# Optional Areas
st.sidebar.subheader("🌿 Optional Areas")
terrace_surface = st.sidebar.slider("Terrace Surface (m²)", 0, 200, 0)
garden_surface = st.sidebar.slider("Garden Surface (m²)", 0, 2000, 0)

# Energy Performance
st.sidebar.subheader("⚡ Energy Performance")
epc_score = st.sidebar.selectbox(
    "EPC Score",
    ["A+", "A", "B", "C", "D", "E", "F", "G"],
    index=3  # Default to C
)

# Features
st.sidebar.subheader("🏡 Property Features")

col1, col2 = st.sidebar.columns(2)

with col1:
    has_attic = st.checkbox("Attic", key="attic")
    has_garden = st.checkbox("Garden", key="garden")
    has_air_conditioning = st.checkbox("Air Conditioning", key="ac")
    has_armored_door = st.checkbox("Armored Door", key="armored")
    has_visiophone = st.checkbox("Visiophone", key="visiophone")
    has_terrace = st.checkbox("Terrace", key="terrace")
    has_office = st.checkbox("Office", key="office")
    has_swimming_pool = st.checkbox("Swimming Pool", key="pool")

with col2:
    has_fireplace = st.checkbox("Fireplace", key="fireplace")
    has_basement = st.checkbox("Basement", key="basement")
    has_dressing_room = st.checkbox("Dressing Room", key="dressing")
    has_dining_room = st.checkbox("Dining Room", key="dining")
    has_lift = st.checkbox("Lift/Elevator", key="lift")
    has_heat_pump = st.checkbox("Heat Pump", key="heat_pump")
    has_photovoltaic_panels = st.checkbox("Solar Panels", key="solar")
    has_living_room = st.checkbox("Living Room", key="living", value=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="sub-header">📊 Property Summary</h2>', unsafe_allow_html=True)
    
    # Create property summary
    property_summary = {
        "🏠 Type": f"{property_type} - {subtype}",
        "📍 Location": f"{province}, {post_code}",
        "🛏️ Bedrooms": bedroom_count,
        "🚿 Bathrooms": bathroom_count,
        "📐 Surface": f"{habitable_surface} m²",
        "⚡ EPC Score": epc_score,
        "🌿 Garden": f"{garden_surface} m²" if has_garden else "No",
        "🏡 Terrace": f"{terrace_surface} m²" if has_terrace else "No"
    }
    
    # Display summary in a nice format
    for key, value in property_summary.items():
        st.write(f"**{key}:** {value}")

with col2:
    st.markdown('<h2 class="sub-header">🔮 Make Prediction</h2>', unsafe_allow_html=True)
    
    if st.button("🚀 Predict Price", type="primary", use_container_width=True):
        # Prepare data for prediction
        house_data = {
            "bedroomCount": bedroom_count,
            "bathroomCount": bathroom_count,
            "habitableSurface": habitable_surface,
            "toiletCount": toilet_count,
            "terraceSurface": terrace_surface,
            "gardenSurface": garden_surface,
            "province": province,
            "type": property_type,
            "subtype": subtype,
            "epcScore": epc_score,
            "postCode": post_code,
            "hasAttic": has_attic,
            "hasGarden": has_garden,
            "hasAirConditioning": has_air_conditioning,
            "hasArmoredDoor": has_armored_door,
            "hasVisiophone": has_visiophone,
            "hasTerrace": has_terrace,
            "hasOffice": has_office,
            "hasSwimmingPool": has_swimming_pool,
            "hasFireplace": has_fireplace,
            "hasBasement": has_basement,
            "hasDressingRoom": has_dressing_room,
            "hasDiningRoom": has_dining_room,
            "hasLift": has_lift,
            "hasHeatPump": has_heat_pump,
            "hasPhotovoltaicPanels": has_photovoltaic_panels,
            "hasLivingRoom": has_living_room
        }
        
        try:
            # Show loading spinner
            with st.spinner("🔄 Analyzing property and making prediction..."):
                # Preprocess data
                preprocessed_data = preprocess(house_data)
                
                # Make prediction
                predicted_price = predict(preprocessed_data)
                
                if predicted_price is not None:
                    # Display prediction
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h3>💰 Predicted Price</h3>
                        <div class="prediction-price">€{predicted_price:,.2f}</div>
                        <p><small>Price prediction based on current market data</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to history
                    prediction_record = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "price": predicted_price,
                        "property_type": property_type,
                        "province": province,
                        "surface": habitable_surface,
                        "bedrooms": bedroom_count
                    }
                    st.session_state.prediction_history.append(prediction_record)
                    
                    # Price insights
                    st.markdown('<h3 class="sub-header">💡 Price Insights</h3>', unsafe_allow_html=True)
                    
                    price_per_sqm = predicted_price / habitable_surface
                    st.write(f"**Price per m²:** €{price_per_sqm:,.2f}")
                    
                    # Price category
                    if predicted_price < 200000:
                        category = "💚 Budget-friendly"
                    elif predicted_price < 400000:
                        category = "🟡 Mid-range"
                    elif predicted_price < 600000:
                        category = "🟠 Premium"
                    else:
                        category = "🔴 Luxury"
                    
                    st.write(f"**Price Category:** {category}")
                    
                else:
                    st.error("❌ Could not make prediction. Please check your inputs.")
                    
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")
            st.write("Please check that all required files are present and try again.")

# Prediction History
if st.session_state.prediction_history:
    st.markdown('<h2 class="sub-header">📈 Recent Predictions</h2>', unsafe_allow_html=True)
    
    # Convert to DataFrame for better display
    history_df = pd.DataFrame(st.session_state.prediction_history)
    history_df['price_formatted'] = history_df['price'].apply(lambda x: f"€{x:,.2f}")
    
    # Show last 5 predictions
    st.dataframe(
        history_df[['timestamp', 'price_formatted', 'property_type', 'province', 'surface', 'bedrooms']].tail(5),
        column_config={
            'timestamp': 'Time',
            'price_formatted': 'Predicted Price',
            'property_type': 'Type',
            'province': 'Province',
            'surface': 'Surface (m²)',
            'bedrooms': 'Bedrooms'
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("🗑️ Clear History"):
        st.session_state.prediction_history = []
        st.rerun()

# Footer with information
st.markdown("---")
st.markdown("""
<div class="info-box">
    <h4>ℹ️ About this Application</h4>
    <p>This application uses machine learning (XGBoost) to predict real estate prices in Belgium. 
    The model has been trained on historical property data and considers various factors including 
    location, property type, size, and features.</p>
    <p><strong>Disclaimer:</strong> Predictions are estimates based on historical data and should not be 
    considered as professional property valuations. Always consult with real estate professionals 
    for accurate assessments.</p>
</div>
""", unsafe_allow_html=True)

# Information about required files
st.markdown("""
<div class="warning-box">
    <h4>⚠️ Required Files</h4>
    <p>To run this application, make sure you have the following files in your directory:</p>
    <ul>
        <li><code>preprocess.py</code> - Data preprocessing functions</li>
        <li><code>predict.py</code> - Prediction functions</li>
        <li><code>model/Immo_ML.pkl</code> - Trained XGBoost model</li>
        <li><code>georef-belgium-postal-codes.csv</code> - Geographic data (optional)</li>
    </ul>
</div>
""", unsafe_allow_html=True)