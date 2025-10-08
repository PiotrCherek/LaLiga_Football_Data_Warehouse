import json, requests, os
from pathlib import Path

def get_teams_stadium_coords(teams: list) -> dict:
    # Escape double quotes in team names
    teams_escaped = [team.replace('"', '\\"') for team in teams]
    filter_clause = " || ".join([f'?teamLabel = "{team}"@en' for team in teams_escaped])
    url = "https://query.wikidata.org/sparql"
    headers = {'Accept': 'application/sparql-results+json'}

    query = f"""
    SELECT ?teamLabel ?stadiumLabel ?coord WHERE {{
        ?team rdfs:label ?teamLabel.
        ?team wdt:P115 ?stadium.
        ?stadium wdt:P625 ?coord.
        FILTER ({filter_clause})
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """

    response = requests.get(url, headers=headers, params={'query': query})
    response.raise_for_status()
    data = response.json()
    results = data['results']['bindings']

    coords_dict = {}
    for result in results:
        team = result['teamLabel']['value']
        stadium = result['stadiumLabel']['value']
        coord = result['coord']['value']
        coords_dict[team] = {'stadium': stadium, 'coordinates': coord}

    return coords_dict

if __name__ == '__main__':
    base_path = Path(__file__).resolve().parents[2]
    matches_json_path = base_path / 'data' / 'raw' / 'matches_season_2024.json'

    with open(matches_json_path, 'r') as file:
        matches = json.load(file)

    unique_teams = []
    for match in matches['matches']:
        home_team_name = match['homeTeam']['name']
        if home_team_name not in unique_teams:
            unique_teams.append(home_team_name)
    unique_teams = sorted(unique_teams)

    stadium_coords = get_teams_stadium_coords(unique_teams)
    file_name = base_path / 'data' / 'raw' / 'stadium_coords.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(stadium_coords, file, ensure_ascii=False, indent=2)