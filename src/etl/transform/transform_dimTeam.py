import json
import pandas as pd
from pathlib import Path

# Build path to data/transformed directory
base_path = Path(__file__).resolve().parents[3]
jsons_path = base_path / 'data' / 'raw'
transformed_path = base_path / 'data' / 'transformed'

# Open json file
with open(jsons_path / 'matches_season_2024.json', 'r', encoding='utf-8') as file:
    matches = json.load(file)

# Extract unique teams
unique_teams = []
for match in matches['matches']:
    home_team_name = match['homeTeam']['name']
    if home_team_name not in unique_teams:
        unique_teams.append(home_team_name)

# Create DataFrame with unique teams
unique = sorted(dict.fromkeys(unique_teams))
df = pd.DataFrame({'name': unique})
df.insert(0, 'team_id', range(1, len(df) + 1))

# Save DataFrame to CSV
df.to_csv(transformed_path / 'dimTeam.csv', index=False, encoding='utf-8')