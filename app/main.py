from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.services.data_service import start_scheduler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    """start the scheduler and run fetch_data_and_save on startup"""
    start_scheduler()

@app.get("/")
def root():
    return {"message" : "Welcome to the Grit Force API"}