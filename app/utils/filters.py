import pandas as pd


#basically just a bunch of filters that filter exoplanets depending on method
def filt_by_dist(data, distance_threshold):
    """
    filters by a certain distance threshold

    Parameters:
    data: exoplanet data
    distance_threshold: distance limit in parsec

    Returns:
    dataframe containing only exoplanets within that distance threshold"""

    filtered_exoplanets = data[data['sy_dist'] <= distance_threshold.dropna(subset=['sy_dist'])]
    return filtered_exoplanets

def filt_by_dia_and_wavelength(data, telescope_diameter, wavelength):
    """
    filters exoplanets based on telescope diameter and wavelength.

    Parameters:
    data: exoplanet data
    telescope_diameter: diameter of the telescope in meteres
    wavelength: wavelength of light in micrometers

    Returns:
    dataframe with exoplanets that can be observed based on angular resolution.
    
    """
    #convert from micrometer to meter
    wavelength_meters = wavelength * 1e-6


    #calculate angular resolution (in radians)
    angular_resolution = (1.22*wavelength_meters) / telescope_diameter

    #convert radians to arcseconds (unit of angular measurement commonly used in astronomy to measure visible size in the sky) (multiply by 206265 to convert)
    angular_resolution_arcseconds = angular_resolution * 206265

    #filter by this measurement
    filtered_exoplanets = data[data['pl_angsep'].astype(float) > angular_resolution_arcseconds]
    return filtered_exoplanets


    