import pandas as pd
import numpy as np
import os

def create_synthetic_hdi_data():
    np.random.seed(42)
    n_samples = 500
    
    # Generate continuous realistic data ranges
    life_exp = np.random.uniform(50, 85, n_samples)
    mean_school = np.random.uniform(2, 15, n_samples)
    exp_school = np.random.uniform(5, 18, n_samples)
    gni = np.random.uniform(500, 70000, n_samples)
    
    df = pd.DataFrame({
        'life_expectancy': life_exp,
        'mean_schooling': mean_school,
        'expected_schooling': exp_school,
        'gni_per_capita': gni
    })
    
    # Mimic the target metric calculation to generate ground truth labels
    le_i = (df['life_expectancy'] - 20) / 65
    edu_i = (((df['mean_schooling'] / 15) + (df['expected_schooling'] / 18)) / 2)
    inc_i = (np.log(df['gni_per_capita']) - np.log(100)) / (np.log(75000) - np.log(100))
    
    df['hdi_score'] = (le_i * edu_i * inc_i) ** (1/3)
    df['hdi_score'] = df['hdi_score'].clip(0, 1).round(3)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/hdi_dataset.csv', index=False)
    print("Dataset generated successfully at data/hdi_dataset.csv!")

if __name__ == "__main__":
    create_synthetic_hdi_data()
