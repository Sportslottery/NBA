__author__ = 'Shane_Kao'

import time
from datetime import datetime

import numpy as np
import pandas as pd

data = pd.DataFrame()

for year in range(2016, 2017):
    api_df = pd.read_csv('F:/NBA/crawler/data/espn_api/%d.csv' %(year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_score', 'home_score', 'season_type', 'date'])
    print year
    data = data.append(api_df)

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
    data['date'].tolist())
data['two_way_winner'] = np.where(data['away_score'] > data['home_score'], data['away_abbreviation'], data['home_abbreviation'])
data['home_total_strk'] = data['away_total_strk'] = data['home_home_strk'] = data['away_away_strk'] = [None for i in range(data.shape[0])]

def get_last_game_result(team_name, season_type, season_year, date, game_type ='total'):
    if game_type == 'total':
        cond = (data['away_abbreviation'] == team_name) | (data['home_abbreviation'] == team_name)
    elif game_type == 'home':
        cond = data['home_abbreviation'] == team_name
    else:
        cond = data['away_abbreviation'] == team_name

    df = data[cond][(data['season_type'] == season_type) & (data['season_year'] == season_year)][data['date'] < date].tail(1)
    if df.shape[0] == 0:
        game_result = None
    else:
        if df.iloc[0]['two_way_winner'] == team_name:
            game_result = 'W'
        else:
            game_result = 'L'
    return game_result

data['away_last_total_result'] = data.apply(lambda x: get_last_game_result(x['away_abbreviation'], x['season_type'], x['season_year'], x['date'],
                                                                           game_type = 'total') , axis=1)
data['home_last_total_result'] = data.apply(lambda x: get_last_game_result(x['home_abbreviation'], x['season_type'], x['season_year'], x['date'],
                                                                           game_type = 'total') , axis=1)

data['home_last_home_result'] = data.apply(lambda x: get_last_game_result(x['home_abbreviation'], x['season_type'], x['season_year'], x['date'],
                                                                          game_type = 'home') , axis=1)
data['away_last_away_result'] = data.apply(lambda x: get_last_game_result(x['away_abbreviation'], x['season_type'], x['season_year'], x['date'],
                                                                          game_type = 'away') , axis=1)


# def get_last_game_strk(team_name, season_type, season_year, date, game_type ='total')

for i in range(100): #data.shape[0]
    print i
    if not data.iloc[i]['home_last_total_result']:
        data.set_value(i, 'home_total_strk', 0)
    if not data.iloc[i]['away_last_total_result']:
        data.set_value(i, 'away_total_strk', 0)
    if not data.iloc[i]['home_last_home_result']:
        data.set_value(i, 'home_home_strk', 0)
    if not data.iloc[i]['away_last_away_result']:
        data.set_value(i, 'away_away_strk', 0)


data.to_csv('a.csv')
