# 🌍 HDI Capability Prediction Dashboard & ML Pipeline

This project is an end-to-end Machine Learning web application that predicts a country's Human Development Index (HDI) score and classifies it into one of four development tiers (Very High, High, Medium, or Low). The core logic is built using **Scikit-Learn** based on the official United Nations Development Programme (UNDP) formulation framework, and served via a **Flask** web dashboard interface.

---

## 📁 Project Directory Layout

```text
hdi_ml_project/
│
├── data/
│   ├── generate_data.py         # Synthetic generation tool for training data
│   └── hdi_dataset.csv          # Feature matrix repository dataset
│
├── static/
│   ├── style.css                # CSS presentation rules for UI
│   └── feature_importance.png   # Performance evaluation visualization
│
├── templates/
│   └── index.html               # Frontend dashboard input form
│
├── src/
│   ├── __init__.py
│   ├── train.py                 # Training script for Random Forest Regressor
│   └── app.py                   # Production Flask application backend controller
│
├── hdi_model.pkl                # Serialized Scikit-Learn Model (Pickle file)
├── requirements.txt             # Virtual environment external dependencies
└── README.md                    # Operational runtime instructions
```

---

## 🛠️ Required Technical Skills & Stack

- **Environment / Software**: Anaconda, Python 3.8+
- **Data Infrastructure**: NumPy, Pandas
- **Machine Learning Engine**: Scikit-Learn (Random Forest Regressor)
- **Data Visualization**: Matplotlib, Seaborn
- **Web Application Architecture**: Flask (HTML5, CSS3)

---

## 🚀 Setup & Execution Guide

Follow these sequential steps within your **Anaconda Prompt** or system terminal to initialize and execute the project application pipeline:

### 1. Environment Setup & Dependency Installation
Create your workspace directory, change directories, and install the verified packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Generate Training Target Data
Execute the dataset script to synthesize 500 country profile rows mapped directly to standard UN boundary constraints:
```bash
python data/generate_data.py
```
*Verification:* Check that `data/hdi_dataset.csv` is populated and no longer empty.

### 3. Run the Machine Learning Pipeline
Train the Scikit-Learn Random Forest Regressor model and generate diagnostic plots:
```bash
python src/train.py
```
*Verification:* This step creates the `hdi_model.pkl` binary artifact file. Confirm its size is greater than 0 bytes.

### 4. Deploy the Web Application Dashboard
Launch the local Flask application web engine:
```bash
python src/app.py
```

### 5. Access the Interface
Open your web browser and go to:
👉 **`http://127.0.0`**

---

## 📊 Core Simulation Scenarios to Test

Once the dashboard is active, you can test your original three simulation profiles using the form:

*   **Scenario 1 (Very High Tier Development):**
    *   *Inputs:* Life Expectancy: `83.2` | Mean Schooling: `13.4` | Expected Schooling: `18.0` | GNI per Capita: `66000`
    *   *Expected Result:* Score $\ge$ 0.800 (**Very High Human Development**)
*   **Scenario 2 (Emerging Economy Structural Gaps):**
    *   *Inputs:* Life Expectancy: `70.1` | Mean Schooling: `6.7` | Expected Schooling: `11.9` | GNI per Capita: `6800`
    *   *Expected Result:* Score between 0.550 and 0.699 (**Medium Human Development**)
*   **Scenario 3 (Critical Developmental Intervention Zone):**
    *   *Inputs:* Life Expectancy: `54.0` | Mean Schooling: `3.2` | Expected Schooling: `7.5` | GNI per Capita: `1200`
    *   *Expected Result:* Score < 0.550 (**Low Human Development**)
