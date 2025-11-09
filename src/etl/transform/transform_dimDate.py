import json
import pandas as pd
from pathlib import Path

# Build path to data/transformed directory
base_path = Path(__file__).resolve().parents[3]
jsons_path = base_path / 'data' / 'raw'
transformed_path = base_path / 'data' / 'transformed'

def generate_dates(first_year: int, last_year: int) -> pd.DataFrame:
    date_list = []
    for year in range(first_year, last_year + 1):
        for month in range(1, 13):
            if month in [1, 3, 5, 7, 8, 10, 12]:
                days_in_month = 31
            elif month in [4, 6, 9, 11]:
                days_in_month = 30
            else:  # February
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    days_in_month = 29
                else:
                    days_in_month = 28
            for day in range(1, days_in_month + 1):
                date_list.append({'year': year,
                                  'month': month,
                                  'day': day})
    df_dates = pd.DataFrame(date_list)
    df_dates.insert(0, 'date_id', range(1, len(df_dates) + 1))
    return df_dates

# Create dataframe for 2024 
df = generate_dates(first_year=2024, last_year=2024)

# Create CSV
df.to_csv(transformed_path / 'dimDate.csv', index=False, encoding='utf-8')