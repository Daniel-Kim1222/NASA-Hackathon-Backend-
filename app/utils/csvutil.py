import csv
import os
import pandas as pd
import numpy as np

def clean_csv(input_csv):
    '''cleans the CSV file of useless data and saves it as a new CSV file'''


    #output will be named "_cleaned" after finished
    base_name, ext = os.path.splitext(input_csv)
    output_csv = f"{base_name}_cleaned{ext}"

    try:
        #read the csv file
        df = pd.read_csv(input_csv, low_memory=False)

        #list of things to remove
        suffixes_to_remove = ['err1', 'err2', 'lim', 'format', 'str', 
                              'symerr', '_reflink', 'id', '_flag', 'j', 'mag']
        columns_to_remove = ['hd_name', 'hip_name', 'disc_pubdate', 'disc_method','disc_locale', 'disc_facility',
                     'disc_telescope', 'disc_refname','pl_pubdate', 'pl_ndispec', "htm20", "st_nphot", 
                     "st_nrvc", "st_nspec", "pl_nespec", "pl_ntranspec", "pl_ndispec", "pl_nnotes"]
        #Combine columns to remove (by suffix and by specific name)
        columns_to_exclude = columns_to_remove + [col for col in df.columns if any(col.endswith(suffix) for suffix in suffixes_to_remove)]

        #saves df without columns
        c_df = df.drop(columns=columns_to_exclude, errors="ignore")


        #preprocesses the csv using another function
        p_df = preprocessing_csv(c_df)
        print("data processing complete")

        #removes even more columns
        columns_to_remove = ['ra', 'dec', 'glon', 'glat', 'x', 'y', 'z', 'elon', 'elat', 'elon_rad', 'elat_rad', 'st_spectype']
        final_df = p_df.drop(columns=columns_to_remove, errors='ignore')
        print("data cleaning complete")
        #save cleaned data
        final_df.to_csv(output_csv, index=False)

        #get rid of original csv
        os.remove(input_csv)

    except Exception as e:
        print(f"Error cleaning CSV: {e}")


def preprocessing_csv(input_df):
    '''preprocesses the csv for our needs'''




