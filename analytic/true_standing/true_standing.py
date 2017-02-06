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

api_df['home_total_pct'] = np.where(api_df['home_total_pct'].isnull(), 0.5,
                           np.where(api_df['home_total_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(api_df['home_total_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    api_df['home_total_pct'])))

api_df['away_total_pct'] = np.where(api_df['away_total_pct'].isnull(), 0.5,
                           np.where(api_df['away_total_pct'] > best_season_winning_pct, best_season_winning_pct,
                           np.where(api_df['away_total_pct'] < worst_season_winning_pct, worst_season_winning_pct,
                                    api_df['away_total_pct'])))

api_df['home_home_pct'] = np.where(api_df['home_home_pct'].isnull(), 0.5,
                           np.where(api_df['home_home_pct'] > best_home_winning_pct, best_home_winning_pct,
                           np.where(api_df['home_home_pct'] < worst_home_winning_pct, worst_home_winning_pct,
                                    api_df['home_home_pct'])))

api_df['away_away_pct'] = np.where(api_df['away_away_pct'].isnull(), 0.5,
                           np.where(api_df['away_away_pct'] > best_away_winning_pct, best_away_winning_pct,
                           np.where(api_df['away_away_pct'] < worst_away_winning_pct, worst_away_winning_pct,
                                    api_df['away_away_pct'])))