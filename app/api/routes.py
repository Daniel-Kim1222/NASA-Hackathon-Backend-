from fastapi import APIRouter, Request
from app.services.data_service import fetch_data_and_save, get_data
import simplejson as json


router = APIRouter()

@router.get("/fetch")
def fetch_data():
    fetch_data_and_save()
    return {"message":"data fetched and saved as CSV"}


@router.get("/data")
def get_exo_data():
    """Return the cleaned exoplanet data."""
    data = get_data()
    return json.loads(data)
