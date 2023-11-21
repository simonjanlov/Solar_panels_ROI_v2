# script for calling the PVGIS API with a get request for getting the irradiation/insolation data
# for any location by logitude and latitude

import requests

# minimum:
# https://re.jrc.ec.europa.eu/api/MRcalc?lat=45&lon=8&horirrad=1

def get_pvgis_data(lat, lon):

    # api-endpoint
    URL = "https://re.jrc.ec.europa.eu/api/MRcalc"
    raddatabase = "PVGIS-COSMO"
    horirrad = '1'
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'lat': lat,
              'lon': lon,
              'raddatabase': raddatabase,
              'horirrad': horirrad}
    
    # sending get request and saving the response as response object
    response = requests.get(url = URL, params = PARAMS)
    
    csv_data = response.text
    return csv_data


if __name__=="__main__":

    lat = '56.855'
    lon = '12.691'

    print(get_pvgis_data(lat, lon))