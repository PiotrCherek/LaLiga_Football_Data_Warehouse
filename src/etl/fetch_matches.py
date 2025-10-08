import requests, os, json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv("FOOTBALL_API_TOKEN")
assert TOKEN != 'your_token_here', 'FOOTBALL_API_TOKEN must be set in .env file'

BASE_URL = 'https://api.football-data.org/v4/competitions/PD/matches' # La Liga matches
HEADERS = {'X-Auth-Token': TOKEN}

def fetch_matches(season: str, matchday: int):
    parameters = {
        'season': season,
        'matchday': matchday
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=parameters)
    response.raise_for_status() # Raise an error for bad responses
    return response.json()

if __name__ == '__main__':
    # Build path to data/raw directory
    base_path = Path(__file__).resolve().parents[2]
    raw_data_path = base_path / 'data' / 'raw'

    # Ensure the raw data directory exists
    raw_data_path.mkdir(parents=True, exist_ok=True)

    # Fetch matches for a specific season and matchday
    season = '2024'
    matchday = 1
    matches = fetch_matches(season=season, matchday=matchday)

    # Saving in data/raw directory
    file_name = raw_data_path / f'matches_season_{season}_matchday_{matchday}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(matches, file, ensure_ascii=False, indent=2)
