__author__ = 'shane'

import requests

from pyquery import PyQuery as pyq

# url = 'http://www.espn.com/nba/game?gameId=400278178'

# url = 'http://www.espn.com/nba/game?gameId=400899410'
#
url = 'http://www.espn.com/nba/game?gameId=320101005'

r = requests.get(url)
data = r.content
doc = pyq(data)


print doc('.odds-details').text()

print doc('#gameFlow-graph').attr('data-plays')