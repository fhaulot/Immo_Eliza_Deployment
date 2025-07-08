import streamlit as st
import requests

st.set_page_config(page_title='Properties price prediction', layout="centered")
"""
Setting the page.
"""
st.title("Property price prediction")
st.markdown("Fill in the blank to get your property prediction price")
"""
Giving a title and a subtitle.
"""
with st.form("prediction_form"):
    subtype = st.selectbox("Type of property", ["HOUSE", "APARTMENT"])
    bedroomCount = st.number_input("Bedroom count", min_value=0, max_value=20, value=1)
    province = st.selectbox("Province", ["Namur", "Brussels", "Luxembourg", "Hainaut", "Liège", "Limburg", "Antwerp", "Flemish Brabant", "Walloon Brabant", "East Flanders", "West Flanders"])
    postCode = st.number_input("Postcode", min_value=1000, max_value=9999, value=5330)
    habitableSurface = st.number_input("Habitable surface (m²)", min_value=10.0, max_value=1000.0, value=125.0)
    buildingCondition = st.selectbox("Building Condition", ["AS_NEW", "GOOD", "JUST_RENOVATED", "TO_RENOVATE", "TO_BE_DONE_UP", "TO_RESTORE"])
    gardenSurface = st.number_input("Garden surface (m²)", min_value=0.0, max_value=1000.0, value=0.0)
    hasTerrace = st.checkbox("Terrace", value=True)
    epcScore = st.selectbox("EPC score", ["A", "B", "C", "D", "E", "F", "G"], index=2)
    hasParking = st.checkbox("Parking", value=True)

    submit = st.form_submit_button("Predict Price")
"""
Creating the form for prediction with every feature. They'are different depending on the need of a selection or inputing a number or ticking a box.
Then we add the submit button. 
"""

if submit:
    with st.spinner("Sending request to the API..."):
        payload = {
            "subtype": subtype,
            "bedroomCount": bedroomCount,
            "province": province,
            "postCode": postCode,
            "habitableSurface": habitableSurface,
            "buildingCondition": buildingCondition,
            "gardenSurface": gardenSurface,
            "hasTerrace": hasTerrace,
            "epcScore": epcScore,
            "hasParking": hasParking,
        }

        try:
            # 
            url = "https://intro-deployement.onrender.com/predict"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Price estimation : **{round(float(prediction), 2)} €**")
            else:
                st.error(f"Error ({response.status_code}) : {response.text}")
        except Exception as e:
            st.error(f"Request error : {e}")
"""
Then we make the request post with a spinner to say that work is in progress. The input data is transofrmed in dictionnary to have the right json
format for the API. The post request is sent directly to the render website deployed.
The request send an output with explanation of the type of error depending on the status_code. 
"""

# link for the streamlit app : https://fhaulot-intro-deployement-streamlit-app-floriane-nnfluk.streamlit.app/