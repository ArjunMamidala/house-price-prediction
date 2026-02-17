# House Price Predictor

An end-to-end ML web application that predicts house prices across 17,000+ cities using a Random Forest model trained on 1.5M property records.

## Tech Stack

**ML Pipeline:** Python, scikit-learn, XGBoost, Pandas, NumPy

**Backend:** FastAPI, SQLite, Pydantic

**Frontend:** React.js

**DevOps:** Docker, Docker Compose

## Project Overview

### ML Pipeline
- Cleaned and preprocessed 2.2M property records from a Kaggle dataset, removing 32% of incomplete data
- Engineered features including target encoding for 17,000+ unique cities using `category_encoders.TargetEncoder`
- Trained and evaluated three models with proper train/validation/test splitting (70/15/15):

| Model | Validation R² | Test R² |
|---|---|---|
| Linear Regression | 0.59 | — |
| Random Forest | **0.69** | **0.69** |
| XGBoost (tuned) | 0.66 | — |

- Diagnosed and resolved XGBoost overfitting (train-val gap 0.08 → 0.01) through regularization tuning
- Selected Random Forest as the production model based on generalization performance

### Backend
- FastAPI REST API with `/predict` and `/history` endpoints
- Pydantic input validation with type checking and value constraints
- SQLite database storing prediction history
- Model inference pipeline: Target Encoding → Standard Scaling → Random Forest Prediction

### Frontend
- React.js interface with dark theme UI
- Real-time price predictions with form validation
- Prediction history display

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Run with Docker
```bash
docker-compose up --build
```

- Frontend: http://localhost:3001
- Backend: http://localhost:8000

### Run Locally

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### POST /predict
Predict a house price.

**Request:**
```json
{
  "bed": 3,
  "bath": 2,
  "city": "San Juan",
  "house_size": 1500
}
```

**Response:**
```json
{
  "prediction": 296067.30
}
```

### GET /history
Retrieve all past predictions.

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "bed": 3,
      "bath": 2,
      "city": "San Juan",
      "house_size": 1500.0,
      "prediction": 296067.30
    }
  ]
}
```

## Project Structure
```
house-price-prediction/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── models/
│   ├── best_model.joblib
│   ├── scaler.joblib
│   └── encoder.joblib
├── notebooks/
│   └── 01_eda.ipynb
├── docker-compose.yml
└── README.md
```

## Key Technical Decisions

1. **Target Encoding over One-Hot:** 17,000+ unique cities made one-hot encoding infeasible. Target encoding reduced this to a single numeric feature while improving R² from 0.29 to 0.69.

2. **Random Forest over XGBoost:** With only 6 features, Random Forest's bagging approach generalized better than XGBoost's boosting. XGBoost showed overfitting tendencies even after regularization tuning.

3. **Train/Val/Test Split with Stratification:** Stratified splitting by city frequency ensured rare cities appeared in all sets, preventing data leakage and improving encoder reliability.

## Dataset

[USA Real Estate Dataset](https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset) — 2.2M property listings from Realtor.com.

> **Note:** Model files (.joblib) are not included in the repository due to size. To generate them, run the notebook in `notebooks/01_eda.ipynb`.
