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
    api_df = api_df.replace('--', np.nan)
    data2 = data2.append(api_df)

data1.reset_index(inplace=True, drop=True)
data2.reset_index(inplace=True, drop=True)

data = pd.merge(data1, data2, on='id', how='left')

data['date'] = map(lambda x: time.mktime(datetime.strptime(x, '%Y-%m-%dT%H:%MZ').timetuple()),
                    data['date'].tolist())

data['away_DREB'] = data['away_DREB'].apply(lambda x: x if pd.isnull(x) else int(x))
data['away_OREB'] = data['away_OREB'].apply(lambda x: x if pd.isnull(x) else int(x))
data['away_TO'] = data['away_TO'].apply(lambda x: x if pd.isnull(x) else int(x))

data = data.fillna(data.mean())

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
            orb_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_OREB'],
                                        df['away_OREB']).tolist())
            opp_drb_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_DREB'],
                                        df['home_DREB']).tolist())
            drb_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_DREB'],
                                        df['away_DREB']).tolist())
            opp_orb_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_OREB'],
                                        df['home_OREB']).tolist())

            offensive_ftm_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_FTM'],
                                        df['away_FTM']).tolist())
            defensive_ftm_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_FTM'],
                                        df['home_FTM']).tolist())

            offensive_tov_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_TO'],
                                        df['away_TO']).tolist())
            defensive_tov_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_TO'],
                                        df['home_TO']).tolist())

            offensive_fta_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_FTA'],
                                        df['away_FTA']).tolist())
            defensive_fta_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_FTA'],
                                        df['home_FTA']).tolist())

            offensive_fg_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_FGM'],
                                        df['away_FGM']).tolist())
            defensive_fg_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_FGM'],
                                        df['home_FGM']).tolist())
            offensive_3p_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_3PM'],
                                        df['away_3PM']).tolist())
            defensive_3p_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_3PM'],
                                        df['home_3PM']).tolist())
            offensive_fga_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['home_FGA'],
                                        df['away_FGA']).tolist())
            defensive_fga_cnt = map(int, np.where(df['home_abbreviation'] == team_name, df['away_FGA'],
                                        df['home_FGA']).tolist())
            for ln in range(1, 11):
                _drb_cnt = sum(drb_cnt[-ln:])
                _opp_orb_cnt = sum(opp_orb_cnt[-ln:])
                _orb_cnt = sum(orb_cnt[-ln:])
                _opp_drb_cnt = sum(opp_drb_cnt[-ln:])
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
                result_dict['offensive_rb_last%d' %(ln, )] = \
                    float(_orb_cnt) / (_orb_cnt + _opp_drb_cnt)

                result_dict['defensive_rb_last%d' %(ln, )] = \
                    float(_drb_cnt) / (_drb_cnt + _opp_orb_cnt)

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
                _orb_cnt = sum(map(int, df['%s_OREB' %(game_type, )][-ln:]))
                _offensive_fg_cnt = sum(map(int, df['%s_FGM' %(game_type, )][-ln:]))

                _drb_cnt = sum(map(int, df['%s_DREB' %(game_type, )][-ln:]))

                _offensive_3p_cnt = sum(map(int, df['%s_3PM' %(game_type, )][-ln:]))
                _offensive_fga_cnt = sum(map(int, df['%s_FGA' %(game_type, )][-ln:]))
                _offensive_tov_cnt = sum(map(int, df['%s_TO' %(game_type, )][-ln:]))
                _offensive_fta_cnt = sum(map(int, df['%s_FTA' %(game_type, )][-ln:]))
                _offensive_ftm_cnt = sum(map(int, df['%s_FTM' %(game_type, )][-ln:]))

                _opp_drb_cnt = sum(map(int, df['%s_DREB' %(defensive_game_type_dict[game_type], )][-ln:]))
                _opp_orb_cnt = sum(map(int, df['%s_OREB' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_fg_cnt = sum(map(int, df['%s_FGM' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_3p_cnt = sum(map(int, df['%s_3PM' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_fga_cnt = sum(map(int, df['%s_FGA' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_tov_cnt = sum(map(int, df['%s_TO' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_fta_cnt = sum(map(int, df['%s_FTA' %(defensive_game_type_dict[game_type], )][-ln:]))
                _defensive_ftm_cnt = sum(map(int, df['%s_FTM' %(defensive_game_type_dict[game_type], )][-ln:]))

                result_dict['defensive_rb_last%d' %(ln, )] = \
                    float(_drb_cnt) / (_drb_cnt + _opp_orb_cnt)
                result_dict['offensive_rb_last%d' %(ln, )] = \
                    float(_orb_cnt) / (_orb_cnt + _opp_drb_cnt)

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





df = data.loc[:, ['id', 'date', 'season_type', 'season_year', 'away_abbreviation',
                  'home_abbreviation']]

result_list = df.T.to_dict().values()


get_last_N_game_four_factor(team_name='LAC',
                                             season_type=2,
                                             season_year=2016,
                                             date=1160578800,
                                             last_n=10,
                                             game_type='total')

for j ,i in enumerate(result_list[:]):
    print j, len(result_list)
    home_total = get_last_N_game_four_factor(team_name=i['home_abbreviation'],
                                             season_type=i['season_type'],
                                             season_year=i['season_year'],
                                             date=i['date'],
                                             last_n=10,
                                             game_type='total')
    home_total = dict(map(lambda x: ('home_total_' + x[0], x[1]), home_total.items()))
    away_total = get_last_N_game_four_factor(team_name=i['away_abbreviation'],
                                             season_type=i['season_type'],
                                             season_year=i['season_year'],
                                             date=i['date'],
                                             last_n=10,
                                             game_type='total')
    away_total = dict(map(lambda x: ('away_total_' + x[0], x[1]), away_total.items()))
    home_home = get_last_N_game_four_factor(team_name=i['home_abbreviation'],
                                             season_type=i['season_type'],
                                             season_year=i['season_year'],
                                             date=i['date'],
                                             last_n=10,
                                             game_type='home')
    home_home = dict(map(lambda x: ('home_home_' + x[0], x[1]), home_home.items()))
    away_away = get_last_N_game_four_factor(team_name=i['away_abbreviation'],
                                             season_type=i['season_type'],
                                             season_year=i['season_year'],
                                             date=i['date'],
                                             last_n=10,
                                             game_type='away')
    away_away = dict(map(lambda x: ('away_away_' + x[0], x[1]), away_away.items()))
    i.update(home_total)
    i.update(away_total)
    i.update(home_home)
    i.update(away_away)
#
four_factor_df = pd.DataFrame(result_list)

for year in range(2007, 2017):
    df1 = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ))
    df1 = df1.loc[:, ['id', 'two_way_winner', 'handicap_winner', 'over_under_result',
                      'home_line_margin', 'over_under']]
    df2 = four_factor_df
    df2 = df2[['id'] + filter(lambda x: '_last' in x, df2.columns.tolist())]
    df1.reset_index(inplace=True, drop=True)
    df2.reset_index(inplace=True, drop=True)
    df = pd.merge(df1, df2, on='id', how='left')
    #
    df.to_csv('F:/NBA/analytic/four_factor' + '/data/' + '%d.csv' %year, index=None)
    print year