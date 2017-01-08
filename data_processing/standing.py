__author__ = 'shane'

import os

import numpy as np
import pandas as pd

class StandingDataProcessing(object):
    def __init__(self):
        # self.data_path = os.path.dirname(os.path.dirname(__file__)) + '/crawler/data/espn_api/'
        self.data_path = 'F:/NBA/crawler/data/espn_api/'
        self.col_names = ['away_away_records', 'away_home_records', 'away_score', 'away_total_records', 'date',
                          'home_away_records', 'home_home_records', 'home_score', 'home_total_records',
                          'id','season_type','season_year']


    def get_raw_data(self, year):
        df = pd.read_csv(self.data_path + '%d.csv' %(year, ), usecols=self.col_names)
        df['year'] = year
        df_last_year = pd.read_csv(self.data_path + '%d.csv' %(year - 1, ), usecols=self.col_names)
        df_last_year['year'] = year - 1
        df = df.append(df_last_year)
        return df

    def get_tmp_df(self, year):
        df = self.get_raw_data(year)
        df = df.fillna('-')
        df['home_total_w'] = df.home_total_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['home_total_l'] = df.home_total_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        df['away_total_w'] = df.away_total_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['away_total_l'] = df.away_total_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        df['home_home_w'] = df.home_home_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['home_home_l'] = df.home_home_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        df['home_away_w'] = df.home_away_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['home_away_l'] = df.home_away_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        df['away_home_w'] = df.away_home_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['away_home_l'] = df.away_home_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        df['away_away_w'] = df.away_away_records.apply(lambda x: int(x.split('-')[0]) if x != '-' else None)
        df['away_away_l'] = df.away_away_records.apply(lambda x: int(x.split('-')[-1]) if x != '-' else None)
        return df

    def get_init_standing(row, df):
        if not df['home_total_w']:
            init_result = None
        elif df['season_type'] == 3:
            init_result = int(df['home_total_w'])
        else:
            if df['home_score'] > df['away_score']:
                init_result = int(df['home_total_w']) - 1
            else:
                init_result = int(df['home_total_w'])
        return init_result



    def main(self, year):
        result_df = pd.DataFrame()
        df = self.get_tmp_df(year)
        result_df['id'] = df[df['year' == year]]['id']

        return result_df


if __name__ == "__main__":
    SDP = StandingDataProcessing()
    df = SDP.get_tmp_df(2016)
    print df
