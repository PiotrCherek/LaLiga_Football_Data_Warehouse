import json, requests, os
from pathlib import Path
from meteostat import Point, Hourly


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
    
    for match in matches['matches']:
        # Time of the match
        match_date_time = match['utcDate']
        match_date = match_date_time[:10]
        match_time = match_date_time[11:-1]
        
        # Where the match was
        home_team = match['homeTeam']['name']
        location = stadium_coords[home_team]['coordinates']
        