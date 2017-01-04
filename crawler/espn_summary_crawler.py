__author__ = 'shane'

import re
import requests

from pyquery import PyQuery as pyq

# url = 'http://www.espn.com/nba/game?gameId=400278178'

url = 'http://www.espn.com/nba/game?gameId=400899410'

r = requests.get(url)
data = r.content
doc = pyq(data)

odds_details = doc('.odds-details').text()

result_dict = {}
if odds_details:
    m1 = re.match(r'.*Line: (\S+) (\S+)', odds_details)
    if m1:
        result_dict['line_team'] = m1.group(1)
        result_dict['line_margin'] = float(m1.group(2))
    m2 = re.match(r'.*Over/Under: (\d+)', odds_details)
    if m2:
        result_dict['over_under'] = float(m2.group(1))


game_flow = eval(doc('#gameFlow-graph').attr('data-plays'))
result_dict['game_flow'] = game_flow