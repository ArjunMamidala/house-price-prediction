import pandas as pd
import numpy as np
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Load and clean
df = pd.read_csv('data/realtor-data.csv')
df_clean = df.dropna(subset=['bed', 'bath', 'city', 'house_size', 'price'])
df_clean = df_clean[(df_clean['price'] > 0) & (df_clean['house_size'] > 0)]

# Remove outliers
df_clean = df_clean[df_clean['price'] < 10_000_000]        # < $10M
df_clean = df_clean[df_clean['house_size'] < 10_000]        # < 10K sqft
df_clean = df_clean[df_clean['bed'] <= 10]
df_clean = df_clean[df_clean['bath'] <= 10]

print(f"After cleaning: {len(df_clean):,} rows")

# Feature engineering
df_clean['total_rooms'] = df_clean['bed'] + df_clean['bath']
df_clean['bed_bath_ratio'] = df_clean['bed'] / df_clean['bath']

# Filter rare cities
city_counts = df_clean['city'].value_counts()
valid_cities = city_counts[city_counts >= 5].index
df_filtered = df_clean[df_clean['city'].isin(valid_cities)].copy()

X = df_filtered[['bed', 'bath', 'city', 'house_size', 'total_rooms', 'bed_bath_ratio']]
y = df_filtered['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Encode and scale
encoder = ce.TargetEncoder(cols=['city'])
X_train_encoded = encoder.fit_transform(X_train, y_train)
X_test_encoded = encoder.transform(X_test)

sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train_encoded)
X_test_scaled = sc.transform(X_test_encoded)

# Smaller model
rf = RandomForestRegressor(n_estimators=50, max_depth=20, random_state=42)
rf.fit(X_train_scaled, y_train)

print(f"R²: {r2_score(y_test, rf.predict(X_test_scaled)):.4f}")

# Save
joblib.dump(rf, 'models/best_model.joblib', compress=3)
joblib.dump(sc, 'models/scaler.joblib', compress=3)
joblib.dump(encoder, 'models/encoder.joblib', compress=3)

import os
print(f"Model size: {os.path.getsize('models/best_model.joblib') / 1024 / 1024:.0f} MB")
print("Done!")