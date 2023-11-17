import pandas as pd
import io

from PVGIS_API_request import get_pvgis_data
from city_to_lat_lon import city_to_lat_lon


def coordinates_to_insolation_mean(city_name):
    
    # Convert city name to coordinates
    lat, lon = city_to_lat_lon(city_name)

    # Call API and save csv data in buffer
    data = get_pvgis_data(lat, lon)
    buffer = io.StringIO(data)

    # Create dataframe from buffer and clean up
    df = pd.read_csv(filepath_or_buffer=buffer, sep='\t\t', engine='python', header=3)
    df.drop(df.index[-3:],inplace=True)
    df.rename(columns={'H(h)_m':'ghi'},inplace=True) # ghi = global horizontal irradiation
    
    # Sum months to get total per year. Then return the yearly mean value
    df_sum_ghi = df.groupby('year').sum('ghi')
    
    return df_sum_ghi.ghi.mean()
    


if __name__=='__main__':


    print(coordinates_to_insolation_mean('Göteborg'))
