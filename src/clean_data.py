import os
import pandas as pd
import numpy as np
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


def calculate_ppq(row):
   if np.isnan(row['home.over_time']):
      row['home.ppq'] = row['home.total']/4
      row['away.ppq'] = row['away.total']/4
   elif not np.isnan(row['home.over_time']):
      row['home.ppq'] = row['home.total']/5
      row['away.ppq'] = row['away.total']/5

   return row


def home_win(row):
   if row['home.ppq'] > row['away.ppq']:
      row['home.win'] = 1
   else:
      row['home.win'] = 0
   
   return row


def to_df(all_teams):
   team_df = pd.DataFrame.from_dict(list(all_teams))
   team_df = team_df[['date', 'scores', 'teams','time']]
   return team_df


def clean_scores(team_df):
   scores_expand_df = pd.json_normalize(team_df['scores'])
   scores_expand_df = scores_expand_df.apply(calculate_ppq, axis=1)
   scores_expand_df = scores_expand_df.apply(home_win, axis=1)
   scores_expand_df = scores_expand_df[['home.ppq', 'away.ppq', 'home.win']]
   return scores_expand_df


def clean_teams(team_df):
   teams_expand_df = pd.json_normalize(team_df['teams'])
   teams_expand_df = teams_expand_df[['home.id', 'home.name', 'away.id', 'away.name']]
   return teams_expand_df


def clean_time(scores_teams_df):
   scores_teams_df['date'] = scores_teams_df['date'].apply(lambda x: x[:-9].replace('T', ' '))
   scores_teams_df['date'] = pd.to_datetime(scores_teams_df['date'], format='%Y-%m-%d %H:%M')
   scores_teams_df['day_of_week'] = scores_teams_df['date'].dt.dayofweek + 1
   scores_teams_df['hour'] = scores_teams_df['date'].dt.hour
   return scores_teams_df


team_df = to_df(all_teams)

scores_expand_df = clean_scores(team_df)
teams_expand_df = clean_teams(team_df)

scores_teams_df = pd.concat([team_df, teams_expand_df, scores_expand_df], axis=1)
clean_team_df = clean_time(scores_teams_df)
full_team_df = clean_team_df[['day_of_week', 'date', 'hour', 'home.id', 'home.ppq', 'away.id', 'away.ppq', 'home.win']]

# Trying to add average number of points teams score to the model. Accuracy doesn't seem to change much
home_grouped_df = full_team_df[full_team_df['date'] < '2022-02-01'].groupby('home.id').mean()['home.ppq']
home_grouped_dict = home_grouped_df.to_dict()
home_grouped_dict[1412] = 40.75 # all-star game
away_grouped_df = full_team_df[full_team_df['date'] < '2022-02-01'].groupby('away.id').mean()['away.ppq']
away_grouped_dict = away_grouped_df.to_dict()
away_grouped_dict[2511] = 40 # all-star game


def merge_group(row):
   row['home_avg_ppq'] = home_grouped_dict[row['home.id']]
   row['away_avg_ppq'] = away_grouped_dict[row['away.id']]
   return row


full_team_df = full_team_df.apply(merge_group, axis=1)
# print(full_team_df)