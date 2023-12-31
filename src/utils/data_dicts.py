import pandas as pd
from pathlib import Path


csv_path = Path(__file__).resolve().parents[2] / 'data' / 'predicted_prices_withzones.csv'

packages_dict = {
    '12 solar panels': {'system_cost': 87995 / 1.25, 'system_effect': 4.9},
    '25 solar panels': {'system_cost': 130999 / 1.25, 'system_effect': 10.3}, 
    '35 solar panels': {'system_cost': 164999 / 1.25, 'system_effect': 14.4}, 
    '45 solar panels': {'system_cost': 195999 / 1.25, 'system_effect': 18.5}
}

price_prognoses_df = pd.read_csv(csv_path)

years_list = list(price_prognoses_df['Year'])
years_list = list([2023] + years_list)

zone_1_predicted_prices = list(price_prognoses_df['zone1'])
zone_2_predicted_prices = list(price_prognoses_df['zone2'])
zone_3_predicted_prices = list(price_prognoses_df['zone3'])
zone_4_predicted_prices = list(price_prognoses_df['zone4'])

