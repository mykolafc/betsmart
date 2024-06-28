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


'''def getDataNba():
    url = "https://api.on.DraftKings.com/api/v2/competitions/105/events/featured?includeLive=false&page=1"

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.DraftKings.com',
        'path': '/api/v2/competitions/105/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.DraftKings.com',
        #'If-Modified-Since': formatdate(timeval=datetime.now().timestamp(), localtime=False, usegmt=True),
        'Origin': 'https://on.DraftKings.ca',
        'Referer': 'https://on.DraftKings.ca/',
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
    url = "https://api.on.DraftKings.com/api/v2/competitions/18917/events/featured?includeLive=false&page=1"

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.DraftKings.com',
        'path': '/api/v2/competitions/194/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.DraftKings.com',
        #'If-Modified-Since': 'Fri, 31 May 2024 17:27:00 GMT',
        'Origin': 'https://on.DraftKings.ca',
        'Referer': 'https://on.DraftKings.ca/',
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
'''

def getDataMlb():
    # This should return the JSON file of the mlb front page from DraftKings
    # I realized the problem is that we didnt include the headers parameter in the get request

    # It's possible that some things in this link variable so it might not always be this EXACT link
    url = "https://sportsbook-nash-caon.draftkings.com/sites/CA-ON-SB/api/v5/eventgroups/84240?format=json"

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://sportsbook.draftkings.com/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data
'''
def getDataNfl():
    url = 'https://api.on.DraftKings.com/api/v2/competitions/6/events/featured?includeLive=false&page=1'

    headers = {
        'method': 'GET',
        'scheme': 'https',
        'authority': 'api.on.DraftKings.com',
        'path': '/api/v2/competitions/194/events/featured?includeLive=false&page=1',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.on.DraftKings.com',
        #'If-Modified-Since': 'Fri, 31 May 2024 17:27:00 GMT',
        'Origin': 'https://on.DraftKings.ca',
        'Referer': 'https://on.DraftKings.ca/',
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
'''
def listGameIds(data):
    gameIds = []
    for category in data['eventGroup']['offerCategories']:
        if 'offerSubcategoryDescriptors' in category:
            for descriptor in category['offerSubcategoryDescriptors']:
                if 'offerSubcategory' in descriptor:  
                    for offer in descriptor['offerSubcategory']['offers']:
                        gameIds.append(offer[0]['eventId'])
    return gameIds

def decimal_to_american(decimal_odds):
    if decimal_odds == 1.0:
        american_odds = 0
    elif decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)

def getGameData(gameId):

    gameUrl = "https://sportsbook-ca-on.draftkings.com/api/team/markets/dkcaon/v3/event/"+gameId+"?format=json"

    gameHeaders = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://sportsbook.draftkings.com/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
    }
    
    gameResponse = requests.get(gameUrl, headers=gameHeaders)
    data = gameResponse.json()

    with open('DraftKingsGame'+gameId+'.json', 'w') as f:
        json.dump(data, f, indent=4)

    return data

def gameJson(gameId):
    gameUrl = "https://api.on.DraftKings.com/api/mes/v3/events/"+gameId

    gameHeaders = {
        "authority": "api.on.DraftKings.com",
        "method": "GET",
        "path": "/api/mes/v3/events/"+gameId,
        "scheme": "https",
        "Accept": "application/json, text/plain, /",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        #"If-Modified-Since": "Fri, 24 May 2024 17:13:09 GMT",
        "Origin": "https://on.DraftKings.ca/",
        "Priority": "u=1, i",
        "Referer": "https://on.DraftKings.ca/",
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

    with open('DraftKingsGame'+gameId+'.json', 'w') as f:
        json.dump(data, f, indent=4)

def jsonDump(data, league):
    with open('DraftKings'+league+'.json', 'w') as f:
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
    df.to_csv('DraftKings'+league+'.csv', index=False)

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
        #NBA game switches
        "Point Spread": f"s;0;s;{points}",
        "Moneyline": f"s;0;m",
        "Total": f"s;0;ou;{points}",
        "Home Total": f"s;0;tt;{points};home",
        "Away Total": f"s;0;tt;{points};away",

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
        #MLB game switches
        "Moneyline OF": f"s;0;m",
        "Run Line": f"s;0;s;{points}",
        "Total Runs OF": f"s;0;ou;{points}",
        "Total Runs - AWAYTEAM OF": f"s;0;tt;{points};away",
        "Total Runs - HOMETEAM OF": f"s;0;tt;{points};home",

        #NHL switches
        re.compile(r'^Away Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Away Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        re.compile(r'^Home Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Home Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        "Home Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Away Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Home Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",
        "Away Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",
        #NHL game switches
        "Puck Line": f"s;0;s;{points}",
        "Total OF": f"s;0;ou;{points}",
        "Money Line OF": f"s;0;m",

    }

    for key, value in switcher.items():
        if isinstance(key, re.Pattern):  # Check if the key is a compiled regex pattern
            if re.match(key, unit):
                return value
        elif key == unit:
            return value

    return None

    for pattern in patterns:
        # Replace ? with a regex pattern that matches any letter
        regex_pattern = re.sub(r'\?', r'[A-Za-z]', pattern)
        if re.fullmatch(regex_pattern, event_class):
            return True
    return False

def gigaDump(dataMlb):
    
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

    games = listGameIds(dataMlb)

    frames = []
    urls = []
    timer = time.time()

    for x in games:
        urls.append("https://sportsbook-ca-on.draftkings.com/api/team/markets/dkcaon/v3/event/"+ x +"?format=json")
        gameHeaders = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://sportsbook.draftkings.com/',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
        }

    rs = (grequests.get(u, headers=gameHeaders) for u in urls)
    rs = grequests.map(rs)

    print(time.time()-timer)

    for x in rs:
        data = x.json()
        homeTeam = data['event']['teamName2']
        awayTeam = data['event']['teamName1']
        homeAwayTeams = awayTeam + \
            '(away)' + ' vs ' + homeTeam + '(home)'
        currentLeague = (data['event']['eventGroupName'])

        #Game Props a.k.a. eventCategories index = 1
        components = data['eventCategories'][1]['componentizedOffers']
        print(data['eventCategories'][1]['name'])
        for component in components:
            for offers in component['offers']:
                for offer in offers:
                    for outcome in offer['outcomes']:
                        print("Here is an outcome : "+ str(outcome))
                        league.append(currentLeague)
                        teams.append(homeAwayTeams)
                        category.append(offer['label'])
                        if homeTeam in outcome['label']:
                            side.append('home')
                        elif awayTeam in outcome['label']:
                            side.append('away')
                        else:
                            side.append(None)
                        points.append(outcome.get('line', None))
                        odds.append(outcome['oddsDecimal'])
                        americanOdds.append(outcome['oddsAmerican'])
                        names.append(None)
                        designation.append(None)
                        keys.append('key')
                        print("Done with iteration for this outcome!")

        #Player Props a.k.a. eventCategories index = 2 for batters and 3 for pitchers
        for i in range(2, 3):
            components = data['eventCategories'][i]['componentizedOffers']
            for component in components:
                for offers in component['offers']:
                    for offer in offers:
                        for outcome in offer['outcomes']:
                            print("Here is a "+ str(i) +" outcome")
                            league.append(currentLeague)
                            teams.append(homeAwayTeams)
                            category.append(component['subcategoryName'])
                            side.append(None)
                            points.append(outcome.get('line', None))
                            odds.append(outcome['oddsDecimal'])
                            americanOdds.append(outcome['oddsAmerican'])
                            names.append(outcome.get('playerNameIdentifier', None))
                            designation.append(outcome.get('label', None).lower())
                            keys.append('key')
                            print("Done with iteration for this outcome!")

    print(len(teams), len(category), len(league), len(designation), len(side), len(names), len(points), len(odds), len(americanOdds), len(keys))

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': category, 'Designation': designation, 
                       'Side': side, 'Name': names, 'Points': points, 'Odds': odds, 'American Odds': americanOdds, 'Key': keys})
    
    frames.append(df)

    df = pd.concat(frames)

    df.to_csv('DraftKingsGigaDump.csv', index=False)

class MyCmd(cmd.Cmd):
    prompt = '> '

    def __init__(self):    #initalize console with default values set to MLB
        super(MyCmd, self).__init__()
        self.data = getDataMlb()
        self.gameId = listGameIds(self.data)[0]
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
        #nba = getDataNba()
        #nhl = getDataNhl()
        #nfl = getDataNfl()
        print(time.time()-x)
        gigaDump(mlb)
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