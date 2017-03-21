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

    def get_espn_boxscore_data(self, url):
        r = requests.get(url)
        text = r.content
        doc = pyq(text)
        away_TO = doc('.highlight .to').eq(0).text()
        home_TO = doc('.highlight .to').eq(2).text()
        print away_TO
        print home_TO

if __name__ == "__main__":
    # TOV RB
    EBD = EspnBoxscoreData()
    EBD.get_espn_boxscore_data('http://www.espn.com/nba/boxscore?gameId=400900430')

