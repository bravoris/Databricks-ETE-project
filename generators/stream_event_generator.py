import json
import uuid
import random
import time
import os
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient

# =========================
# CONFIGURATION
# =========================

STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")
CONTAINER_NAME = "raw"

BASE_PATH = "streaming/events"

WRITE_INTERVAL_SECONDS = 3
BURST_PROBABILITY = 0.15
DUPLICATE_PROBABILITY = 0.10
LATE_EVENT_PROBABILITY = 0.15

CUSTOMER_POOL = [f"C{i}" for i in range(1, 201)]
PRODUCT_POOL = [f"P{i}" for i in range(1, 101)]
COUNTRIES = ["India", "USA", "UK", "Germany"]
DEVICES = ["mobile", "desktop", "tablet"]
CHANNELS = ["organic", "ads", "email", "referral"]
PAYMENT_METHODS = ["card", "upi", "wallet", "cod"]

EVENT_TYPES = ["login", "view", "add_to_cart", "purchase", "refund"]

# Keep some previous IDs for duplicates
RECENT_EVENT_IDS = []

# =========================
# ADLS CONNECTION
# =========================

connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={STORAGE_ACCOUNT_NAME};"
    f"AccountKey={STORAGE_ACCOUNT_KEY};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# =========================
# EVENT GENERATOR
# =========================

def generate_event():
    global RECENT_EVENT_IDS

    # Decide duplicate
    if RECENT_EVENT_IDS and random.random() < DUPLICATE_PROBABILITY:
        event_id = random.choice(RECENT_EVENT_IDS)
    else:
        event_id = str(uuid.uuid4())
        RECENT_EVENT_IDS.append(event_id)
        if len(RECENT_EVENT_IDS) > 100:
            RECENT_EVENT_IDS.pop(0)

    event_type = random.choice(EVENT_TYPES)

    customer_id = random.choice(CUSTOMER_POOL)
    session_id = str(uuid.uuid4())

    product_id = None
    quantity = None
    price = None
    payment_method = None

    if event_type != "login":
        product_id = random.choice(PRODUCT_POOL)

    if event_type in ["purchase", "refund"]:
        quantity = random.randint(1, 5)
        price = round(random.uniform(10, 500), 2)
        payment_method = random.choice(PAYMENT_METHODS)
    elif event_type in ["view", "add_to_cart"]:
        quantity = 1
        price = round(random.uniform(10, 500), 2)

    # Late event simulation
    if random.random() < LATE_EVENT_PROBABILITY:
        event_timestamp = datetime.utcnow() - timedelta(minutes=random.randint(5, 120))
    else:
        event_timestamp = datetime.utcnow()

    event = {
        "event_id": event_id,
        "customer_id": customer_id,
        "session_id": session_id,
        "product_id": product_id,
        "event_type": event_type,
        "quantity": quantity,
        "price": price,
        "payment_method": payment_method,
        "device_type": random.choice(DEVICES),
        "channel": random.choice(CHANNELS),
        "country": random.choice(COUNTRIES),
        "event_timestamp": event_timestamp.isoformat()
    }

    return event


# =========================
# FILE WRITER
# =========================

def upload_events(events):
    now = datetime.utcnow()
    date_path = now.strftime("%Y/%m/%d")
    file_name = f"events_{int(time.time())}.json"

    blob_path = f"{BASE_PATH}/{date_path}/{file_name}"

    data = "\n".join(json.dumps(event) for event in events)

    container_client.upload_blob(
        name=blob_path,
        data=data,
        overwrite=True
    )

    print(f"Uploaded {len(events)} events to {blob_path}")


# =========================
# MAIN LOOP
# =========================

def main():
    print("Starting streaming event generator... Press Ctrl+C to stop.")

    try:
        while True:
            if random.random() < BURST_PROBABILITY:
                batch_size = random.randint(50, 100)
                print("Burst spike detected!")
            else:
                batch_size = random.randint(5, 20)

            events = [generate_event() for _ in range(batch_size)]
            upload_events(events)

            time.sleep(WRITE_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Generator stopped.")


if __name__ == "__main__":
    main()