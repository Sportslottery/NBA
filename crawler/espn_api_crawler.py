__author__ = 'shane'

import os
import time
import datetime
import requests

import pandas as pd


class EspnApiData(object):
    def __init__(self):
        self.col_names = ['id', 'date', 'season_year', 'season_type', 'status_period', 'home_display_name',
                          'home_abbreviation', 'away_display_name', 'away_abbreviation', 'home_score', 'away_score',
                          'regular_total_score', 'home_total_records',
                          'home_home_records', 'home_away_records', 'away_total_records', 'away_home_records',
                          'away_away_records', 'home_FGM', 'away_FGM', 'home_3PM', 'away_3PM', 'home_FGA', 'away_FGA',
                          'home_FTA', 'away_FTA', 'home_FTM', 'away_FTM', 'series_summary']
        self.request_url = ('http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?'
                            'lang=en&region=us&calendartype=blacklist&limit=100&dates=%s')
        self.project_dir = os.path.dirname(__file__) + '\\data\\espn_api\\'

    def get_date_list(self, year, month=None):
        if month:
            start = datetime.datetime.strptime('%d%02d01' %(year, month, ), '%Y%m%d')
            end = datetime.datetime.strptime('%d%02d01' %(year, month + 1, ), '%Y%m%d')
        else:
            start = datetime.datetime.strptime('%d0101' %(year, ), '%Y%m%d')
            end = datetime.datetime.strptime('%d0101' %(year + 1, ), '%Y%m%d')
        step = datetime.timedelta(days=1)
        date_list = []
        while start < end:
            date_list.append(start.date().strftime(format='%Y%m%d'))
            start += step
        return date_list

    def get_espn_api_data(self, url):
        r = requests.get(url)
        data = r.json()
        result_list = []
        if data['events']:
            for i in data['events']:
                if i['competitions'][0]['status']['type']['completed']:
                    id = i['id']
                    date = i['date']
                    season_year = i['season']['year']
                    season_type = i['season']['type']
                    status_period = i['status']['period']
                    home_display_name = i['competitions'][0]['competitors'][0]['team']['displayName']
                    home_abbreviation = i['competitions'][0]['competitors'][0]['team'].get('abbreviation', None)
                    away_display_name = i['competitions'][0]['competitors'][1]['team']['displayName']
                    away_abbreviation = i['competitions'][0]['competitors'][1]['team'].get('abbreviation', None)
                    home_score = int(i['competitions'][0]['competitors'][0]['score'])
                    away_score = int(i['competitions'][0]['competitors'][1]['score'])
                    home_regular_score = sum(map(lambda x: x['value'], i['competitions'][0]['competitors'][0]['linescores'])[:4])
                    away_regular_score = sum(map(lambda x: x['value'], i['competitions'][0]['competitors'][1]['linescores'])[:4])
                    regular_total_score = home_regular_score + away_regular_score
                    home_total_records = i['competitions'][0]['competitors'][0].get('records', [{}, {}, {}])[0].get('summary', None)
                    home_home_records = i['competitions'][0]['competitors'][0].get('records', [{}, {}, {}])[1].get('summary', None)
                    home_away_records = i['competitions'][0]['competitors'][0].get('records', [{}, {}, {}])[2].get('summary', None)
                    away_total_records = i['competitions'][0]['competitors'][1].get('records', [{}, {}, {}])[0].get('summary', None)
                    away_home_records = i['competitions'][0]['competitors'][1].get('records', [{}, {}, {}])[1].get('summary', None)
                    away_away_records = i['competitions'][0]['competitors'][1].get('records', [{}, {}, {}])[2].get('summary', None)
                    home_stat = i['competitions'][0]['competitors'][0].get('statistics', [])
                    if home_stat:
                        home_FGM = int(filter(lambda x: x['abbreviation'] == 'FGM', home_stat)[0]['displayValue'])
                        home_3PM = int(filter(lambda x: x['abbreviation'] == '3PM', home_stat)[0]['displayValue'])
                        home_FGA = int(filter(lambda x: x['abbreviation'] == 'FGA', home_stat)[0]['displayValue'])
                        home_FTA = int(filter(lambda x: x['abbreviation'] == 'FTA', home_stat)[0]['displayValue'])
                        home_FTM = int(filter(lambda x: x['abbreviation'] == 'FTM', home_stat)[0]['displayValue'])
                    else:
                        home_FGM = home_3PM = home_FGA = home_FTA = home_FTM = None
                    away_stat = i['competitions'][0]['competitors'][1].get('statistics', [])
                    if away_stat:
                        away_FGM = int(filter(lambda x: x['abbreviation'] == 'FGM', away_stat)[0]['displayValue'])
                        away_3PM = int(filter(lambda x: x['abbreviation'] == '3PM', away_stat)[0]['displayValue'])
                        away_FGA = int(filter(lambda x: x['abbreviation'] == 'FGA', away_stat)[0]['displayValue'])
                        away_FTA = int(filter(lambda x: x['abbreviation'] == 'FTA', away_stat)[0]['displayValue'])
                        away_FTM = int(filter(lambda x: x['abbreviation'] == 'FTM', away_stat)[0]['displayValue'])
                    else:
                        away_FGM = away_3PM = away_FGA = away_FTA = away_FTM = None
                    series_summary = i['competitions'][0].get('series', {}).get('summary', None)
                    col_value = [id, date, season_year, season_type, status_period, home_display_name, home_abbreviation,
                                away_display_name, away_abbreviation, home_score, away_score, regular_total_score, home_total_records,
                                home_home_records, home_away_records, away_total_records, away_home_records, away_away_records, home_FGM, away_FGM, home_3PM, away_3PM, home_FGA, away_FGA,
                                home_FTA, away_FTA, home_FTM, away_FTM, series_summary]
                    result_dict = dict(zip(self.col_names, col_value))
                    result_list.append(result_dict)
        return result_list

    def main(self, year, month=None):
        result_list = []
        target_dates = self.get_date_list(year, month)
        for i in target_dates:
            url = self.request_url %i
            print url
            result_list += self.get_espn_api_data(url)
            time.sleep(0.5)
        if result_list:
            df = pd.DataFrame(result_list)
            if month:
                file_name = '%d%02d.csv' %(year, month, )
            else:
                file_name = '%d.csv' %(year, )
            df.to_csv(self.project_dir + file_name, index=None)

if __name__ == "__main__":
    EAD = EspnApiData()
    EAD.main(year=2017, month=3)