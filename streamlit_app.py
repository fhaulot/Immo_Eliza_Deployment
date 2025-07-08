import streamlit as st
import requests
import json

payload = {
    "data": {
        "area": 120,
        "property-type": "HOUSE",
        "rooms-number": 4,
        "zip-code": 1000
    }
}

st.title("🏡 ImmoEliza Price Prediction")

# Display introduction text
st.markdown(
    """
    This app helps you estimate the price range for buying a house or apartment. 
    You'll see a simple form where you can enter details about the property you're interested in, like its type, size, location, and features. 
    Don't worry, it's easy—just pick options from drop-down menus and sliders.

    Once you've filled in the details, click the "Predict!" button, and voila! 
    The app will crunch the numbers for you and show you an estimated price range based on similar properties. 
    It's like having your own real estate expert right at your fingertips!

    If you ever get stuck or have questions, don't worry. 
    Just click the button, and the app will guide you through the process. 
    
    Happy house hunting!

    
    [Repository](https://github.com/fhaulot/Immo_Eliza_Deployment/tree/immoEliza_deployment_by_Hanieh)</small>                                
    [API](https://immoelizapredictor.onrender.com/docs)</small>                         
    [Data Analysis](https://immoelizaanalysis.streamlit.app/)</small>


    <small> @ created by Florian, Hanieh, and Younes


    """,
    unsafe_allow_html=True
)

st.sidebar.header("Input Property Details")

area = st.sidebar.number_input("Area (m²)", min_value=10)
rooms = st.sidebar.number_input("Rooms", min_value=1)
zip_code = st.sidebar.number_input("Zip Code", min_value=1000, max_value=9999)
property_type = st.sidebar.selectbox("Property Type", ["APARTMENT", "HOUSE", "OTHERS"])

if st.sidebar.button("Predict Price"):
    payload = {
        "data": {
            "area": area,
            "property-type": property_type,
            "rooms-number": rooms,
            "zip-code": zip_code
        }
    }
    response = requests.post("http://localhost:8000/predict", json=payload)
    result = response.json()
    if response.status_code == 200:
        st.success(f"💰 Predicted Price: €{result['prediction']}")
    else:
        st.error(result.get("detail", "Error"))