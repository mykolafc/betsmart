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

def getDataNba():
    url = "https://api.on.pointsbet.com/api/v2/competitions/105/events/featured?includeLive=false&page=1"

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.pointsbet.com',
        'path': '/api/v2/competitions/105/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.pointsbet.com',
        #'If-Modified-Since': formatdate(timeval=datetime.now().timestamp(), localtime=False, usegmt=True),
        'Origin': 'https://on.pointsbet.ca',
        'Referer': 'https://on.pointsbet.ca/',
        'Request-Context': 'appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd',
        'Request-Id': '|a8b66a6bd2b44162ae6a7cb987ea6135.509a70a7a2354790',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'traceparent': '00-a8b66a6bd2b44162ae6a7cb987ea6135-509a70a7a2354790-01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15'
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data

def getDataNhl():
    url = "https://api.on.pointsbet.com/api/v2/competitions/18917/events/featured?includeLive=false&page=1"

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.pointsbet.com',
        'path': '/api/v2/competitions/194/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.pointsbet.com',
        #'If-Modified-Since': 'Fri, 31 May 2024 17:27:00 GMT',
        'Origin': 'https://on.pointsbet.ca',
        'Referer': 'https://on.pointsbet.ca/',
        'Request-Context': 'appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd',
        'Request-Id': '|ad6bb16722724ade810782b0897de4cc.8f194ef6f10e4d44',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'traceparent': '00-ad6bb16722724ade810782b0897de4cc-8f194ef6f10e4d44-01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15'
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data

def getDataMlb():
    # This should return the JSON file of the mlb front page from PointsBet
    # I realized the problem is that we didnt include the headers parameter in the get request

    # It's possible that some things in this link variable so it might not always be this EXACT link
    url = "https://api.on.pointsbet.com/api/v2/competitions/7366/events/featured?includeLive=false&page=1"

    headers = {
        "authority": "api.on.pointsbet.com",
        "method": "GET",
        "path": "/api/v2/competitions/7366/events/featured?includeLive=false&page=1",
        "scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",

        # This changes based on the current time obv so it needs to be a variable attributed to the time
        #"If-Modified-Since": formatdate(timeval=datetime.now().timestamp(), localtime=False, usegmt=True),
        "Origin": "https://on.pointsbet.ca",
        "Priority": "u=1, i",
        "Referer": "https://on.pointsbet.ca/",
        "Request-Context": "appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd",
        "Request-Id": "|5f2a39d254164a50847559703c0e1f05.8a4cfc06025146c4",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Traceparent": "00-5f2a39d254164a50847559703c0e1f05-8a4cfc06025146c4-01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data

def getDataNfl():
    url = 'https://api.on.pointsbet.com/api/v2/competitions/6/events/featured?includeLive=false&page=1'

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.pointsbet.com',
        'path': '/api/v2/competitions/194/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.pointsbet.com',
        #'If-Modified-Since': 'Fri, 31 May 2024 17:27:00 GMT',
        'Origin': 'https://on.pointsbet.ca',
        'Referer': 'https://on.pointsbet.ca/',
        'Request-Context': 'appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd',
        'Request-Id': '|ad6bb16722724ade810782b0897de4cc.8f194ef6f10e4d44',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'traceparent': '00-ad6bb16722724ade810782b0897de4cc-8f194ef6f10e4d44-01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15'
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data

def getGameId(data):
    gameId = data['events'][0]['key']
    print(gameId)
    return gameId

def getGameData(gameId):

    gameUrl = "https://api.on.pointsbet.com/api/mes/v3/events/"+gameId

    gameHeaders = {
        "authority": "api.on.pointsbet.com",
        "method": "GET",
        "path": "/api/mes/v3/events/"+gameId,
        "scheme": "https",
        "Accept": "application/json, text/plain, /",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        #"If-Modified-Since": "Fri, 24 May 2024 17:13:09 GMT",
        "Origin": "https://on.pointsbet.ca/",
        "Priority": "u=1, i",
        "Referer": "https://on.pointsbet.ca/",
        "Request-Id": "|36c6c128c94f46ffa4f43c87f09fa6b2.888d033e0e04443f",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Traceparent": "00-36c6c128c94f46ffa4f43c87f09fa6b2-888d033e0e04443f-01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    
    gameResponse = requests.get(gameUrl, headers=gameHeaders)
    data = gameResponse.json()

    homeAwayTeams = data['awayTeam'] + \
        '(away)' + ' vs ' + data['homeTeam'] + '(home)'

    markets = data['fixedOddsMarkets']
    if data['competitionName'] == 'National Hockey League':
        league = 'NHL'
    else:
        league = data['competitionName']
    teams = []
    points = []
    odds = []
    side = []
    category = []
    names = []
    designation = []
    unit = []
    for market in markets:
        for prop in market['outcomes']:
            teams.append(homeAwayTeams)
            category.append(market['eventClass'])
            side.append(prop['side'])
            points.append(prop['points'])
            odds.append(prop['price'])
            unit.append(prop['unitType'])
            if 'Over' in prop['name']:
                designation.append('over')
            elif 'Under' in prop['name']:
                designation.append('under')
            else:
                designation.append('')
            names.append(prop['name'])

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': category, 'Designation': designation,
                    'Side': side, 'Name': names, 'Points': points, 'Odds': odds, 'Units': unit})
    
    return df

def gameDump(gameId):

    df = getGameData(gameId)

    df.to_csv('PointsBetGame'+ gameId +'.csv')

def jsonDump(data, league):
    with open('Pointsbet'+league+'.json', 'w') as f:
        json.dump(data, f, indent=4)

def csvDump(data, league):

    teams = []
    points = []
    odds = []
    side = []
    category = []
    names = []
    designation = []
    unit = []

    for x in data['events']:
        for y in x['specialFixedOddsMarkets']:
            for z in y['outcomes']:
                teams.append(x['awayTeam'] + '(away)' + ' vs ' + x['homeTeam'] + '(home)')
                category.append(z['groupByHeader'])
                side.append(z['side'])
                points.append(z['points'])
                odds.append(z['price'])
                names.append(' ')
                unit.append(' ')
                if 'Over' in z['name']:
                    designation.append('over')
                elif 'Under' in z['name']:
                    designation.append('under')
                else:
                    designation.append(' ')

    df = pd.DataFrame({'Teams': teams, 'Category': category, 'Designation': designation, 
                       'Side': side, 'Name': names, 'Points': points, 'Odds': odds, 'Units': unit})
    df.to_csv('PointsBet'+league+'.csv', index=False)

def gigaDump(dataMlb, dataNba, dataNhl, dataNfl):
    
    league = []
    teams = []
    points = []
    odds = []
    side = []
    category = []
    names = []
    designation = []
    unit = []

    games = []

    for x in dataMlb['events']:
        games.append(x['key'])
        for y in x['specialFixedOddsMarkets']:
            for z in y['outcomes']:
                league.append('MLB')
                teams.append(x['awayTeam'] + '(away)' + ' vs ' + x['homeTeam'] + '(home)')
                category.append(z['groupByHeader'])
                side.append(z['side'])
                points.append(z['points'])
                odds.append(z['price'])
                names.append(' ')
                unit.append(' ')
                if 'Over' in z['name']:
                    designation.append('over')
                elif 'Under' in z['name']:
                    designation.append('under')
                else:
                    designation.append(' ')

    for x in dataNba['events']:
        games.append(x['key'])
        for y in x['specialFixedOddsMarkets']:
            for z in y['outcomes']:
                league.append('NBA')
                teams.append(x['awayTeam'] + '(away)' + ' vs ' + x['homeTeam'] + '(home)')
                category.append(z['groupByHeader'])
                side.append(z['side'])
                points.append(z['points'])
                odds.append(z['price'])
                names.append(' ')
                unit.append(' ')
                if 'Over' in z['name']:
                    designation.append('over')
                elif 'Under' in z['name']:
                    designation.append('under')
                else:
                    designation.append(' ')
    
    for x in dataNhl['events']:
        games.append(x['key'])
        for y in x['specialFixedOddsMarkets']:
            for z in y['outcomes']:
                league.append('NHL')
                teams.append(x['awayTeam'] + '(away)' + ' vs ' + x['homeTeam'] + '(home)')
                category.append(z['groupByHeader'])
                side.append(z['side'])
                points.append(z['points'])
                odds.append(z['price'])
                names.append(' ')
                unit.append(' ')
                if 'Over' in z['name']:
                    designation.append('over')
                elif 'Under' in z['name']:
                    designation.append('under')
                else:
                    designation.append(' ')

    for x in dataNfl['events']:
        games.append(x['key'])
        for y in x['specialFixedOddsMarkets']:
            for z in y['outcomes']:
                league.append('NFL')
                teams.append(x['awayTeam'] + '(away)' + ' vs ' + x['homeTeam'] + '(home)')
                category.append(z['groupByHeader'])
                side.append(z['side'])
                points.append(z['points'])
                odds.append(z['price'])
                names.append(' ')
                unit.append(' ')
                if 'Over' in z['name']:
                    designation.append('over')
                elif 'Under' in z['name']:
                    designation.append('under')
                else:
                    designation.append(' ')

    frames = []

    for x in games:
        frames.append(getGameData(x))

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': category, 'Designation': designation, 
                       'Side': side, 'Name': names, 'Points': points, 'Odds': odds, 'Units': unit})
    
    frames.append(df)

    df = pd.concat(frames)

    df.to_csv('PointsBetGigaDump.csv', index=False)

class MyCmd(cmd.Cmd):
    prompt = '> '

    def __init__(self):
        super(MyCmd, self).__init__()
        self.data = getDataMlb()
        self.gameId = getGameId(self.data)
        self.league = 'Mlb'

    def do_set_gameid(self, arg):
        """Set the gameId"""
        self.gameId = arg

    def do_get_mlb(self, arg):
        """Call the getDataMlb function"""
        self.data = getDataMlb()
        self.gameId = getGameId(self.data)
        self.league = 'Mlb'

    def do_get_nba(self, arg):
        """Call the getDataNba function"""
        self.data = getDataNba()
        self.gameId = getGameId(self.data)
        self.league = 'Nba'

    def do_get_nhl(self, arg):
        """Call the getDataNhl function"""
        self.data = getDataNhl()
        self.gameId = getGameId(self.data)
        self.league = 'Nhl'
    
    def do_get_nfl(self, arg):
        """Call the getDataNfl function"""
        self.data = getDataNfl()
        self.gameId = getGameId(self.data)
        self.league = 'Nfl'

    def do_json_dump(self, arg):
        """Call the jsonDump function"""
        jsonDump(self.data, self.league)

    def do_csv_dump(self, arg):
        """Call the csvDump function"""
        csvDump(self.data, self.league)

    def do_game_dump(self, arg):
        """Call the gameDump function"""
        gameId = self.gameId
        gameDump(gameId)

    def do_get_game_id(self, arg):
        """Call the getGameId function"""
        getGameId(self.data)

    def do_giga_dump(self, arg):
        """Call the gigaDump function"""
        gigaDump(getDataMlb(), getDataNba(), getDataNhl(), getDataNfl())

    
    def do_exit(self, arg):
        """Exit the program"""
        return True

if __name__ == '__main__':
    MyCmd().cmdloop()