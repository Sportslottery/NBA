__author__ = 'Shane_Kao'


import os
import time
import json
from datetime import datetime

import numpy as np
import pandas as pd

data = pd.DataFrame()
# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
proj_dict = 'F:/NBA'
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
    return df

get_matchup_result('LAL', "HOU", 2, 2017, date)