from fastapi import FastAPI
import joblib
import os
import pandas as pd
from pydantic import BaseModel, Field, field_validator
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

con = sqlite3.connect("predictions.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bed INTEGER,
    bath INTEGER,
    city TEXT,
    house_size REAL,
    prediction REAL
)''')
con.commit()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models') if os.path.exists(os.path.join(BASE_DIR, '..', 'models')) else '/app/models'

best_model = joblib.load(os.path.join(MODELS_DIR, 'best_model.joblib'))
encoder = joblib.load(os.path.join(MODELS_DIR, 'encoder.joblib'))
scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.joblib'))

class HouseInput(BaseModel):
    bed: int = Field(ge=0)
    bath: int = Field(ge=1)
    city: str
    house_size: float = Field(gt=0)

    @field_validator('city')
    def city_must_be_text(cls, v):
        if v.strip() == '' or v.replace(' ', '').isdigit():
            raise ValueError('City must be a valid name, not a number')
        return v.strip()

@app.post("/predict")
async def predict(data: HouseInput):
    # Extract features from the input data
    features = [data.bed, data.bath, data.city, data.house_size]
    features.append(data.bed + data.bath)
    features.append(data.bed / (data.bath))  # Avoid division by zero
    features = pd.DataFrame([features], columns=['bed', 'bath', 'city', 'house_size', 'total_rooms', 'bed_bath_ratio'])

    # Preprocess the features
    features_encoded = encoder.transform(features)
    features_scaled = scaler.transform(features_encoded)

    # Make a prediction using the best model
    prediction = best_model.predict(features_scaled)

    cur.execute('''INSERT INTO predictions (bed, bath, city, house_size, prediction) VALUES (?, ?, ?, ?, ?)''',
                (data.bed, data.bath, data.city, data.house_size, prediction[0]))
    con.commit()

    return {"prediction": prediction[0]}

@app.get("/history")
async def get_history():
    cur.execute('''SELECT * FROM predictions''')
    rows = cur.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "bed": row[1],
            "bath": row[2],
            "city": row[3],
            "house_size": row[4],
            "prediction": row[5]
        })
    return {"history": history}