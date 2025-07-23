Real-Time Financial Fraud Detection System

This project is a complete end-to-end fraud detection system that uses machine learning to identify fraudulent financial transactions — in real-time. It was developed during our internship at ZIDIO.

Project Highlights
- Supervised ML models with 99%+ accuracy (XGBoost, LightGBM, Random Forest)
- Unsupervised anomaly detection using Isolation Forest and PCA
- Real-time prediction pipeline using Apache Kafka
- Live email alerting system for high-risk transactions
- Streamlit dashboard for real-time visualization and monitoring
- Graph-based fraud ring detection using synthetic data and NetworkX

Files Included
- `zidio.ipynb`: Main notebook with data prep, modeling, and real-time pipeline
- `ZIDIO_PROJECT_1.pdf`: Final report with all implementation phases
- `transactions.json` (optional): Sample transaction stream input
- `dashboard_data.json` (optional): Streamlit dashboard source file
- `fraud_model.pkl` (optional): Pre-trained model for Kafka consumer

Tech Stack
- Python, Pandas, Scikit-learn, XGBoost, LightGBM
- Kafka for real-time message streaming
- Streamlit for dashboard
- SMTP for email alerts
- NetworkX for graph analysis

Models Implemented

| Model              | Type          | Highlights                      |
|-------------------|---------------|----------------------------------|
| Random Forest      | Supervised    | High recall & precision         |
| XGBoost            | Supervised    | Best performance overall        |
| LightGBM           | Supervised    | Fast + high accuracy            |
| Isolation Forest   | Unsupervised  | Detects new/unseen fraud types  |
| PCA (Reconstruction Error) | Unsupervised  | Autoencoder-style anomaly detection |
| Graph-Based Analysis | Conceptual  | Fraud ring visualization        |

Live Monitoring Dashboard
Built using Streamlit:
- Real-time logs
- Fraud/legit transaction counts
- Visual bar charts
- Refreshes every 5 seconds

Alert System
- Email notifications sent via SMTP if a transaction is predicted as fraudulent

Contributors
- Sabahath Taj Z
- Riya Yadav

Future Scope
- AI-powered risk scoring system
- Blockchain-based transaction tracking
- Mobile app integration for instant fraud alerts

Dataset
- Kaggle: Credit Card Fraud Detection Dataset 2023
- Balanced dataset: 50% fraud, 50% legit

Developed during our internship at ZIDIO
