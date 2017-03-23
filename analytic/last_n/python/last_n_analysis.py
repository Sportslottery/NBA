__author__ = 'shane'

import os
import time
import json
from datetime import datetime


import pandas as pd
import numpy as np


proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

data = pd.DataFrame()

for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_api/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_score', 'home_score', 'season_type', 'date'])
    print year
    data = data.append(api_df)

data.reset_index(inplace=True, drop=True)

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
    data['date'].tolist())
data['two_way_winner'] = np.where(data['away_score'] > data['home_score'], data['away_abbreviation'], data['home_abbreviation'])

def get_last_N_game_result(team_name, season_type, season_year, date, last_n, game_type ='total'):
    if game_type == 'total':
        cond = (data['away_abbreviation'] == team_name) | (data['home_abbreviation'] == team_name)
    elif game_type == 'home':
        cond = data['home_abbreviation'] == team_name
    else:
        cond = data['away_abbreviation'] == team_name

    df = data[cond][(data['season_type'] == season_type) & (data['season_year'] == season_year)][data['date'] < date].tail(last_n)
    if df.shape[0] == 0:
        winning_pct = None
    else:
        winning_pct = float(df[df['two_way_winner'] == team_name].shape[0])/float(df.shape[0])
    return winning_pct


data['away_total_last_1_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=1,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_2_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=2,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_3_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 3,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_4_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 4,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_5_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 5,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_6_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 6,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_7_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 7,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_8_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 8,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_9_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 9,
                                                                             game_type = 'total') , axis=1)
data['away_total_last_10_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 10,
                                                                             game_type = 'total') , axis=1)




data['home_total_last_1_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=1,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_2_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=2,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_3_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 3,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_4_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 4,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_5_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 5,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_6_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 6,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_7_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 7,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_8_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 8,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_9_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 9,
                                                                             game_type = 'total') , axis=1)
data['home_total_last_10_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 10,
                                                                             game_type = 'total') , axis=1)



data['home_home_last_1_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=1,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_2_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=2,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_3_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 3,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_4_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 4,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_5_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 5,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_6_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 6,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_7_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 7,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_8_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 8,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_9_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 9,
                                                                             game_type = 'home') , axis=1)
data['home_home_last_10_pct'] = data.apply(lambda x: get_last_N_game_result(x['home_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 10,
                                                                             game_type = 'home') , axis=1)


data['away_away_last_1_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=1,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_2_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n=2,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_3_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 3,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_4_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 4,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_5_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 5,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_6_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 6,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_7_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 7,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_8_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 8,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_9_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 9,
                                                                             game_type = 'away') , axis=1)
data['away_away_last_10_pct'] = data.apply(lambda x: get_last_N_game_result(x['away_abbreviation'], x['season_type'],
                                                                             x['season_year'], x['date'], last_n = 10,
                                                                             game_type = 'away') , axis=1)

result_list = data[filter(lambda x: '_pct' in x, data.columns.tolist()) + ['id']].T.to_dict().values()
result_dict = {}
for i in result_list:
    result_dict[i['id']] = dict(filter(lambda x: x[0] != 'id', i.items()))

with open('last_n_result.json', 'w') as fp:
    json.dump(result_dict, fp)