import grequests
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
import time
import asyncio
import aiohttp
import requests
import json
import numpy as np
from datetime import datetime
from email.utils import formatdate
import cmd
import re
import git

# Open and read the JSON file
with open('pinnacle_data.json', 'r') as json_file:
    nameData = json.load(json_file)
with open('pinnacle_data2.json', 'r') as json_file:
    oddsData = json.load(json_file)

category = []
designation = []
points = []
odds = []

# Now 'data' contains the content of the JSON file as a Python dictionary
matchupIds = dict()
for bet in nameData:
    if bet.get('special') and bet['special'].get('category') == 'Player Props':
        matchupIds[bet['id']] = bet['special']['description']

# filtered_data = [item for item in oddsData if item.get(
#     'matchupId') in matchupIds]

for item in oddsData:
    if item.get('matchupId') in matchupIds:
        # Over
        category.append(matchupIds[item['matchupId']])
        designation.append('over')
        points.append(item['prices'][0]['points'])
        odds.append(item['prices'][0]['price'])
        # Under
        category.append(matchupIds[item['matchupId']])
        designation.append('under')
        points.append(item['prices'][1]['points'])
        odds.append(item['prices'][1]['price'])

df = pd.DataFrame({'Category': category, 'Designation': designation,
                  'Points': points, 'PN American Odds': odds})

dir = git.Repo('.', search_parent_directories=True).working_tree_dir
df.to_csv(str(dir) + '/bin/PinnacleTestDump.csv', index=False)
