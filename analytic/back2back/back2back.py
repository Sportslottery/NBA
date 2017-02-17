__author__ = 'shane'

import os
import time
import json
from datetime import datetime, timedelta


import pandas as pd
import numpy as np


# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
proj_dict = 'F:/NBA'
data = pd.DataFrame()
for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_api/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_score', 'home_score', 'season_type', 'date'])
    print year
    data = data.append(api_df)

data['date'] = data['date'].apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))

def back2back(team_name, date):
    df = data[(data['away_abbreviation'] == team_name)|(data['home_abbreviation'] == team_name)]
    df = df[df['date'] == date - timedelta(days=1)]
    return df.shape[0]

home_b2b = []
away_b2b = []
for i in range(data.shape[0]):
    print i, data.shape[0]
    home_b2b.append(back2back(data.iloc[i]['home_abbreviation'], data.iloc[i]['date']))
    away_b2b.append(back2back(data.iloc[i]['away_abbreviation'], data.iloc[i]['date']))

data['home_b2b'] = home_b2b
data['away_b2b'] = away_b2b

for year in range(2007, 2017):
    df = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ))
    if 'handicap_winner' in list(df.columns):
        df = df[['id', 'season_type', 'two_way_winner', 'handicap_winner', 'over_under_result',
             'home_line_margin', 'over_under']]
    else:
        df = df[['id', 'season_type', 'two_way_winner', 'over_under_result',
             'home_line_margin', 'over_under']]

    df = pd.merge(df, data.loc[:, ['id', u'home_b2b', u'away_b2b']], on='id', how='left')


    df.to_csv(proj_dict + '/analytic/back2back/data/' + '%d.csv' %year, index=None)
    print year