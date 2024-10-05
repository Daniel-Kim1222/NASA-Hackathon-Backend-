from fastapi import APIRouter, Request
import simplejson as json


router = APIRouter()

@router.get("/fetch")
def fetch_data():
    # will put fetch command here from services when done
    return {"message":"data fetched and saved as CSV"}
