import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Belgian Real Estate Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'comparison_properties' not in st.session_state:
    st.session_state.comparison_properties = []

# Custom CSS for better styling
def get_theme_css(dark_mode):
    base_bg = "#0E1117" if dark_mode else "#FFFFFF"
    text_color = "#FAFAFA" if dark_mode else "#262730"
    card_bg = "#262730" if dark_mode else "#F8F9FA"
    
    return f"""
    <style>
        .stApp {{
            background-color: {base_bg};
            color: {text_color};
        }}
        
        .hero-section {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .hero-title {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .hero-subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .prediction-card {{
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        .metric-card {{
            background: {card_bg};
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid {"#404552" if dark_mode else "#E1E8ED"};
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .comparison-card {{
            background: {card_bg};
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #3498db;
        }}
        
        .price-range {{
            background: linear-gradient(90deg, #f39c12, #e67e22);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, #3498db, #2980b9) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
        }}


        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4) !important;
        }}
        
        .error-alert {{
            background: #e74c3c;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #c0392b;
        }}
        
        .success-alert {{
            background: #27ae60;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #229954;
        }}
        
        .info-panel {{
            background: {card_bg};
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid {"#404552" if dark_mode else "#E1E8ED"};
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .footer {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-top: 3rem;
        }}
    </style>
    """

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Configuration
API_BASE_URL = "https://immo-eliza-deployment-01ya.onrender.com"

# Province price data (more comprehensive)
PROVINCE_DATA = {
    "Brussels": {"avg_price": 350000, "price_per_m2": 3500, "trend": "↗️", "color": "#e74c3c"},
    "Antwerp": {"avg_price": 280000, "price_per_m2": 2800, "trend": "↗️", "color": "#3498db"},
    "East Flanders": {"avg_price": 250000, "price_per_m2": 2400, "trend": "→", "color": "#2ecc71"},
    "West Flanders": {"avg_price": 220000, "price_per_m2": 2200, "trend": "↗️", "color": "#f39c12"},
    "Flemish Brabant": {"avg_price": 320000, "price_per_m2": 3200, "trend": "↗️", "color": "#9b59b6"},
    "Walloon Brabant": {"avg_price": 300000, "price_per_m2": 2900, "trend": "→", "color": "#1abc9c"},
    "Hainaut": {"avg_price": 180000, "price_per_m2": 1800, "trend": "↗️", "color": "#e67e22"},
    "Liège": {"avg_price": 190000, "price_per_m2": 1900, "trend": "↗️", "color": "#34495e"},
    "Luxembourg": {"avg_price": 240000, "price_per_m2": 2300, "trend": "↗️", "color": "#16a085"},
    "Namur": {"avg_price": 200000, "price_per_m2": 2000, "trend": "→", "color": "#8e44ad"},
    "Limburg": {"avg_price": 230000, "price_per_m2": 2300, "trend": "↗️", "color": "#d35400"}
}

# Helper functions
def check_api_health():
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        return False, str(e)

def make_prediction(data):
    """Make a prediction request to the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return False, f"Connection Error: {str(e)}"

def calculate_price_insights(predicted_price, province, habitable_surface):
    """Calculate price insights and comparisons"""
    if province in PROVINCE_DATA:
        avg_price = PROVINCE_DATA[province]["avg_price"]
        price_per_m2 = predicted_price / habitable_surface if habitable_surface > 0 else 0
        avg_price_per_m2 = PROVINCE_DATA[province]["price_per_m2"]
        
        price_diff = predicted_price - avg_price
        price_diff_pct = (price_diff / avg_price) * 100
        
        return {
            "price_per_m2": price_per_m2,
            "avg_price_per_m2": avg_price_per_m2,
            "price_diff": price_diff,
            "price_diff_pct": price_diff_pct,
            "vs_average": "above" if price_diff > 0 else "below"
        }
    return None

def create_price_comparison_chart():
    """Create a price comparison chart for provinces"""
    df = pd.DataFrame([
        {
            "Province": province,
            "Average Price (€)": data["avg_price"],
            "Price per m² (€)": data["price_per_m2"],
            "Trend": data["trend"]
        }
        for province, data in PROVINCE_DATA.items()
    ])
    
    fig = px.bar(
        df, 
        x="Province", 
        y="Average Price (€)",
        color="Price per m² (€)",
        title="Average Property Prices by Province",
        color_continuous_scale="viridis"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white' if st.session_state.dark_mode else 'black',
        title_font_size=16,
        xaxis_tickangle=-45
    )
    
    return fig

def validate_inputs(data):
    """Validate input data"""
    errors = []
    
    if data.get('habitableSurface', 0) <= 0:
        errors.append("Habitable surface must be greater than 0")
    
    if data.get('bedroomCount', 0) < 0:
        errors.append("Number of bedrooms cannot be negative")
    
    if data.get('postCode', '').strip() == '':
        errors.append("Postal code is required")
    
    postal_code = data.get('postCode', '').strip()
    if not postal_code.isdigit() or len(postal_code) != 4:
        errors.append("Postal code must be a 4-digit number")
    
    return errors

# Main app
def main():
    # Header with theme toggle
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button(f"{'🌙' if not st.session_state.dark_mode else '☀️'} {'Dark' if not st.session_state.dark_mode else 'Light'}", 
                    key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🏠 Belgian Real Estate Predictor</div>
        <div class="hero-subtitle">AI-Powered Property Valuation • Accurate • Fast • Reliable</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔮 Predict Price", "📊 Market Analysis", "📈 History", "⚙️ Settings"])
    
    with tab1:
        # API Health Check in sidebar
        with st.sidebar:
            st.markdown("### 🔧 System Status")
            health_status, health_data = check_api_health()
            
            if health_status:
                st.success("✅ API Online")
                if health_data:
                    st.json(health_data)
            else:
                st.error("❌ API Offline")
                st.caption(f"Error: {health_data}")
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🔄 Refresh Status"):
                st.rerun()
            
            if st.button("🗑️ Clear History"):
                st.session_state.prediction_history = []
                st.success("History cleared!")
        
        # Main prediction interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Property Details")
            
            # Create a form for better UX
            with st.form("prediction_form"):
                # Basic Information
                st.markdown("**🏠 Basic Information**")
                col1_1, col1_2 = st.columns(2)
                
                with col1_1:
                    property_type = st.selectbox(
                        "Property Type",
                        ["APARTMENT", "HOUSE"],
                        help="Select apartment or house"
                    )
                    
                    bedrooms = st.number_input(
                        "Bedrooms",
                        min_value=0,
                        max_value=20,
                        value=2,
                        help="Number of bedrooms"
                    )
                    
                    bathrooms = st.number_input(
                        "Bathrooms",
                        min_value=0,
                        max_value=10,
                        value=1,
                        help="Number of bathrooms"
                    )
                
                with col1_2:
                    habitable_surface = st.number_input(
                        "Living Area (m²)",
                        min_value=1,
                        max_value=1000,
                        value=85,
                        help="Habitable surface area"
                    )
                    
                    province = st.selectbox(
                        "Province",
                        list(PROVINCE_DATA.keys()),
                        help="Select the province"
                    )
                    
                    postal_code = st.text_input(
                        "Postal Code",
                        value="1000",
                        help="4-digit postal code"
                    )
                
                # Energy and Features
                st.markdown("**⚡ Energy & Features**")
                col2_1, col2_2 = st.columns(2)
                
                with col2_1:
                    epc_score = st.selectbox(
                        "EPC Score",
                        ["A+", "A", "B", "C", "D", "E", "F", "G"],
                        index=2,
                        help="Energy Performance Certificate"
                    )
                    
                    toilets = st.number_input("Toilets", min_value=0, max_value=5, value=1)
                    terrace_surface = st.number_input("Terrace (m²)", min_value=0, max_value=200, value=0)
                    garden_surface = st.number_input("Garden (m²)", min_value=0, max_value=2000, value=0)
                
                with col2_2:
                    has_garden = st.checkbox("🌱 Garden", value=False)
                    has_terrace = st.checkbox("🏖️ Terrace", value=False)
                    has_fireplace = st.checkbox("🔥 Fireplace", value=False)
                    has_living_room = st.checkbox("🛋️ Living Room", value=True)
                
                # Advanced features in expandable section
                with st.expander("🔧 Advanced Features"):
                    col3_1, col3_2, col3_3 = st.columns(3)
                    
                    with col3_1:
                        has_attic = st.checkbox("🏠 Attic", value=False)
                        has_basement = st.checkbox("🏚️ Basement", value=False)
                        has_office = st.checkbox("💼 Office", value=False)
                        has_dining_room = st.checkbox("🍽️ Dining Room", value=False)
                    
                    with col3_2:
                        has_dressing_room = st.checkbox("👔 Dressing Room", value=False)
                        has_lift = st.checkbox("⬆️⬇️ Elevator", value=False)
                        has_swimming_pool = st.checkbox("🏊 Swimming Pool", value=False)
                        has_air_conditioning = st.checkbox("❄️ Air Conditioning", value=False)
                    
                    with col3_3:
                        has_armored_door = st.checkbox("🚪 Armored Door", value=False)
                        has_visiophone = st.checkbox("📹 Visiophone", value=False)
                        has_heat_pump = st.checkbox("🌡️ Heat Pump", value=False)
                        has_photovoltaic = st.checkbox("☀️ Solar Panels", value=False)
                
                # Submit button
                submitted = st.form_submit_button("🔮 Get Price Prediction", use_container_width=True)
                
                if submitted:
                    # Prepare data
                    prediction_data = {
                        "type": property_type,
                        "bedroomCount": bedrooms,
                        "bathroomCount": bathrooms,
                        "habitableSurface": habitable_surface,
                        "province": province,
                        "postCode": postal_code,
                        "epcScore": epc_score,
                        "toiletCount": toilets,
                        "terraceSurface": terrace_surface if terrace_surface > 0 else None,
                        "gardenSurface": garden_surface if garden_surface > 0 else None,
                        "hasGarden": has_garden,
                        "hasTerrace": has_terrace,
                        "hasFireplace": has_fireplace,
                        "hasLivingRoom": has_living_room,
                        "hasAttic": has_attic,
                        "hasBasement": has_basement,
                        "hasOffice": has_office,
                        "hasDiningRoom": has_dining_room,
                        "hasDressingRoom": has_dressing_room,
                        "hasLift": has_lift,
                        "hasSwimmingPool": has_swimming_pool,
                        "hasAirConditioning": has_air_conditioning,
                        "hasArmoredDoor": has_armored_door,
                        "hasVisiophone": has_visiophone,
                        "hasHeatPump": has_heat_pump,
                        "hasPhotovoltaicPanels": has_photovoltaic,
                    }
                    
                    # Clean data
                    prediction_data = {k: v for k, v in prediction_data.items() if v is not None}
                    
                    # Validate inputs
                    errors = validate_inputs(prediction_data)
                    
                    if errors:
                        for error in errors:
                            st.error(f"❌ {error}")
                    else:
                        # Make prediction
                        with st.spinner("🔄 Analyzing property..."):
                            success, result = make_prediction(prediction_data)
                            
                            if success:
                                predicted_price = result.get("predicted_price", 0)
                                
                                # Store in history
                                st.session_state.prediction_history.append({
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "price": predicted_price,
                                    "province": province,
                                    "type": property_type,
                                    "surface": habitable_surface,
                                    "bedrooms": bedrooms
                                })
                                
                                # Display result
                                st.markdown(f"""
                                <div class="prediction-card">
                                    <h2>🎯 Predicted Price</h2>
                                    <h1>€{predicted_price:,.0f}</h1>
                                    <p>€{predicted_price/habitable_surface:,.0f} per m²</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Price insights
                                insights = calculate_price_insights(predicted_price, province, habitable_surface)
                                if insights:
                                    col_i1, col_i2, col_i3 = st.columns(3)
                                    
                                    with col_i1:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <h4>Price per m²</h4>
                                            <h3>€{insights['price_per_m2']:,.0f}</h3>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_i2:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <h4>vs Province Avg</h4>
                                            <h3>€{abs(insights['price_diff']):,.0f}</h3>
                                            <p>{"Above" if insights['vs_average'] == 'above' else "Below"} average</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_i3:
                                        st.markdown(f"""
                                        <div class="metric-card">
                                            <h4>Difference</h4>
                                            <h3>{insights['price_diff_pct']:+.1f}%</h3>
                                        </div>
                                        """, unsafe_allow_html=True)
                                
                                st.success(f"✅ Prediction completed successfully!")
                                
                            else:
                                st.markdown(f"""
                                <div class="error-alert">
                                    <h3>❌ Prediction Failed</h3>
                                    <p>{result}</p>
                                </div>
                                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Market Context")
            
            # Province info
            if 'province' in locals():
                province_info = PROVINCE_DATA.get(province, {})
                st.markdown(f"""
                <div class="info-panel">
                    <h4>{province} Market</h4>
                    <p><strong>Average Price:</strong> €{province_info.get('avg_price', 0):,}</p>
                    <p><strong>Price per m²:</strong> €{province_info.get('price_per_m2', 0):,}</p>
                    <p><strong>Trend:</strong> {province_info.get('trend', '→')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick tips
            st.markdown("""
            <div class="info-panel">
                <h4>💡 Tips for Accuracy</h4>
                <ul>
                    <li>Double-check surface area measurements</li>
                    <li>Include all available features</li>
                    <li>Verify postal code format (4 digits)</li>
                    <li>Be as precise as possible</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Market Analysis")
        
        # Price comparison chart
        fig = create_price_comparison_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        # Province comparison table
        st.markdown("### 🏘️ Province Comparison")
        
        comparison_data = []
        for province, data in PROVINCE_DATA.items():
            comparison_data.append({
                "Province": province,
                "Avg Price (€)": f"€{data['avg_price']:,}",
                "Price/m² (€)": f"€{data['price_per_m2']:,}",
                "Market Trend": data['trend']
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
    
    with tab3:
        st.markdown("### 📈 Prediction History")
        
        if st.session_state.prediction_history:
            history_df = pd.DataFrame(st.session_state.prediction_history)
            
            # Show recent predictions
            st.dataframe(history_df.sort_values('timestamp', ascending=False), use_container_width=True)
            
            # Simple chart
            if len(history_df) > 1:
                fig_history = px.line(
                    history_df, 
                    x='timestamp', 
                    y='price',
                    title='Price Predictions Over Time',
                    markers=True
                )
                fig_history.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white' if st.session_state.dark_mode else 'black'
                )
                st.plotly_chart(fig_history, use_container_width=True)
        else:
            st.info("No predictions yet. Make your first prediction in the 'Predict Price' tab!")
    
    with tab4:
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎨 Appearance**")
            if st.button("Toggle Dark/Light Mode"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
            
            st.markdown("**🔧 API Configuration**")
            st.code(f"API Endpoint: {API_BASE_URL}")
            
        with col2:
            st.markdown("**📊 Data Management**")
            if st.button("Clear Prediction History"):
                st.session_state.prediction_history = []
                st.success("History cleared!")
            
            st.markdown("**ℹ️ About**")
            st.info("This app uses machine learning to predict Belgian real estate prices based on property characteristics and location.")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🏠 Belgian Real Estate Price Predictor</h3>
        <p>AI-Powered Property Valuation for the Belgian Market</p>
        <p>Cooked up with Streamlit & FastAPI magic</p>
        <p><strong>Created by Floriane, Hanieh and Younes</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()