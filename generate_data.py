import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ===== 1. dim_customers =====
INDUSTRIES = ["News", "Sports Broadcasting", "Government", "Public Safety", "Pro A/V", "Streaming/OTT"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]

n_customers = 120
customers = pd.DataFrame({
    "customer_id": range(1, n_customers + 1),
    "customer_name": [fake.company() for _ in range(n_customers)],
    "industry": np.random.choice(INDUSTRIES, n_customers, p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.1]),
    "region": np.random.choice(REGIONS, n_customers, p=[0.35, 0.35, 0.2, 0.1]),
    "segment": np.random.choice(SEGMENTS, n_customers, p=[0.3, 0.4, 0.3]),
    "signup_date": [fake.date_between(start_date="-3y", end_date="-30d") for _ in range(n_customers)],
})
customers.to_csv("data/raw_customers.csv", index=False)

# ===== 2. dim_devices =====
DEVICE_MODELS = ["LU800", "LU600", "LU300", "Solo Backpack", "LiveU Nexus (Software)"]
n_devices = 300
devices = pd.DataFrame({
    "device_id": range(1, n_devices + 1),
    "customer_id": np.random.choice(customers["customer_id"], n_devices),
    "device_model": np.random.choice(DEVICE_MODELS, n_devices, p=[0.25, 0.25, 0.2, 0.15, 0.15]),
    "purchase_type": np.random.choice(["Purchase", "Rental", "Subscription"], n_devices, p=[0.4, 0.25, 0.35]),
    "activation_date": [fake.date_between(start_date="-2y", end_date="-10d") for _ in range(n_devices)],
})
devices.to_csv("data/raw_devices.csv", index=False)

# ===== 3. fact_streaming_sessions =====
n_sessions = 8000
session_rows = []
for i in range(1, n_sessions + 1):
    device_id = random.choice(devices["device_id"])
    device_row = devices[devices["device_id"] == device_id].iloc[0]
    session_date = fake.date_time_between(start_date="-12M", end_date="now")
    duration_min = max(1, np.random.normal(65, 40))
    avg_bitrate = np.random.normal(8000, 2500)  # kbps
    packet_loss_pct = max(0, np.random.exponential(0.4))
    dropped_connection = 1 if random.random() < 0.04 else 0
    uptime_pct = 100 - packet_loss_pct - (5 if dropped_connection else 0)
    uptime_pct = max(0, min(100, uptime_pct))
    session_rows.append({
        "session_id": i,
        "device_id": device_id,
        "customer_id": device_row["customer_id"],
        "session_start": session_date,
        "duration_minutes": round(duration_min, 1),
        "avg_bitrate_kbps": round(max(500, avg_bitrate), 0),
        "packet_loss_pct": round(packet_loss_pct, 2),
        "uptime_pct": round(uptime_pct, 2),
        "dropped_connection": dropped_connection,
        "network_type": np.random.choice(["Cellular Bonded", "Satellite Hybrid", "WiFi", "Wired IP"], p=[0.55, 0.1, 0.2, 0.15]),
    })
sessions = pd.DataFrame(session_rows)
sessions.to_csv("data/raw_streaming_sessions.csv", index=False)

# ===== 4. fact_invoices (Finance) =====
n_invoices = 600
PRICE_BY_TYPE = {"Purchase": 8500, "Rental": 450, "Subscription": 650}
invoice_rows = []
for i in range(1, n_invoices + 1):
    device_id = random.choice(devices["device_id"])
    device_row = devices[devices["device_id"] == device_id].iloc[0]
    base_price = PRICE_BY_TYPE[device_row["purchase_type"]]
    invoice_date = fake.date_between(start_date="-12M", end_date="today")
    amount = round(base_price * np.random.uniform(0.85, 1.25), 2)
    status = np.random.choice(["Paid", "Pending", "Overdue"], p=[0.82, 0.13, 0.05])
    invoice_rows.append({
        "invoice_id": i,
        "customer_id": device_row["customer_id"],
        "device_id": device_id,
        "invoice_date": invoice_date,
        "amount_usd": amount,
        "status": status,
    })
invoices = pd.DataFrame(invoice_rows)
invoices.to_csv("data/raw_invoices.csv", index=False)

print("Done! Files created in ./data/")
print(f"customers: {len(customers)}, devices: {len(devices)}, sessions: {len(sessions)}, invoices: {len(invoices)}")
