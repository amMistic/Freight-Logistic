# Freight Logistic Shipment Delay Prediction 🚚

<div style="display: center; justify-content: space-between;">
  <img src="https://github.com/user-attachments/assets/83224221-6bd1-4017-a76a-a4a357b5e6f2" alt="Image 1" style="width: 85%;">
</div>

This project predicts whether a shipment will be **Delayed** or **On Time** based on various input factors such as origin, destination, vehicle type, weather, and traffic conditions.

## Features
- Predict shipment delay status using a trained machine learning model.
- User-friendly **Streamlit** web interface.
- REST API built with **FastAPI** for backend prediction logic.

## Steps Implemented

### 1. Backend API Development
- Built using **FastAPI**.
- Model trained using `XGBoost` and stored as a pickle file.
- API endpoint `/predict/` accepts shipment details and returns delay status.
- Features include label encoding, distance binning, and categorical ranking for input features.

### 2. Frontend Development
- Built with **Streamlit** for a user-friendly interface.
- Form inputs for shipment details (origin, destination, vehicle type, etc.).
- Integration with the FastAPI backend for predictions.

### 3. Model Training
- Used `XGBoost` for building the predictive model.
- Trained on shipment data with features like traffic conditions, weather, and vehicle type.
- Saved model as `xgb_model.pkl`.

## How to Clone and Run the System Locally

### Prerequisites
- Python 3.8+
- Pip (Python package installer)

### Steps

1. **Clone the Repository**

```bash
git clone https://github.com/amMistic/freight-logistic.git
cd freight-logistic
```

2. **Set Up a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Backend (FastAPI)**

```bash
cd backend
uvicorn main:app --reload
```

- FastAPI will run on `http://127.0.0.1:8000`.

5. **Run the Frontend (Streamlit)**

```bash
cd ../frontend
streamlit run app.py
```

- Streamlit will run on `http://localhost:8501`.
- 
