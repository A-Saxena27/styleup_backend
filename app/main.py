from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
from app.models import connect_db, close_db
from app.db import MONGO_URI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient(MONGO_URI)
db = client["styleup"]
users = db["users"]

@app.get("/")
def home():
    return {"status": "StyleUp backend running"}

app = FastAPI(title="StyleUp Backend")

@app.get("/")
def root():
    return {"message": "StyleUp backend running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running smoothly"}

import logging

logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def startup_event():
    logging.info("Starting StyleUp backend...")
    connect_db()


app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
	connect_db()


@app.on_event("shutdown")
async def shutdown_event():
	close_db()


app.include_router(api_router, prefix="/api")

