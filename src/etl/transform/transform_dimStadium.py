import json
import pandas as pd
from pathlib import Path

# Build path to data/transformed directory
base_path = Path(__file__).resolve().parents[3]
jsons_path = base_path / 'data' / 'raw'
transformed_path = base_path / 'data' / 'transformed'

# Open json file
with open(jsons_path / 'stadium_coords.json', 'r', encoding='utf-8') as file:
    stadium_coords = json.load(file)

# Transform for df
rows = []
for team, stadium_info in stadium_coords.items():
    # Remove unnecessary chars
    connected_coords = stadium_info['coordinates'].replace('Point(', '').replace(')', '').split()
    
    # Cast float on coors
    connected_coords = list(map(float, connected_coords))
    rows.append({
        'name': stadium_info['stadium'],
        'lat': connected_coords[0],
        'lon': connected_coords[1]
    })

# Create dataframe
df = pd.DataFrame(rows)
df.insert(0, 'stadium_id', range(1, len(df) + 1))

# Create CSV
df.to_csv(transformed_path / 'dimStadium.csv', index=False, encoding='utf-8')