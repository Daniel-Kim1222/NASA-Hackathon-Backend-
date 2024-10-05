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


@router.post("/data/filter/distance")
async def get_exoplanet_data_distance(request: Request):
    # Extract max distance from JSON
    request_data = await request.json()
    max_distance = request_data.get("max_distance")

    if not max_distance:
        return {"error" : "max distance is required"}
    
    filtered_data = get_data(request_data, "distance")

    return {"filered_data": filtered_data}


@router.post("/data/filter/diameter-wavelength")
async def get_exoplanet_data_diameter_wavelength(request: Request):
    try:
        # Extract diameter and wavelength from JSON 
        request_data = await request.json()
        diameter = request_data.get("telescope_diameter")
        wavelength = request_data.get("wavelength")

        if not diameter or not wavelength:
            return {"error" : "input missing"}
        
        # filter using data service
        filtered_data = get_data(request_data, "diameter_wavelength")
        return {"filtered_data" : filtered_data}
    
    except Exception as e:
        return {"error" : str(e)}
    
@router.post("/data/filter/discovery-method")
async def get_exoplanet_data_discovery_method(request: Request):
    try:
        # Extract the diameter and wavelength from the JSON 
        request_data = await request.json()
        discovery_method = request_data.get("discovery_method")
        
        if not discovery_method:
            return {"error": "discovery method is required"}

        # fliter using data service
        filtered_data = get_data(request_data, "discovery_method")
        return {"filtered_data": filtered_data}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/data/filter/esi")
async def get_exoplanet_data_esi(request: Request):
    try:
        # Extract the diameter and wavelength from the JSON 
        request_data = await request.json()
        esi_threshold = request_data.get("esi_threshold")
        
        if not esi_threshold:
            return {"error": "discovery method is required"}

        # filter using data service
        filtered_data = get_data(request_data, "esi")
        return {"filtered_data": filtered_data}

    except Exception as e:
        return {"error": str(e)}
    
@router.post("/data/filter/combined")
async def apply_combined_filters_api(request: Request):
    try:
        # Extract filter criteria from the JSON
        request_data = await request.json()
        
        filtered_data = get_data(request_data, "combined")
        
        return {"filtered_data": filtered_data}
    
    except Exception as e:
        return {"error": str(e)}