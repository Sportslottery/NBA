__author__ = 'shane'

import os
import re
import json
import requests

import pandas as pd
from pyquery import PyQuery as pyq


class EspnSummaryData(object):
    def __init__(self):
        self.data_path = os.path.dirname(__file__) + '/data/'

    def get_id_list(self, year):
        df = pd.read_csv(self.data_path + 'espn_api/' + '%d.csv' %(year, ))
        id_list = df.id.tolist()
        return id_list

    def get_espn_summary_data(self, url):
        r = requests.get(url)
        data = r.content
        doc = pyq(data)
        odds_details = doc('.odds-details').text()
        result_dict = {}
        if odds_details:
            if 'Line: EVEN' in odds_details:
                result_dict['line_margin'] = 'EVEN'
                if 'Over/Under:' in odds_details:
                    result_dict['over_under'] = float(odds_details.split()[-1])
            else:
                m1 = re.match(r'.*Line: (\S+) (\S+)', odds_details)
                if m1:
                    result_dict['line_team'] = m1.group(1)
                    result_dict['line_margin'] = float(m1.group(2))
                m2 = re.match(r'.*Over/Under: (\d+)', odds_details)
                if m2:
                    result_dict['over_under'] = float(m2.group(1))
            game_flow = doc('#gameFlow-graph').attr('data-plays')
            if game_flow:
                result_dict['game_flow'] = eval(game_flow)
        return result_dict

    def main(self, year):
        id_list = self.get_id_list(year)
        tot = len(id_list)
        result_dict = {}
        for index, element in enumerate(id_list):
            url = 'http://www.espn.com/nba/game?gameId=%d' %(element, )
            print index, tot, url
            result_dict[str(element)] = self.get_espn_summary_data(url)
        with open(self.data_path + 'espn_summary/%d.json' %(year, ), 'w') as fp:
            json.dump(result_dict, fp)

if __name__ == "__main__":
    ESD = EspnSummaryData()
    ESD.main(2016)