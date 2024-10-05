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
    #get cartesian coordinates for host stars
    p_df = convert_to_cartesian(input_df)
    #standardize spectral types
    p_df['st_spectype'] = p_df['st_spectype'].astype(str)
    p_df['st_spectype_cleaned'] = p_df['st_spectype'].apply(convert_spectral_type)
    #categorize exoplanets
    p_df['pl_type'] = p_df['pl_rade'].apply(categorize_exoplanets_by_radius)
    p_df['pl_esi'] = calculate_esi(p_df)
    return p_df




def convert_to_cartesian(df):
    #make a copy of the df
    df_copy = df.copy()

    df_copy['elon_rad'] = np.deg2rad(df_copy['elon'])
    df_copy['elat_rad'] = np.deg2rad(df_copy['elat'])
    dist = df_copy['sy_dist']

    # Calculate Cartesian coordinate
    df_copy['cartesian_x'] = dist * np.cos(df_copy['elat_rad']) * np.cos(df_copy['elon_rad'])
    df_copy['cartesian_y'] = dist * np.cos(df_copy['elat_rad']) * np.sin(df_copy['elon_rad'])
    df_copy['cartesian_z'] = dist * np.sin(df_copy['elat_rad'])
    return df_copy


def convert_spectral_type(spectype):
    non_normal_types = {
        'DQ': 'D',
        'DC': 'D',
        'WD': 'D',
        'sdBV': 'B',
        'L1.5': 'L',
        'T8.5': 'T',
        'nan': 'Unknown'  
    }
    if spectype in non_normal_types:
        return non_normal_types[spectype]
    
    return spectype[0].upper()

def categorize_exoplanets_by_radius(radius):
    #set comparable planets in our solar system
    earth_r_e = 1
    neptune_r_e = 3.883
    saturn_r_e = 9.449
    if radius <= earth_r_e:
        return 'Terrestial'
    elif earth_r_e < radius < neptune_r_e:
        return 'Super-Earth'
    elif neptune_r_e < radius < saturn_r_e:
        return "Neptune-Like"
    elif saturn_r_e <= radius:
        return "Gas Giants"
    else: 
        return "Unknown"


def calculate_esi(df):
    S_earth = 1
    R_earth = 1
    S = df['pl_insol'].replace(0, np.nan)  
    R = df['pl_rade'].replace(0, np.nan)

    esi = 1 - np.sqrt(0.5 * (((S - S_earth) / (S + S_earth))**2 + ((R - R_earth) / (R + R_earth))**2))

    return esi