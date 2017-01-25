__author__ = 'Shane_Kao'

import os
import json

import pandas as pd
proj_dict = 'F:/NBA'
# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
last_n_dict = json.load(open(proj_dict + '/analytic/last_n/last_n_result.json', 'r'))
col_names = [u'home_total_last_4_pct',
 u'home_home_last_4_pct',
 u'away_total_last_6_pct',
 u'home_total_last_7_pct',
 u'away_away_last_9_pct',
 u'away_total_last_4_pct',
 u'away_total_last_5_pct',
 u'home_total_last_5_pct',
 u'away_total_last_3_pct',
 u'home_total_last_1_pct',
 u'home_home_last_9_pct',
 u'away_away_last_3_pct',
 u'away_away_last_2_pct',
 u'home_home_last_7_pct',
 u'away_away_last_5_pct',
 u'home_home_last_6_pct',
 u'away_total_last_10_pct',
 u'home_home_last_3_pct',
 u'away_away_last_8_pct',
 u'home_total_last_9_pct',
 u'home_total_last_8_pct',
 u'home_total_last_2_pct',
 u'away_total_last_9_pct',
 u'away_away_last_10_pct',
 u'home_total_last_3_pct',
 u'away_total_last_1_pct',
 u'home_home_last_1_pct',
 u'home_home_last_5_pct',
 u'away_total_last_7_pct',
 u'home_home_last_8_pct',
 u'away_total_last_2_pct',
 u'home_total_last_6_pct',
 u'away_total_last_8_pct',
 u'away_away_last_7_pct',
 u'home_home_last_2_pct',
 u'home_total_last_10_pct',
 u'away_away_last_1_pct',
 u'away_away_last_6_pct',
 u'home_home_last_10_pct',
 u'away_away_last_4_pct']
for year in range(2007, 2017):
    df = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ))
    if 'handicap_winner' in list(df.columns):
        df = df[['id', 'season_type', 'two_way_winner', 'handicap_winner', 'over_under_result',
             'home_line_margin', 'over_under']]
    else:
        df = df[['id', 'season_type', 'two_way_winner', 'over_under_result',
             'home_line_margin', 'over_under']]
    for col in col_names:
        df[col] = df['id'].apply(lambda x: last_n_dict.get(str(x) + '.0', {}).get(col))


    df.to_csv(os.path.dirname(__file__) + '/data/' + '%d.csv' %year, index=None)
    print year