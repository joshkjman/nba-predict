import requests
import sys
from pprint import pprint


base_url = 'https://v1.basketball.api-sports.io/'

payload = {}
headers = {
  'x-rapidapi-key': 'dd16c5ef6246e4ea91264f53be0209e4',
  'x-rapidapi-host': 'v1.basketball.api-sports.io'
}

league_response = requests.get(base_url + 'leagues', headers=headers, data=payload)
leagues = league_response.json()['response']

for league in leagues:
    if league['name'] == 'NBA':
        nba_id = int(league['id'])

game_response = requests.get(base_url + f'games?league={nba_id}&season=2021-2022', headers=headers, data=payload)
games = game_response.json()['response']

filter_games = []
for game in games:
    filter_keys = ['date', 'scores', 'teams', 'time']
    filter_games.append({key: game[key] for key in filter_keys})

print(sys.getsizeof(filter_games))