__author__ = 'shane'

import os
import sys
import json
import time
from datetime import datetime


import pandas as pd
import numpy as np

worst_season_winning_pct = float(7)/float(66)
best_season_winning_pct = float(73)/float(82)

worst_home_winning_pct = float(4)/float(33)
best_home_winning_pct = float(40)/float(41)

worst_away_winning_pct = float(1)/float(41)
best_away_winning_pct = float(34)/float(41)

# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
proj_dict = 'F:/NBA'
# print proj_dict

# year = 2016
def get_true_standing(year):
    api_df = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'home_total_pct', 'away_total_pct', 'home_home_pct',
                              'away_away_pct', 'two_way_winner'])

    last_n_df = pd.read_csv('%s/analytic/last_n/data/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'home_total_last_10_pct', 'away_total_last_10_pct',
                              'home_home_last_10_pct', 'away_away_last_10_pct'])
    df = pd.merge(api_df, last_n_df, on='id', how='left')

    df['home_total_pct'] = np.where(df['home_total_pct'].isnull(), 0.5,
                           np.where(df['home_total_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(df['home_total_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    df['home_total_pct'])))

    df['away_total_pct'] = np.where(df['away_total_pct'].isnull(), 0.5,
                           np.where(df['away_total_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(df['away_total_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    df['away_total_pct'])))

    df['home_home_pct'] = np.where(df['home_home_pct'].isnull(), 0.5,
                           np.where(df['home_home_pct'] > best_home_winning_pct, best_home_winning_pct,
                           np.where(df['home_home_pct'] < worst_home_winning_pct, worst_home_winning_pct,
                                    df['home_home_pct'])))

    df['away_away_pct'] = np.where(df['away_away_pct'].isnull(), 0.5,
                           np.where(df['away_away_pct'] > best_away_winning_pct, best_away_winning_pct,
                           np.where(df['away_away_pct'] < worst_away_winning_pct, worst_away_winning_pct,
                                    df['away_away_pct'])))

    df['home_total_last_10_pct'] = np.where(df['home_total_last_10_pct'].isnull(), 0.5,
                           np.where(df['home_total_last_10_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(df['home_total_last_10_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    df['home_total_last_10_pct'])))

    df['away_total_last_10_pct'] = np.where(df['away_total_last_10_pct'].isnull(), 0.5,
                           np.where(df['away_total_last_10_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(df['away_total_last_10_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    df['away_total_last_10_pct'])))

    df['home_home_last_10_pct'] = np.where(df['home_home_last_10_pct'].isnull(), 0.5,
                           np.where(df['home_home_last_10_pct'] > best_home_winning_pct, best_home_winning_pct,
                           np.where(df['home_home_last_10_pct'] < worst_home_winning_pct, worst_home_winning_pct,
                                    df['home_home_last_10_pct'])))

    df['away_away_last_10_pct'] = np.where(df['away_away_last_10_pct'].isnull(), 0.5,
                           np.where(df['away_away_last_10_pct'] > best_away_winning_pct, best_away_winning_pct,
                           np.where(df['away_away_last_10_pct'] < worst_away_winning_pct, worst_away_winning_pct,
                                    df['away_away_last_10_pct'])))

    df['home_total_winning_score'] = np.where(df['two_way_winner'] == 'home', df['away_total_pct']/(1 - df['away_total_pct']),
         -1 * (1 - df['away_total_pct'])/df['away_total_pct'])

    df['away_total_winning_score'] = np.where(df['two_way_winner'] == 'away', df['home_total_pct']/(1 - df['home_total_pct']),
         -1 * (1 - df['home_total_pct'])/df['home_total_pct'])

    df['home_home_winning_score'] = np.where(df['two_way_winner'] == 'home',
                                             df['away_away_pct']/(1 - df['away_away_pct']),
                                             -1 * (1 - df['away_away_pct'])/df['away_away_pct'])

    df['away_away_winning_score'] = np.where(df['two_way_winner'] == 'away',
                                             df['home_home_pct']/(1 - df['home_home_pct']),
                                             -1 * (1 - df['home_home_pct'])/df['home_home_pct'])

    df['lastN_home_total_winning_score'] = np.where(df['two_way_winner'] == 'home', df['away_total_last_10_pct']/(1 - df['away_total_last_10_pct']),
         -1 * (1 - df['away_total_last_10_pct'])/df['away_total_last_10_pct'])

    df['lastN_away_total_winning_score'] = np.where(df['two_way_winner'] == 'away', df['home_total_last_10_pct']/(1 - df['home_total_last_10_pct']),
         -1 * (1 - df['home_total_last_10_pct'])/df['home_total_last_10_pct'])

    df['lastN_home_home_winning_score'] = np.where(df['two_way_winner'] == 'home',
                                             df['away_away_last_10_pct']/(1 - df['away_away_last_10_pct']),
                                             -1 * (1 - df['away_away_last_10_pct'])/df['away_away_last_10_pct'])

    df['lastN_away_away_winning_score'] = np.where(df['two_way_winner'] == 'away',
                                             df['home_home_last_10_pct']/(1 - df['home_home_last_10_pct']),
                                             -1 * (1 - df['home_home_last_10_pct'])/df['home_home_last_10_pct'])

    df = df.loc[:, ['id',u'home_total_winning_score',
       u'away_total_winning_score', u'home_home_winning_score',
       u'away_away_winning_score', u'lastN_home_total_winning_score',
       u'lastN_away_total_winning_score', u'lastN_home_home_winning_score',
       u'lastN_away_away_winning_score']]

    return df

true_standing_df = pd.DataFrame()
for year in range(2007, 2017):
    df = get_true_standing(year)
    true_standing_df = true_standing_df.append(df)

data = pd.DataFrame()

for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_api/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'season_type', 'date'])
    print year
    data = data.append(api_df)

data.reset_index(inplace=True, drop=True)

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
    data['date'].tolist())
# data['two_way_winner'] = np.where(data['away_score'] > data['home_score'], data['away_abbreviation'], data['home_abbreviation'])

data = pd.merge(data, true_standing_df, on='id', how='left')

def get_last_N_game_score(team_name, season_type, season_year, date, last_n=10, game_type ='total'):
    if game_type == 'total':
        cond = (data['away_abbreviation'] == team_name) | (data['home_abbreviation'] == team_name)
    elif game_type == 'home':
        cond = data['home_abbreviation'] == team_name
    else:
        cond = data['away_abbreviation'] == team_name

    df = data[cond][(data['season_type'] == season_type) & (data['season_year'] == season_year)][data['date'] < date].tail(last_n)
    if df.shape[0] == 0:
        score_dict = {}
    else:
        if game_type == 'total':
            total_score = np.where(df['away_abbreviation'] == team_name, df['away_total_winning_score'],
                             df['home_total_winning_score'])
            lastN_score = np.where(df['away_abbreviation'] == team_name, df['lastN_away_total_winning_score'],
                             df['lastN_home_total_winning_score'])
        if game_type == 'home':
            total_score = df['home_home_winning_score'].tolist()
            lastN_score = df['lastN_home_home_winning_score'].tolist()
        if game_type == 'away':
            total_score = df['away_away_winning_score'].tolist()
            lastN_score = df['lastN_away_away_winning_score'].tolist()
        score_dict = {'total': total_score, 'lastN': lastN_score}
    return score_dict




for i in range(data.shape):
    away_team_name = data.loc[i, 'away_abbreviation']
    home_team_name = data.loc[i, 'home_abbreviation']
    season_type = data.loc[i, 'season_type']
    season_year = data.loc[i, 'season_year']
    date = data.loc[i, 'date']
    away_total_score_dict = get_last_N_game_score(away_team_name, season_type, season_year, date, last_n=10, game_type ='total')
    away_away_score_dict = get_last_N_game_score(away_team_name, season_type, season_year, date, last_n=10, game_type ='away')
    home_total_score_dict = get_last_N_game_score(home_team_name, season_type, season_year, date, last_n=10, game_type ='total')
    home_home_score_dict = get_last_N_game_score(home_team_name, season_type, season_year, date, last_n=10, game_type ='home')



data['away_total_last_1']
data['away_away_last_1']
data['away_lastN_last_1']

data['home_total_last_1']
data['home_home_last_1']
data['home_lastN_last_1']

