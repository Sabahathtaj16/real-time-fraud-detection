from kafka import KafkaProducer
import json
import time

# === Load transactions from JSON ===
with open('transactions.json', 'r') as f:
    transactions = json.load(f)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# === Send each transaction ===
for transaction in transactions:
    print("Sending:", transaction)
    producer.send('transactions', transaction)
    producer.flush()
    time.sleep(1)  # wait between sends

print("✅ All transactions sent.")
