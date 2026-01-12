from pymongo import MongoClient
import os

# Provide a tolerant db module: if `MONGO_URI` is not set we keep `client` and
# `db` as None so the rest of the app (and tests) can run in an in-memory
# fallback mode implemented in `app.models`.
MONGO_URI = os.getenv("MONGO_URI")

client = None
db = None

if MONGO_URI:
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
    db = client["styleup"]
    print("✅ Connected to MongoDB")

