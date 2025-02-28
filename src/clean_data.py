import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

db_password = os.environ.get('DB_PASSWORD')

uri = f"mongodb+srv://lollipopjosh:{db_password}@nba-cluster.upxg9.mongodb.net/?appName=nba-cluster"

def get_database():
   client = MongoClient(uri)
   return client['nba_db']

nba_db = get_database()
teams = nba_db['nba_teams']

all_teams = teams.find({})

team_df = pd.DataFrame.from_dict(list(all_teams))
team_df = team_df[['date', 'scores', 'teams','time']]
scores_expand_df = pd.json_normalize(team_df['scores'])

teams_expand_df = pd.json_normalize(team_df['teams'])
print(teams_expand_df)