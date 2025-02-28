from pymongo import MongoClient
from dotenv import load_dotenv
from api_call import filter_games
import os 


load_dotenv()

db_password = os.environ.get('DB_PASSWORD')

uri = f"mongodb+srv://lollipopjosh:{db_password}@nba-cluster.upxg9.mongodb.net/?appName=nba-cluster"

def get_database():
   client = MongoClient(uri)
   return client['nba_db']

nba_db = get_database()
teams = nba_db['nba_teams']

for game in filter_games:
   teams.insert_one(game)

print(nba_db.command('dbstats'))