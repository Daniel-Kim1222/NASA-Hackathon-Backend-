import requests
import os
import pandas as pd
import simplejson as json
from app.utils.csvutil import clean_csv
from app.utils.filters import filt_by_combined_filt, filt_by_dia_and_wavelength, filt_by_discovery_method, filt_by_dist, filt_by_esi
from apscheduler.schedulers.background import BackgroundScheduler

# URL of the API from which we will fetch data 
EXOPLANET_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=csv"

def fetch_data_and_save():
    # fetch data from API, save it as CSV, clean, and save the cleaned data


    folder_name = 'data'

    #making sure that the directory exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Define the file path for the fetched data
    csv_file_path = os.path.join(folder_name, 'planetary_system_composite.csv')

    print("fetching data from the API...")
    try:
        #fetch data from the API
        response = requests.get(EXOPLANET_API_URL)
        response.raise_for_status()

        # Save with raw data as "planetary_system_composite.csv" inside the folder
        with open(csv_file_path, 'wb') as file:
            file.write(response.content)

        print("succeeded!")

        #cleans the csv file from unnecessary columns
        clean_csv(csv_file_path)
        print("Data saved as CSV successfully")


    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# set up scheduler to run daily
scheduler = BackgroundScheduler()

def start_scheduler():
    """Start the scheduler to run fetch_data_and_save once every day."""
    # Call fetch_data_and_save immediately
    #fetch_data_and_save() is what you want to disable if you want to debug the code without saving every time
    fetch_data_and_save()
    # Schedule the function to run daily
    scheduler.add_job(fetch_data_and_save, 'interval', days=1)
     # Start the scheduler
    scheduler.start()

def get_data(threshold = None, type="full"):
    folder_name = 'data'
    csv_file_path = os.path.join(folder_name, 'planetary_system_composite_cleaned.csv')


    # load csv into pandas dataframe
    df = pd.read_csv(csv_file_path)


    #check for file type

    #full data
    if type == "full":
        ddict = df.to_dict(orient="records")
        return json.dumps(ddict, ignore_nan= True)
    
    #these are for if the type is NOT full, and the user requests data of a certain type/threshold.
    if threshold is None:
        raise ValueError(f"threshold is required for filtering with type '{type}'")
    

    #combined is a mix of all of the filters.
    elif type == "combined":
        filt_df = filt_by_combined_filt(df, threshold)
    #distance filters by distance of the planets from our current system.
    elif type == "distance":
        max_distance = threshold.get("max_distance")
        filt_df = filt_by_dist(df, max_distance)
    #this filters by telescope diameter needed and the wavelength of the light measured.
    elif type == "diameter_wavelength":
        telescope_dia = threshold.get("telescope_diameter")
        wavelength = threshold.get("wavelength")
        filt_df = filt_by_dia_and_wavelength(df, telescope_dia, wavelength)
    #this filters by the method of discovery.
    elif type == "discovery_method":
        disc_method = threshold.get("discovery_method")
        filt_df = filt_by_discovery_method(df, disc_method)
    #this filters by ESI, or "earth similarity index". It is a 0-1 scale that measures how similar this planet is to earth, and in turn, how likely it is to support life.
    elif type == "esi":
        esi_threshold = threshold.get("esi_threshold")
        filt_df = filt_by_esi(df, esi_threshold)
    ddict = filt_df[['pl_name']].to_dict(orient = 'records')
    return json.dumps(ddict, ignore_nan = True)
    
