__author__ = 'shane'

import os
import re

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

    def split_records(self, df, col_name, game_result):
        if game_result == 'w':
            idx = 0
        else:
            idx = -1
        result_series = df[col_name].apply(lambda x: int(x.split('-')[idx]) if x != '-' else None)
        return result_series


    def get_tmp_df(self, year):
        df = self.get_raw_data(year)
        df = df.fillna('-')
        df['home_total_w'] = self.split_records(df, 'home_total_records', 'w')
        df['home_total_l'] = self.split_records(df, 'home_total_records', 'l')
        df['away_total_w'] = self.split_records(df, 'away_total_records', 'w')
        df['away_total_l'] = self.split_records(df, 'away_total_records', 'l')
        df['home_home_w'] = self.split_records(df, 'home_home_records', 'w')
        df['home_home_l'] = self.split_records(df, 'home_home_records', 'l')
        df['home_away_w'] = self.split_records(df, 'home_away_records', 'w')
        df['home_away_l'] = self.split_records(df, 'home_away_records', 'l')
        df['away_home_w'] = self.split_records(df, 'away_home_records', 'w')
        df['away_home_l'] = self.split_records(df, 'away_home_records', 'l')
        df['away_away_w'] = self.split_records(df, 'away_away_records', 'w')
        df['away_away_l'] = self.split_records(df, 'away_away_records', 'l')

        df['home_total_w_i'] = np.where(df['home_total_w'].isnull(), None,
                                np.where(df['season_type'] == 3, df['home_total_w'],
                                np.where(df['home_score'] > df['away_score'], df['home_total_w'] - 1,
                                df['home_total_w'])))

        df['home_home_w_i'] = np.where(df['home_home_w'].isnull(), None,
                                np.where(df['season_type'] == 3, df['home_home_w'],
                                np.where(df['home_score'] > df['away_score'], df['home_home_w'] - 1,
                                df['home_home_w'])))

        df['away_total_l_i'] = np.where(df['away_total_l'].isnull(), None,
                                np.where(df['season_type'] == 3, df['away_total_l'],
                                np.where(df['home_score'] > df['away_score'], df['away_total_l'] - 1,
                                df['away_total_l'])))

        df['away_away_l_i'] = np.where(df['away_away_l'].isnull(), None,
                                np.where(df['season_type'] == 3, df['away_away_l'],
                                np.where(df['home_score'] > df['away_score'], df['away_away_l'] - 1,
                                df['away_away_l'])))

        df['away_total_w_i'] = np.where(df['away_total_w'].isnull(), None,
                                np.where(df['season_type'] == 3, df['away_total_w'],
                                np.where(df['home_score'] < df['away_score'], df['away_total_w'] - 1,
                                df['away_total_w'])))

        df['away_away_w_i'] = np.where(df['away_away_w'].isnull(), None,
                                np.where(df['season_type'] == 3, df['away_away_w'],
                                np.where(df['home_score'] < df['away_score'], df['away_away_w'] - 1,
                                df['away_away_w'])))

        df['home_total_l_i'] = np.where(df['home_total_l'].isnull(), None,
                                np.where(df['season_type'] == 3, df['home_total_l'],
                                np.where(df['home_score'] < df['away_score'], df['home_total_l'] - 1,
                                df['home_total_l'])))

        df['home_home_l_i'] = np.where(df['home_home_l'].isnull(), None,
                                np.where(df['season_type'] == 3, df['home_home_l'],
                                np.where(df['home_score'] < df['away_score'], df['home_home_l'] - 1,
                                df['home_home_l'])))
        df['home_away_w_i'] = df['home_away_w']
        df['home_away_l_i'] = df['home_away_l']
        df['away_home_w_i'] = df['away_home_w']
        df['away_home_l_i'] = df['away_home_l']
        return df

    def main(self, year):
        result_df = pd.DataFrame()
        df = self.get_tmp_df(year)
        result_df['id'] = df[df['year' == year]]['id']

        return result_df


if __name__ == "__main__":
    SDP = StandingDataProcessing()
    df = SDP.get_tmp_df(2016)
    print df
