from kafka import KafkaConsumer
import json
import pickle
import pandas as pd
import os
import threading  # For file lock
from email.message import EmailMessage
import smtplib

# --- 1. Load the pre-trained ML model ---
try:
    with open('fraud_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
except FileNotFoundError:
    print("❌ ERROR: 'fraud_model.pkl' not found. Please run the script to create the model first.")
    exit()

# --- 2. Securely load credentials from environment variables ---
SENDER_EMAIL = "xyz@gmail.com"
SENDER_APP_PASSWORD = "App_password"  # From Google "App Passwords"
RECIPIENT_EMAIL = "xyz@gmail.com"


# --- 3. Define email alert function ---
def send_alert(transaction):
    if not all([SENDER_EMAIL, SENDER_APP_PASSWORD, RECIPIENT_EMAIL]):
        print("❌ ERROR: Email credentials not set as environment variables.")
        return

    print("🚀 Preparing to send email alert...")
    try:
        msg = EmailMessage()
        msg['Subject'] = '⚠️ High-Risk Fraud Alert Detected!'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg.set_content(f'A transaction was flagged as potentially fraudulent by the ML model.\n\nDetails:\n{json.dumps(transaction, indent=2)}')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("   Logging into SMTP server...")
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            print("   Login successful.")
            server.send_message(msg)
            print(f"✅ Alert email sent successfully to {RECIPIENT_EMAIL}!")

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Failed. Check your credentials.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# --- 4. Create Kafka Consumer ---
try:
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='fraud-detection-group-1'
    )
    print("✅ Kafka consumer is running and listening for transactions...")
except Exception as e:
    print(f"❌ ERROR: Could not connect to Kafka. Error: {e}")
    exit()

# --- 5. Initialize file lock for dashboard_data.json ---
lock = threading.Lock()

# --- 6. Main loop to process messages ---
for message in consumer:
    transaction = message.value
    print(f"\n📥 Received: {transaction}")

    # --- Simple feature engineering placeholder ---
    amount = transaction.get('amount', 0)
    location = 1 if transaction.get('location') == 'risky' else 0

    X_new = pd.DataFrame({
        'amount': [amount],
        'location': [location]
    })

    try:
        prediction = model.predict(X_new)[0]
        is_fraud = int(prediction == 1)

        if is_fraud:
            print("🚨 FRAUD DETECTED by ML Model!")
            send_alert(transaction)
        else:
            print("✅ Transaction is legitimate.")

        # --- Append result to dashboard_data.json ---
        transaction_record = transaction.copy()
        transaction_record['is_fraud'] = is_fraud

        try:
            lock.acquire()
            if os.path.exists('dashboard_data.json'):
                with open('dashboard_data.json', 'r') as f:
                    dashboard_data = json.load(f)
            else:
                dashboard_data = []

            dashboard_data.append(transaction_record)

            # Optional: Keep only last 100 transactions
            dashboard_data = dashboard_data[-100:]

            with open('dashboard_data.json', 'w') as f:
                json.dump(dashboard_data, f, indent=2)

            print("📊 Transaction saved to dashboard_data.json")

        finally:
            lock.release()

    except Exception as e:
        print(f"❌ ERROR during model prediction: {e}")
