from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.services.data_service import start_scheduler


#permission statements
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#links routes.py to main.py
app.include_router(api_router, prefix="/api")


#runs on startup
@app.on_event("startup")
def on_startup():
    """start the scheduler and run fetch_data_and_save on startup"""
    start_scheduler()


#main page
@app.get("/")
def root():
    return {"message" : "Welcome to the Grit Force API"}