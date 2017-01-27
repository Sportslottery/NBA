__author__ = 'Shane_Kao'


import os
import time
import json
from datetime import datetime

import numpy as np
import pandas as pd

data = pd.DataFrame()
proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# proj_dict = 'F:/NBA'
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


def get_matchup_result(home_team, away_team, season_type, season_year, date):

    cond = (data['away_abbreviation'] == home_team) & (data['home_abbreviation'] == away_team) | \
           (data['away_abbreviation'] == away_team) & (data['home_abbreviation'] == home_team)

    df = data[cond][(data['season_type'] == season_type) & (data['season_year'] == season_year)][data['date'] < date]
    if df.shape[0] == 0:
        matchup_result = 0
    else:
        matchup_result = sum([1 if i == home_team else -1 for i in df['two_way_winner'].tolist()])
    return matchup_result

# get_matchup_result('LAL', "HOU", 2, 2017, 1483203600)

data['home_matchup_result'] = data.apply(lambda x: get_matchup_result(x['home_abbreviation'],
                                                                      x['away_abbreviation'],
                                                                      x['season_type'],
                                                                      x['season_year'],
                                                                      x['date']), axis=1)

result_list = data[['id', 'home_matchup_result']].T.to_dict().values()
result_dict = {}
for i in result_list:
    result_dict[str(i['id'])] = dict(filter(lambda x: x[0] != 'id', i.items()))


for year in range(2007, 2017):
    df = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ))
    if 'handicap_winner' in list(df.columns):
        df = df[['id', 'season_type', 'two_way_winner', 'handicap_winner', 'over_under_result',
             'home_line_margin', 'over_under']]
    else:
        df = df[['id', 'season_type', 'two_way_winner', 'over_under_result',
             'home_line_margin', 'over_under']]

    df['home_matchup_result'] = df['id'].apply(lambda x: result_dict.get(str(x), {}).get('home_matchup_result'))


    df.to_csv(os.path.dirname(__file__) + '/data/' + '%d.csv' %year, index=None)
    print year