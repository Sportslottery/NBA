__author__ = 'Shane_Kao'

import os
import json

import pandas as pd

proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
strk_dict = json.load(open(os.path.dirname(__file__) + '/strk_result.json', 'r'))

for year in range(2007, 2017):
    df = pd.read_csv('%s/analytic/standing/data/%d.csv' %(proj_dict, year, ))
    df['away_away_strk'] = df['id'].apply(lambda x: strk_dict.get(str(x), {}).get('away_away_strk'))
    df['home_home_strk'] = df['id'].apply(lambda x: strk_dict.get(str(x), {}).get('home_home_strk'))
    df['away_total_strk'] = df['id'].apply(lambda x: strk_dict.get(str(x), {}).get('away_total_strk'))
    df['home_total_strk'] = df['id'].apply(lambda x: strk_dict.get(str(x), {}).get('home_total_strk'))
    df = df[filter(lambda x: '_i' not in x and '_pct' not in x,df.columns.tolist())]
    df.to_csv(os.path.dirname(__file__) + '/data/' + '%d.csv' %year, index=None)
    print year