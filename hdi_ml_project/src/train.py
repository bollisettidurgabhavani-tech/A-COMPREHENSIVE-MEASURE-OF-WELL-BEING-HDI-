import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_pipeline():
    # Load dataset
    if not os.path.exists('data/hdi_dataset.csv'):
        raise FileNotFoundError("Run data/generate_data.py first to create the dataset.")
        
    df = pd.read_csv('data/hdi_dataset.csv')
    
    # Features and Target split
    X = df[['life_expectancy', 'mean_schooling', 'expected_schooling', 'gni_per_capita']]
    y = df['hdi_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and fit Machine Learning Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    print(f"Model R² Score: {r2_score(y_test, predictions):.4f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test, predictions):.4f}")
    
    # Save Model Artifact
    with open('hdi_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved as hdi_model.pkl")
    
    # Generate Feature Importance Visualization
    plt.figure(figsize=(8, 5))
    sns.barplot(x=model.feature_importances_, y=X.columns, palette='viridis')
    plt.title('Feature Performance Metrics impacting HDI')
    plt.xlabel('Importance Value Weight')
    plt.tight_layout()
    plt.savefig('static/feature_importance.png')
    plt.close()

if __name__ == "__main__":
    train_pipeline()
