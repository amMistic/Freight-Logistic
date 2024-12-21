from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
with open("model\\xgb_model.pkl", "rb") as file:
    model = pickle.load(file)

# Define input schema
class ShipmentDetails(BaseModel):
    origin: str
    destination: str
    shipment_date: str
    planned_delivery_date: str
    actual_delivery_date: str
    vehicle_type: str
    distance: int
    weather_conditions: str
    traffic_conditions: str

# load dataset
df = pd.read_csv('data\\freight_delivery_realistic_data.csv')

@app.get('/')
def root():
    return {'message': "Hello world :)"}

# Define the prediction endpoint
@app.post("/predict/")
def predict(details: ShipmentDetails):
    # Feature Engineering
    shipment_day, shipment_month, _ = details.shipment_date.split('-')
    planned_day, planned_month, _ = details.planned_delivery_date.split('-')
    actual_day, actual_month, _ = details.actual_delivery_date.split('-')
    
    # Label Encoding
    origin_cities = df['Origin'].value_counts()
    origin_cities_rank = { city : i  for i, city in enumerate(origin_cities.index)}
    
    destination_cities = df['Destination'].value_counts()
    destination_cities_rank = { city : i for i, city in enumerate(destination_cities.index)}

    origin_encoded = origin_cities_rank.get(details.origin, -1)
    destination_encoded = destination_cities_rank.get(details.destination, -1)

    # Distance Binning
    bins = [650, 1102, 1551, 2000]
    labels = [1, 2, 0, 3]
    distance = labels[-1] if details.distance >= bins[-1] else next(labels[i] for i, bin in enumerate(bins) if details.distance < bin)

    # Categorical Rankings
    traffic_rank = {'heavy': 0, 'light': 1, 'moderate': 2}
    weather_rank = {'clear': 0, 'fog': 1, 'rain': 2, 'storm': 3}
    vehicle_type_rank = {'container': 0, 'lorry': 1, 'trailer': 2, 'truck': 3}

    vehicle_type_encoded = vehicle_type_rank.get(details.vehicle_type.lower(), -1)
    weather_condition_encoded = weather_rank.get(details.weather_conditions.lower(), -1)
    traffic_condition_encoded = traffic_rank.get(details.traffic_conditions.lower(), -1)

    # Prepare Feature List
    feature_names = [
        'Vehicle Type', 'Weather Conditions', 'Traffic Conditions',
        'Shipment Day', 'Shipment Month',
        'Planned Delivery Day', 'Planned Delivery Month',
        'Actual Delivery Day', 'Actual Delivery Month',
        'Origin_rank', 'Destination_rank', 'Distance Group'
    ]
    
    features = [vehicle_type_encoded, weather_condition_encoded, traffic_condition_encoded, 
                int(shipment_day), int(shipment_month), int(planned_day), int(planned_month), 
                int(actual_day), int(actual_month), origin_encoded, destination_encoded, distance]

    df_features = pd.DataFrame([features], columns=feature_names)

    # Predict Delay
    delayed = model.predict(df_features)[0]
    if delayed == 1:
        return {"prediction": "Delayed"}
    else:
        return {"prediction": "On Time"}

# Run the app (Use `uvicorn` to run)
