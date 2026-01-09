from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
from app.models import connect_db, close_db

app = FastAPI(title="StyleUp Backend")

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

