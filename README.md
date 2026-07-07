# 🌍 HDI Neural Intelligence Dashboard

AI-Powered Human Development Index Prediction & Visualization Platform built with Gradio + Plotly

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🎯 Neural Prediction**: Calculate HDI from 4 key indicators
- **🌍 3D Globe Visualization**: Interactive 3D sphere showing HDI color gradient
- **🗺️ World Heatmap**: Real-time choropleth map of global HDI distribution
- **📊 Advanced Charts**: Gauge + Radar charts for detailed breakdown
- **🤖 AI Policy Suggestions**: Automatic recommendations based on weak indices
- **⚔️ Country Presets**: Load data for India, USA, Norway, Japan, Brazil, Nigeria
- **📄 PDF Reports**: Download professional HDI report with 1 click
- **🎨 Glassmorphism UI**: Premium dark theme with blur + glow effects
- **📱 Responsive**: Works perfectly on mobile + desktop

## 🧮 HDI Formula Used

HDI is calculated as the geometric mean of 3 indices:
- **Health**: Life Expectancy at Birth `0-85 years`
- **Education**: Mean + Expected Years of Schooling `0-15, 0-18 years`
- **Income**: GNI per Capita PPP `$100 - $75000`
- git clone https://github.com/your-username/hdi-neural-dashboard
cd hdi-neural-dashboard
pip install -r requirements.txt
python app.py
gradio>=4.0
numpy
plotly
fpdf2
