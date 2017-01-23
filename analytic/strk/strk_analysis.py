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


away_total_strk = home_total_strk = [None for i in range(data.shape[0])]


for i in range(data.shape[0]):
    print i, data.shape[0]
    home_team = data.iloc[i, :]['home_abbreviation']
    away_team = data.iloc[i, :]['away_abbreviation']
    home_last_df = data[(data['away_abbreviation'] == home_team)|(data['home_abbreviation'] == home_team)] \
                       [(data['season_type'] == data.iloc[i, :]['season_type']) &
                        (data['season_year'] == data.iloc[i, :]['season_year'])] \
                       [data['date'] < data.iloc[i, :]['date']].tail(1)
    away_last_df = data[(data['away_abbreviation'] == away_team)|(data['home_abbreviation'] == away_team)] \
                       [(data['season_type'] == data.iloc[i, :]['season_type']) &
                        (data['season_year'] == data.iloc[i, :]['season_year'])] \
                       [data['date'] < data.iloc[i, :]['date']].tail(1)
    if home_last_df.shape[0] == 0:
        home_total_strk[i] = 0
    elif away_last_df.shape[0] == 0:
        away_total_strk[i] = 0
    else:
        if home_last_df.iloc[0]['home_abbreviation'] == home_team:
            if int(home_last_df['home_total_strk']) >= 0:
                if home_last_df.iloc[0]['two_way_winner'] == home_team:
                     home_total_strk[i] = int(home_last_df['home_total_strk']) + 1
                else:
                    home_total_strk[i] = -1
            else:
                if home_last_df.iloc[0]['two_way_winner'] == home_team:
                     home_total_strk[i] = 1
                else:
                    home_total_strk[i] = int(home_last_df['home_total_strk']) - 1
        elif home_last_df.iloc[0]['away_abbreviation'] == home_team:
            if int(home_last_df['away_total_strk']) >= 0:
                if home_last_df.iloc[0]['two_way_winner'] == home_team:
                     home_total_strk[i] = int(home_last_df['away_total_strk']) + 1
                else:
                    home_total_strk[i] = -1
            else:
                if home_last_df.iloc[0]['two_way_winner'] == home_team:
                     home_total_strk[i] = 1
                else:
                    home_total_strk[i] = int(home_last_df['away_total_strk']) - 1

        elif away_last_df.iloc[0]['home_abbreviation'] == away_team:
            if int(away_last_df['home_total_strk']) >= 0:
                if away_last_df.iloc[0]['two_way_winner'] == away_team:
                     away_total_strk[i] = int(away_last_df['home_total_strk']) + 1
                else:
                    away_total_strk[i] = -1
            else:
                if away_last_df.iloc[0]['two_way_winner'] == away_team:
                     away_total_strk[i] = 1
                else:
                    away_total_strk[i] = int(away_last_df['home_total_strk']) - 1
        elif away_last_df.iloc[0]['away_abbreviation'] == away_team:
            if int(away_last_df['away_total_strk']) >= 0:
                if away_last_df.iloc[0]['two_way_winner'] == away_team:
                     away_total_strk[i] = int(away_last_df['away_total_strk']) + 1
                else:
                    away_total_strk[i] = -1
            else:
                if away_last_df.iloc[0]['two_way_winner'] == away_team:
                     away_total_strk[i] = 1
                else:
                    away_total_strk[i] = int(away_last_df['away_total_strk']) - 1
        # if int(home_last_df['home_total_strk']) >= 0:
        #     if home_last_df.iloc[0]['two_way_winner'] == home_team:
        #         if home_last_df.iloc[0]['home_abbreviation'] == home_team:
        #             home_total_strk[i] = int(home_last_df['home_total_strk']) + 1
        #         else:
        #             home_total_strk[i] = int(home_last_df['away_total_strk']) + 1
        #     else:
        #         home_total_strk[i] = -1
        # else:
        #     if home_last_df.iloc[0]['two_way_winner'] == home_team:
        #         home_total_strk[i] = 1
        #     else:
        #         if home_last_df.iloc[0]['home_abbreviation'] == home_team:
        #             home_total_strk[i] = int(home_last_df['home_total_strk']) - 1
        #         else:
        #             home_total_strk[i] = int(home_last_df['away_total_strk']) - 1


    data['home_total_strk'] = home_total_strk
    data['away_total_strk'] = away_total_strk

data.to_csv('a.csv')
