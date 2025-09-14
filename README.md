# 🌍 CO2 Emission Modeling in Rwanda
This repository contains a machine learning project for predicting CO₂ emissions in Rwanda. It includes:
- Jupyter Notebook for exploratory data analysis (EDA) and model training.
- Streamlit Dashboard for interactive visualization of CO₂ emissions on the map of Rwanda.
- PDF report summarizing results and insights.

## 📊 Project Overview
- Dataset: Kaggle Playground Series S3E20
- Goal: Predict CO₂ emissions based on weekly measurements across locations in Rwanda.

- Users: Researchers & environmental policy managers.

- Machine Learning Models Used:
XGBoost
CatBoost
LightGBM
Random Forest
- Feature Engineering:
Rolling means (moving averages).
Sine/cosine transformations for cyclical features (weeks of year).
Normalization & scaling.
Handling missing values & outliers.
- Evaluation Metric: RMSE (Root Mean Squared Error).

## ⚙️ How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the notebook: `jupyter notebook co2-modeling\ (9).ipynb`

## 📦 Dependencies
Main Python libraries used:
pandas, numpy – data processing
geopandas, folium, pydeck, plotly – geospatial visualization
scikit-learn – ML utilities
xgboost, catboost, lightgbm, randomforest – ML models
optuna – hyperparameter tuning (optional)
streamlit – dashboard UI
## 📑 Results

Best model achieved low RMSE for emission prediction.
Clear spatial and temporal patterns in Rwanda’s CO₂ emissions.
Dashboard enables easy exploration by policymakers and researchers.
## 📜 License
This project is released under the MIT License. Feel free to use, modify, and share with attribution.
