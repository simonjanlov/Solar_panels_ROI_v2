import pandas as pd
from pathlib import Path


def find_tilt_and_direction_value(tilt, direction):
    """Input tilt as an integer and direction as a string to return a
    float value for combined tilt and direction"""
    csv_path = Path(__file__).resolve().parents[2] / 'data' / 'tilt_and_direction_table.csv'
    df = pd.read_csv(csv_path, delimiter=';', index_col='Lutning')
    return df[direction][tilt] / 100



if __name__=='__main__':
    print(find_tilt_and_direction_value(20, '225 SV'))
