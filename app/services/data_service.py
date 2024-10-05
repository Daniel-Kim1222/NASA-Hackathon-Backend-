import requests
import os
import pandas as pd
import simplejson as json
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


        #clean function should go here once it is written
        print("Data saved as CSV successfully")


    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# set up scheduler to run daily
scheduler = BackgroundScheduler()