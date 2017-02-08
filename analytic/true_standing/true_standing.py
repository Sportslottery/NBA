__author__ = 'shane'

import os
import sys
import json


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
print proj_dict

year = 2016

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