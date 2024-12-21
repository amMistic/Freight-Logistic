import streamlit as st
import requests

# Define the Streamlit app layout
st.set_page_config(page_title="Shipment Prediction", page_icon="🚚", layout="wide")

# Title of the app
st.title("Shipment Delay Prediction 🚚")

# Instructions
st.subheader("""
This app predicts whether your shipment will be Delayed or On Time based on the shipment details provided.
Fill in the details below and hit Predict to get the result.
""")

# List of cities
cities = [
    "Pune", "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad",
    "Ahmedabad", "Kolkata", "Lucknow", "Jaipur"
]

# Types of vehicles
vehicles = [
    "container", "lorry", "trailer", "truck"
]

# Weather Conditions
weather = [
    "clear", "fog", "rain", "storm"
]

# Traffic Conditions
traffic = [
    "heavy", "light", "moderate"
]

# Input fields for shipment details
with st.form(key='shipment_form'):
    origin = st.selectbox("Origin", cities)
    destination = st.selectbox("Destination", cities)
    shipment_date = st.date_input("Shipment Date")
    planned_delivery_date = st.date_input("Planned Delivery Date")
    actual_delivery_date = st.date_input("Actual Delivery Date")
    vehicle_type = st.selectbox("Vehicle Type", vehicles )
    distance = st.number_input("Distance (km)", min_value=1, max_value=5000, step=1)
    weather_conditions = st.selectbox("Weather Conditions", weather )
    traffic_conditions = st.selectbox("Traffic Conditions", traffic )

    submit_button = st.form_submit_button(label="Predict")

# Handle the form submission and make the API call
if submit_button:
    # Prepare the payload
    payload = {
        "origin": origin,
        "destination": destination,
        "shipment_date": str(shipment_date),
        "planned_delivery_date": str(planned_delivery_date),
        "actual_delivery_date": str(actual_delivery_date),
        "vehicle_type": vehicle_type,
        "distance": distance,
        "weather_conditions": weather_conditions,
        "traffic_conditions": traffic_conditions
    }

    # Send request to FastAPI backend
    api_url = "http://127.0.0.1:8000/predict/"  # Adjust based on where your FastAPI is running
    response = requests.post(api_url, json=payload)

    # Show result
    if response.status_code == 200:
        result = response.json()
        st.subheader(f"Prediction: {result['prediction']}")
    else:
        st.error("There was an error in prediction. Please try again later.")