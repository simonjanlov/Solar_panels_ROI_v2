import pandas as pd


packages_dict = {
    '12 solar panels': {'system_cost': 87995 / 1.25, 'system_effect': 4.9},
    '25 solar panels': {'system_cost': 130999 / 1.25, 'system_effect': 10.3}, 
    '35 solar panels': {'system_cost': 164999 / 1.25, 'system_effect': 14.4}, 
    '45 solar panels': {'system_cost': 195999 / 1.25, 'system_effect': 18.5}
}

elpris_df = pd.read_csv(r'data\predicted_prices_withzones.csv')

years_list = list(elpris_df['Year'])
years_list = list([2023] + years_list)

zone_1_predicted_prices = list(elpris_df['zone1'])
zone_2_predicted_prices = list(elpris_df['zone2'])
zone_3_predicted_prices = list(elpris_df['zone3'])
zone_4_predicted_prices = list(elpris_df['zone4'])

