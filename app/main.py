from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.on_event("startup")
def on_startup():
    """start the scheduler and run fetch_data_and_save on startup"""
    # this is where the code for the scheduler will go when we are done with it

@app.get("/")
def root():
    return {"message" : "Welcome to the Grit Force API"}