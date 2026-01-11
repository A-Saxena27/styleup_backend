from pymongo import MongoClient
import os

MONGO_URI = "mongodb+srv://styleupadmin:Saxena200527@styleup-mongo.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["styleup"]

print("Connected to MongoDB!")
