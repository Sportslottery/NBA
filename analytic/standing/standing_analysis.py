__author__ = 'shane'

import json

import pandas as pd
import numpy as np

worst_season_winning_pct = float(7)/float(66)
best_season_winning_pct = float(73)/float(82)

worst_home_winning_pct = float(4)/float(33)
best_home_winning_pct = float(40)/float(41)

worst_away_winning_pct = float(1)/float(41)
best_away_winning_pct = float(34)/float(41)

year = 2016

api_df = pd.read_csv('F:/NBA/crawler/data/espn_api/%d.csv' %(year, ), usecols=['id', 'away_abbreviation', 'home_abbreviation',
                                                                       'away_score', 'home_score', 'season_type'])

standing_df = pd.read_csv('F:/NBA/data_processing/standing/data/%d.csv' %(year, ))

summary_dict = json.load(open('F:/NBA/crawler/data/espn_summary/%d.json' %(year, ), 'r'))

df = pd.merge(api_df, standing_df, on='id', how='left')

df['line_margin'] = df['id'].apply(lambda x: 0 if summary_dict.get(str(x), {}).get('line_margin') == 'EVEN' else
                                                summary_dict.get(str(x), {}).get('line_margin'))
df['line_team'] = df['id'].apply(lambda x: summary_dict.get(str(x), {}).get('line_team'))

def get_pct(x):
    tot = x[0] + x[1]
    if tot == 0:
        pct = None
    else:
        pct = float(x[0])/float(tot)
    return pct

df['home_total_pct'] = df[['home_total_w_i','home_total_l_i']].apply(get_pct, axis=1)

df['away_total_pct'] = df[['away_total_w_i','away_total_l_i']].apply(get_pct, axis=1)

df['home_home_pct'] = df[['home_home_w_i','home_home_l_i']].apply(get_pct, axis=1)

df['home_away_pct'] = df[['home_away_w_i','home_away_l_i']].apply(get_pct, axis=1)

df['away_away_pct'] = df[['away_away_w_i','away_away_l_i']].apply(get_pct, axis=1)

df['away_home_pct'] = df[['away_home_w_i','away_home_l_i']].apply(get_pct, axis=1)

df['two_way_winner'] = df[['away_score','home_score']].apply(lambda x: 'away' if x[0] > x[1] else 'home', axis=1)

# def get_line_winner(handicap_team, line_margin):


tmp_df = df.loc[:, ['id', 'away_abbreviation', 'away_score', 'home_abbreviation', 'home_score', 'line_margin',
                    'line_team', 'two_way_winner']]
tmp_df = tmp_df[tmp_df.line_margin.notnull()]


tmp_df['home_adjust_score'] = np.where(tmp_df['line_team'] == tmp_df['home_abbreviation'],
                                            tmp_df['home_score'] + tmp_df['line_margin'], tmp_df['home_score'])

tmp_df['away_adjust_score'] = np.where(tmp_df['line_team'] == tmp_df['away_abbreviation'],
                                            tmp_df['away_score'] + tmp_df['line_margin'], tmp_df['away_score'])

tmp_df['handicap_winner'] = tmp_df[['away_adjust_score','home_adjust_score']].apply(lambda x: 'away' if x[0] > x[1] else
                                    'home', axis=1)