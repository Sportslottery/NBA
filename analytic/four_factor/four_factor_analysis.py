__author__ = 'Shane_Kao'

import os
import time
import json
from datetime import datetime


import pandas as pd
import numpy as np

data1 = pd.DataFrame()
data2 = pd.DataFrame()

# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
proj_dict = 'F:\NBA'

for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_api/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_3PM', 'away_FGA', 'away_FGM', 'away_FTA', 'away_FTM',
                              'home_3PM', 'home_FGA', 'home_FGM', 'home_FTA', 'home_FTM',
                              'season_type', 'date'])
    print year
    data1 = data1.append(api_df)

for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_boxscore/%d.csv' %(proj_dict, year, ))
    print year
    data2 = data2.append(api_df)

data1.reset_index(inplace=True, drop=True)
data2.reset_index(inplace=True, drop=True)

data = pd.merge(data1, data2, on='id', how='left')

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
                    data['date'].tolist())
defensive_game_type_dict = {'home': 'away', 'away': 'home'}
def get_last_N_game_four_factor(team_name, season_type, season_year, date, last_n=10, game_type ='total'):
    result_dict = {}
    if game_type == 'total':
        cond = (data['away_abbreviation'] == team_name) | (data['home_abbreviation'] == team_name)
    elif game_type == 'home':
        cond = data['home_abbreviation'] == team_name
    else:
        cond = data['away_abbreviation'] == team_name
    df = data[cond][(data['season_type'] == season_type) &
                    (data['season_year'] == season_year)][data['date'] < date].tail(last_n)

    if df.shape[0] == 0:
        for ln in range(1, 11):
            result_dict['offensive_efg_last%d' %(ln, )] = None
            result_dict['offensive_tov_last%d' %(ln, )] = None
            result_dict['offensive_rb_last%d' %(ln, )] = None
            result_dict['offensive_ftfga_last%d' %(ln, )] = None
            result_dict['defensive_efg_last%d' %(ln, )] = None
            result_dict['defensive_tov_last%d' %(ln, )] = None
            result_dict['defensive_rb_last%d' %(ln, )] = None
            result_dict['defensive_ftfga_last%d' %(ln, )] = None
    else:
        if game_type == 'total':
            offensive_ftm_cnt = np.where(df['home_abbreviation'] == team_name, df['home_FTM'],
                                        df['away_FTM']).tolist()
            defensive_ftm_cnt = np.where(df['home_abbreviation'] == team_name, df['away_FTM'],
                                        df['home_FTM']).tolist()

            offensive_tov_cnt = np.where(df['home_abbreviation'] == team_name, df['home_TO'],
                                        df['away_TO']).tolist()
            defensive_tov_cnt = np.where(df['home_abbreviation'] == team_name, df['away_TO'],
                                        df['home_TO']).tolist()

            offensive_fta_cnt = np.where(df['home_abbreviation'] == team_name, df['home_FTA'],
                                        df['away_FTA']).tolist()
            defensive_fta_cnt = np.where(df['home_abbreviation'] == team_name, df['away_FTA'],
                                        df['home_FTA']).tolist()

            offensive_fg_cnt = np.where(df['home_abbreviation'] == team_name, df['home_FGM'],
                                        df['away_FGM']).tolist()
            defensive_fg_cnt = np.where(df['home_abbreviation'] == team_name, df['away_FGM'],
                                        df['home_FGM']).tolist()
            offensive_3p_cnt = np.where(df['home_abbreviation'] == team_name, df['home_3PM'],
                                        df['away_3PM']).tolist()
            defensive_3p_cnt = np.where(df['home_abbreviation'] == team_name, df['away_3PM'],
                                        df['home_3PM']).tolist()
            offensive_fga_cnt = np.where(df['home_abbreviation'] == team_name, df['home_FGA'],
                                        df['away_FGA']).tolist()
            defensive_fga_cnt = np.where(df['home_abbreviation'] == team_name, df['away_FGA'],
                                        df['home_FGA']).tolist()
            for ln in range(1, 11):
                _offensive_fg_cnt = sum(offensive_fg_cnt[-ln:])
                _offensive_3p_cnt = sum(offensive_3p_cnt[-ln:])
                _offensive_fga_cnt = sum(offensive_fga_cnt[-ln:])
                _offensive_tov_cnt = sum(offensive_tov_cnt[-ln:])
                _offensive_fta_cnt = sum(offensive_fta_cnt[-ln:])
                _offensive_ftm_cnt = sum(offensive_ftm_cnt[-ln:])
                _defensive_fg_cnt = sum(defensive_fg_cnt[-ln:])
                _defensive_3p_cnt = sum(defensive_3p_cnt[-ln:])
                _defensive_fga_cnt = sum(defensive_fga_cnt[-ln:])
                _defensive_tov_cnt = sum(defensive_tov_cnt[-ln:])
                _defensive_fta_cnt = sum(defensive_fta_cnt[-ln:])
                _defensive_ftm_cnt = sum(defensive_ftm_cnt[-ln:])
                result_dict['offensive_ftfga_last%d' %(ln, )] = \
                    float(_offensive_ftm_cnt) / _offensive_fga_cnt
                result_dict['defensive_ftfga_last%d' %(ln, )] = \
                    float(_defensive_ftm_cnt) / _defensive_fga_cnt

                result_dict['offensive_efg_last%d' %(ln, )] = \
                    float(_offensive_fg_cnt + 0.5 * _offensive_3p_cnt) / _offensive_fga_cnt
                result_dict['defensive_efg_last%d' %(ln, )] = \
                    float(_defensive_fg_cnt + 0.5 * _defensive_3p_cnt) / _defensive_fga_cnt
                result_dict['offensive_tov_last%d' %(ln, )] = \
                    float(_offensive_tov_cnt) / (_offensive_fga_cnt + _offensive_tov_cnt +
                                                 0.44 * _offensive_fta_cnt)
                result_dict['defensive_tov_last%d' %(ln, )] = \
                    float(_defensive_tov_cnt) / (_defensive_fga_cnt + _defensive_tov_cnt +
                                                 0.44 * _defensive_fta_cnt)
        else:
            for ln in range(1, 11):
                _offensive_fg_cnt = sum(df['%s_FGM' %(game_type, )][-ln:])
                _offensive_3p_cnt = sum(df['%s_3PM' %(game_type, )][-ln:])
                _offensive_fga_cnt = sum(df['%s_FGA' %(game_type, )][-ln:])
                _offensive_tov_cnt = sum(df['%s_TO' %(game_type, )][-ln:])
                _offensive_fta_cnt = sum(df['%s_FTA' %(game_type, )][-ln:])
                _offensive_ftm_cnt = sum(df['%s_FTM' %(game_type, )][-ln:])

                _defensive_fg_cnt = sum(df['%s_FGM' %(defensive_game_type_dict[game_type], )][-ln:])
                _defensive_3p_cnt = sum(df['%s_3PM' %(defensive_game_type_dict[game_type], )][-ln:])
                _defensive_fga_cnt = sum(df['%s_FGA' %(defensive_game_type_dict[game_type], )][-ln:])
                _defensive_tov_cnt = sum(df['%s_TO' %(defensive_game_type_dict[game_type], )][-ln:])
                _defensive_fta_cnt = sum(df['%s_FTA' %(defensive_game_type_dict[game_type], )][-ln:])
                _defensive_ftm_cnt = sum(df['%s_FTM' %(defensive_game_type_dict[game_type], )][-ln:])

                result_dict['offensive_efg_last%d' %(ln, )] = \
                    float(_offensive_fg_cnt + 0.5 * _offensive_3p_cnt) / _offensive_fga_cnt
                result_dict['defensive_efg_last%d' %(ln, )] = \
                    float(_defensive_fg_cnt + 0.5 * _defensive_3p_cnt) / _defensive_fga_cnt

                result_dict['offensive_tov_last%d' %(ln, )] = \
                    float(_offensive_tov_cnt) / (_offensive_fga_cnt + _offensive_tov_cnt +
                                                 0.44 * _offensive_fta_cnt)
                result_dict['defensive_tov_last%d' %(ln, )] = \
                    float(_defensive_tov_cnt) / (_defensive_fga_cnt + _defensive_tov_cnt +
                                                 0.44 * _defensive_fta_cnt)

                result_dict['offensive_ftfga_last%d' %(ln, )] = \
                    float(_offensive_ftm_cnt) / _offensive_fga_cnt
                result_dict['defensive_ftfga_last%d' %(ln, )] = \
                    float(_defensive_ftm_cnt) / _defensive_fga_cnt

    return result_dict


get_last_N_game_four_factor(team_name='LAC', season_type=2, season_year=2017,
                            date=1483203600, last_n=10, game_type='home')

