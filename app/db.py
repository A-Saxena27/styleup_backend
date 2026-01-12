from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["styleup"]

print("✅ Connected to MongoDB")

