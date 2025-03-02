from clean_data import full_team_df
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score


train = full_team_df[full_team_df['date'] < '2022-02-01']
test = full_team_df[full_team_df['date'] > '2022-02-01']

X_train = train[['day_of_week', 'hour', 'home.id', 'home_avg_ppq', 'away.id', 'away_avg_ppq']]
y_train = train['home.win']
X_test = test[['day_of_week', 'hour', 'home.id', 'home_avg_ppq', 'away.id', 'away_avg_ppq']]
y_test = test['home.win']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
rf.fit(X_train, y_train)

predictions = rf.predict(X_test)

acc = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
print(f'Accuracy of model: {acc}')
print(f'Prob of who we expected to win, and actually won: {precision}')