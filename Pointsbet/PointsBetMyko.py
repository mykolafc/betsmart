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

def listGameIds(data):
    for x in data['events']:
        print(x['key']+ ' ' + x['name'])

def decimal_to_american(decimal_odds):
    if decimal_odds == 1.0:
        american_odds = 0
    elif decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)

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

def gameJson(gameId):
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

    with open('PointsBetGame'+gameId+'.json', 'w') as f:
        json.dump(data, f, indent=4)

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

def makeKey(unit, points):
    switcher = {
        #NBA switches
        "Alternate Assists": f"pp;0;ss;asst;{points}",
        "Player Assists Over/Under": f"pp;0;ou;asst;{points}",
        "Alternate Points": f"pp;0;ss;pts;{points}",
        "Player Points Over/Under": f"pp;0;ou;pts;{points}",
        "Player 3-Pointers Made": f"pp;0;ou;3pt;{points}",
        "Alternate Threes": f"pp;0;ss;3pt;{points}",
        "Player Rebounds Over/Under": f"pp;0;ou;reb;{points}",
        "Alternate Rebounds": f"pp;0;ss;reb;{points}",
        "Player Pts + Rebs + Asts Over/Under": f"pp;0;ou;pra;{points}",
        "Player To Record A Double Double": f"pp;0;ou;dbldbl;{points}",
        "Player To Record A Triple Double": f"pp;0;ou;trpldbl;{points}",

        #MLB switches
        "Player home runs OF": f"pp;0;ou;hr;{points}",
        "Alternate Pitcher Strikeouts": f"pp;0;ss;so;{points}",
        "Player hits OF": f"pp;0;ou;hit;{points}",
        "Player runs batted in OF": f"pp;0;ou;rbi;{points}",
        "Player stolen bases OF": f"pp;0;ou;sb;{points}",
        "Pitcher strikeouts OF": f"pp;0;ou;so;{points}",
        "Alternate Runs Batted In": f"pp;0;ss;rbi;{points}",
        "Alternate Hits": f"pp;0;ss;hit;{points}",
        "Player Total Bases": f"pp;0;ou;tb;{points}",

        #NHL switches
        re.compile(r'^Away Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Away Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        re.compile(r'^Home Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Home Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        "Home Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Away Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Home Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",
        "Away Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",

    }

    # Return the result based on the unit
    return switcher.get(unit, None)

def match_variable_event_class(event_class, patterns):
    for pattern in patterns:
        # Replace ? with a regex pattern that matches any letter
        regex_pattern = re.sub(r'\?', r'[A-Za-z]', pattern)
        if re.fullmatch(regex_pattern, event_class):
            return True
    return False

def gigaDump(dataMlb, dataNba, dataNhl, dataNfl):
    
    gamePropsEventsMLB = ['Moneyline OF', 'Run Line', 'Total Runs OF',
                        'Total Runs - AWAYTEAM OF', 'Total Runs - HOMETEAM OF']

    playerPropOUEventsMLB = ['Player home runs OF', 'Player hits OF', 'Player runs batted in OF',
                            'Player stolen bases OF', 'Pitcher strikeouts OF', 'Player Total Bases']

    playerPropAtleastEventsMLB = ['Alternate Pitcher Strikeouts',
                                'Alternate Runs Batted In', 'Alternate Hits']

    gamePropsEventsNBA = ['Point Spread', 'Moneyline',
                        'Total', 'Home Total', 'Away Total']

    playerPropOUEventsNBA = ['Player Points Over/Under', 'Player Assists Over/Under', 'Player 3-Pointers Made', 'Player Rebounds Over/Under', 'Player Turnovers', 'Player Turnovers+Steals', 'Player Turnovers+Steals+Blocks',
                            'Player Pts + Rebs + Asts Over/Under', 'Player Points + Assists Over/Under', 'Player Points + Rebounds Over/Under', 'Player Assists + Rebounds Over/Under', 'Player Steals', 'Player Blocks']

    playerPropAtleastEventsNBA = ['Alternate Points', 'Alternate Assists', 'Alternate Threes', 'Alternate Rebounds', 'Alternate Steals',
                                'Alternate Blocks', 'Alternate Turnovers', 'Player To Record A Double Double', 'Player To Record A Triple Double']

    gamePropsEventsNHL = ['Puck Line', 'Total OF', 'Money Line OF']

    playerPropOUEventsVariableNHL = [
        'Away Player ? Points Over/Under', 'Away Player ? Assists Over/Under', 'Home Goalie Saves Over/Under', 
        'Away Goalie Saves Over/Under', 'Home Goalie Shutout Over/Under', 'Away Goalie Shutout Over/Under', 
        'Home Player ? Points Over/Under', 'Home Player ? Assists Over/Under']

    gamePropsEvents = gamePropsEventsMLB + gamePropsEventsNBA + gamePropsEventsNHL
    playerPropOUEvents = playerPropOUEventsMLB + \
        playerPropOUEventsNBA + playerPropOUEventsVariableNHL
    playerPropAtleastEvents = playerPropAtleastEventsMLB + \
        playerPropAtleastEventsNBA + playerPropAtleastEventsMLB

    league = []
    teams = []
    points = []
    odds = []
    americanOdds = []
    side = []
    category = []
    names = []
    designation = []
    games = []
    keys = []

    for x in dataMlb['events']:
        games.append(x['key'])

    for x in dataNba['events']:
        games.append(x['key'])
    
    for x in dataNhl['events']:
        games.append(x['key'])

    for x in dataNfl['events']:
        games.append(x['key'])

    frames = []
    urls = []
    timer = time.time()

    for x in games:
        urls.append('https://api.on.pointsbet.com/api/mes/v3/events/'+x)
        gameHeaders = {
            "authority": "api.on.pointsbet.com",
            "method": "GET",
            "path": "/api/mes/v3/events/"+x,
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

    rs = (grequests.get(u, headers=gameHeaders) for u in urls)
    rs = grequests.map(rs)

    print(time.time()-timer)

    for x in rs:
        data = x.json()
        homeAwayTeams = data['awayTeam'] + \
            '(away)' + ' vs ' + data['homeTeam'] + '(home)'
        markets = data['fixedOddsMarkets']
        if data['competitionName'] == 'National Hockey League':
            sport = 'NHL'
        else:
            sport = data['competitionName']
        for market in markets:
            key = ' '
            if (market['eventClass'] in gamePropsEvents or 
                market['eventClass'] in playerPropOUEvents or 
                market['eventClass'] in playerPropAtleastEvents or 
                sport == 'NFL'):
                for prop in market['outcomes']:
                    teams.append(homeAwayTeams)
                    category.append(market['eventClass'])
                    league.append(sport)
                    side.append(prop['side'])
                    points.append(prop['points'])
                    odds.append(prop['price'])
                    americanOdds.append(decimal_to_american(prop['price']))
                    keys.append(makeKey(market['eventClass'], prop['points']))
                    if 'Over' in prop['name'] or 'Alternate' in prop['groupByHeader']:
                        designation.append('over')
                    elif 'Under' in prop['name']:
                        designation.append('under')
                    else:
                        designation.append('')
                    if ('Player' in market['groupName'] or
                        'Goalie' in market['groupName'] or 
                        'Alternate' in market['groupName']):
                        playerName = re.split(r'(\d+| To | Over | Under | \( )', prop['name'], 1)[0].strip()
                        nsplit = playerName.split()
                        names.append(nsplit[0][0] + '. ' + nsplit[1])
                    else:
                        names.append(prop['name'])
            if (match_variable_event_class(market['eventClass'], playerPropOUEventsVariableNHL)):
                for prop in market['outcomes']:
                    teams.append(homeAwayTeams)
                    category.append(market['eventClass'])
                    league.append(sport)
                    side.append('')
                    odds.append(prop['price'])
                    americanOdds.append(decimal_to_american(prop['price']))
                    keys.append(makeKey(market['eventClass'], prop['points']))
                    if 'Over' in prop['name']:
                        designation.append('over')
                        names.append(prop['name'].split('Over')[0].strip())
                        points.append(float(prop['name'].split('Over')[1].strip()))
                    elif 'Under' in prop['name']:
                        designation.append('under')
                        names.append(prop['name'].split('Under')[0].strip())
                        points.append(float(prop['name'].split('Under')[1].strip()))

    print(len(teams), len(category), len(league), len(side), len(names), len(points), len(odds), len(americanOdds), len(keys))

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': category, 'Designation': designation, 
                       'Side': side, 'Name': names, 'Points': points, 'PB Decimal Odds': odds, 'PB American Odds': americanOdds, 'Key': keys})
    
    frames.append(df)

    df = pd.concat(frames)

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/PointsBetGigaDump.csv', index=False)

class MyCmd(cmd.Cmd):
    prompt = '> '

    def __init__(self):    #initalize console with default values set to MLB
        super(MyCmd, self).__init__()
        self.data = getDataMlb()
        self.gameId = getGameId(self.data)
        self.league = 'Mlb'

    def do_set_gameid(self, arg):
        """Set the gameId"""
        self.gameId = arg

    def do_list_gameids(self, arg):
        """List the gameIds"""
        listGameIds(self.data)

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

    def do_get_game_data(self, arg):
        """Call the getGameData function"""
        getGameData(self.gameId)

    def do_game_dump(self, arg):
        """Call the gameDump function"""
        gameId = self.gameId
        gameDump(gameId)

    def do_get_game_id(self, arg):
        """Call the getGameId function"""
        getGameId(self.data)

    def do_gd(self, arg):
        """Call the gigaDump function"""
        x = time.time()
        mlb = getDataMlb()
        nba = getDataNba()
        nhl = getDataNhl()
        nfl = getDataNfl()
        print(time.time()-x)
        gigaDump(mlb, nba, nhl, nfl)
        print(time.time()-x)

    def do_game_json(self, arg):
        """Call the gameJson function"""
        gameJson(self.gameId)

    def do_exit(self, arg):
        """Exit the program"""
        return True
    
    def do_q(self, arg):
        """Exit the program"""
        return True

if __name__ == '__main__':
    MyCmd().cmdloop()