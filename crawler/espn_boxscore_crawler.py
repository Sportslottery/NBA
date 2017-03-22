__author__ = 'shane'

import os
import requests

import pandas as pd
from pyquery import PyQuery as pyq

class EspnBoxscoreData(object):
    def __init__(self):
        self.data_path = os.path.dirname(__file__) + '/data/'

    def get_id_list(self, year, month=None):
        if month:
            file_name = self.data_path + 'espn_api/' + '%d%02d.csv' %(year, month, )
        else:
            file_name = self.data_path + 'espn_api/' + '%d.csv' %(year, )
        df = pd.read_csv(file_name)
        id_list = df.id.tolist()
        return id_list

    def get_espn_boxscore_data(self, id):
        url = 'http://www.espn.com/nba/boxscore?gameId=%d' %id
        result_dict = {}
        r = requests.get(url)
        text = r.content
        doc = pyq(text)
        away_TO = doc('.highlight .to').eq(0).text()
        home_TO = doc('.highlight .to').eq(2).text()
        away_OREB = doc('.highlight .oreb').eq(0).text()
        home_OREB = doc('.highlight .oreb').eq(2).text()
        away_DREB = doc('.highlight .dreb').eq(0).text()
        home_DREB = doc('.highlight .dreb').eq(2).text()
        result_dict['id'] = id
        result_dict['away_TO'] = away_TO
        result_dict['home_TO'] = home_TO
        result_dict['away_OREB'] = away_OREB
        result_dict['home_OREB'] = home_OREB
        result_dict['away_DREB'] = away_DREB
        result_dict['home_DREB'] = home_DREB
        return result_dict

    def main(self, year, month=None):
        id_list = self.get_id_list(year, month)
        tot = len(id_list)
        result_list = []
        for index, element in enumerate(id_list):
            result_dict = self.get_espn_boxscore_data(element)
            result_list.append(result_dict)
            print index, tot, element
        result_df = pd.DataFrame(result_list)
        if month:
            file_name = self.data_path + 'espn_boxscore/%d%02d.csv' %(year, month, )
        else:
            file_name = self.data_path + 'espn_boxscore/%d.csv' %(year, )
        result_df.to_csv(file_name, index=None)

if __name__ == "__main__":
    # TOV RB
    EBD = EspnBoxscoreData()
    EBD.main(year=2017, month=1)

