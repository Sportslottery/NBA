__author__ = 'Shane_Kao'

import time
from datetime import datetime

import pandas as pd

data = pd.DataFrame()

for year in range(2006, 2017):
    api_df = pd.read_csv('F:/NBA/crawler/data/espn_api/%d.csv' %(year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_score', 'home_score', 'season_type', 'date'])
    print year
    data = data.append(api_df)

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
    data['date'].tolist())
data['two_way_winner'] = data[['away_score','home_score']].apply(lambda x: 'away' if x[0] > x[1] else 'home', axis=1)

df = data[(data['away_abbreviation'] == 'DET')|(data['home_abbreviation'] == 'DET')]
df = df[(df['season_type'] == 2)&(df['season_year'] == 2016)]

df = df[df['date'] < 1447005600].tail(1)