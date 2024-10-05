import requests
import os
import pandas as pd
import simplejson as json

# URL of the API from which we will fetch data 
EXOPLANET_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=csv"

def fetch_data_and_save():
    # fetch data from API, save it as CSV, clean, and save the cleaned data


    folder_name = 'data'


    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    