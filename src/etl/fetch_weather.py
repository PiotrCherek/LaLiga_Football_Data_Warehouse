import json, requests, os
from pathlib import Path
from meteostat import Stations, Hourly
from datetime import datetime, timedelta


if __name__ == '__main__':
    # Getting paths for needed JSON files
    base_path = Path(__file__).resolve().parents[2]
    raw_data_path = base_path / 'data' / 'raw'
    matches_path = raw_data_path / 'matches_season_2024.json'
    stadium_coords_path = raw_data_path / 'stadium_coords.json'

    # Open JSON files
    with open(matches_path, 'r') as file:
        matches = json.load(file)
    with open(stadium_coords_path, 'r') as file:
        stadium_coords = json.load(file)

    weather_records = []
    
    for match in matches['matches']:
        # Time of the match
        match_date_time = match['utcDate']
        match_date = match_date_time[:10]
        
        # Getting specifics from date
        match_year = int(match_date[:4])
        match_month = int(match_date[5:7])
        match_day = int(match_date[8:10])
        
        # Getting specifics from time
        match_time = match_date_time[11:-1]
        match_hour = int(match_time[:2])
        match_minute = int(match_time[3:5])
        
        # Setting start and end time for weather data fetch
        start = datetime(match_year, match_month, match_day, match_hour, match_minute)
        end = start + timedelta(hours=2)

        # Where the match was
        home_team = match['homeTeam']['name']
        station_id = stadium_coords[home_team]['station_id']
        
        # Get weather data
        data = Hourly(station_id, start, end)
        data = data.fetch()
        if not data.empty:
            avg_weather = data.mean(numeric_only=True).to_dict()
        else:
            avg_weather = {}
        
        weather_record = {'match_id': match['id'], **avg_weather}
        weather_records.append(weather_record)
    
    # Save weather data to JSON
    file_name = base_path / 'data' / 'raw' / 'weather_data.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(weather_records, file, ensure_ascii=False, indent=2)