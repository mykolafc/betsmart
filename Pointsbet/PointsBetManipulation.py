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

with open('PointsBetGame564090.json', 'r') as f:
    data = json.load(f)

homeAwayTeams = data['awayTeam'] + \
    '(away)' + ' vs ' + data['homeTeam'] + '(home)'
league = data['competitionName']

markets = data['fixedOddsMarkets']


def gameProps(teams, points, odds, side, category, names, designation, units, market):
    eventClass = market['eventClass']
    for prop in market['outcomes']:
        teams.append(homeAwayTeams)
        category.append(eventClass)
        names.append('')
        points.append(prop['points'])
        odds.append(prop['price'])
        side.append(prop['side'])
        units.append('')
        if 'Over' in prop['name']:
            designation.append('over')
        elif 'Under' in prop['name']:
            designation.append('under')
        else:
            designation.append('')


def playerProps(teams, points, odds, side, category, names, designation, units, market):
    eventClass = market['eventClass']
    for prop in market['outcomes']:
        teams.append(homeAwayTeams)
        category.append('Player Props')
        side.append(' ')
        points.append(prop['points'])
        odds.append(prop['price'])
        if 'Over' in prop['name']:
            designation.append('over')
            names.append(prop['name'].split('Over')[0].strip())
        elif 'Under' in prop['name']:
            designation.append('under')
            names.append(prop['name'].split('Under')[0].strip())
        units.append(eventClass)


gamePropsEvents = ['Moneyline OF', 'Run Line', 'Total Runs OF',
                   'Total Runs - AWAYTEAM OF', 'Total Runs - HOMETEAM OF']

playerPropOUEvents = ['Player home runs OF', 'Player hits OF', 'Player runs batted in OF',
                      'Player stolen bases OF', 'Pitcher strikeouts OF', 'Player Total Bases']


teams = []
points = []
odds = []
side = []
category = []
names = []
designation = []
units = []
for market in markets:
    if any(playerPropOUEvent == market['eventClass'] for playerPropOUEvent in playerPropOUEvents):
        playerProps(teams, points, odds, side, category,
                    names, designation, units, market)
    elif any(gamePropEvent == market['eventClass'] for gamePropEvent in gamePropsEvents):
        gameProps(teams, points, odds, side, category,
                  names, designation, units, market)

df = pd.DataFrame({'Teams': teams, 'Category': category, 'Designation': designation,
                  'Side': side, 'Name': names, 'Points': points, 'Odds': odds, 'Units': units})
df.to_csv('PointsBetGame564090.csv')

# Im going to have to manually chose the names to pick in groupNames cuz a lot of the odds are irrelevant
