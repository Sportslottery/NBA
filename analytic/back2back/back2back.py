__author__ = 'shane'

import os
import time
import json
from datetime import datetime


import pandas as pd
import numpy as np


# proj_dict = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
proj_dict = 'F:/NBA'
data = pd.DataFrame()
for year in range(2006, 2017):
    api_df = pd.read_csv('%s/crawler/data/espn_api/%d.csv' %(proj_dict, year, ),
                     usecols=['id', 'away_abbreviation', 'home_abbreviation', 'season_year',
                              'away_score', 'home_score', 'season_type', 'date'])
    print year
    data = data.append(api_df)