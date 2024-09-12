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


def getData():
    # From what I understand this link gives us the eventIds of all sports

    # It's possible that some things in this link variable so it might not always be this EXACT link
    url = "https://sbapi.on.sportsbook.fanduel.ca/api/content-managed-page?page=HOMEPAGE&prominentCard=false&pulseScalingEnable=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"

    headers = {
        'accept': 'application/json',
        'referer': 'https://on.sportsbook.fanduel.ca/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
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

# This function checks if a game is live based off its time and date


def isNotLive(openDate):
    # Parse the given date string into a datetime object (assuming it's in UTC)
    target_time = datetime.strptime(openDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    threshold_time = target_time - timedelta(hours=4, minutes=2)
    current_time = datetime.now()
    # Check if the current time is before the threshold
    return current_time < threshold_time


# For now this is only fetching MLB eventIds
def listGameIds(data):
    gameIds = dict()
    for event in data['attachments']['events'].values():
        # This number is the number representing that its an mlb or nfl game, [11196870, 12282733]
        if event['competitionId'] in [11196870, 12282733] and event['name'] not in ['NFL', 'MLB'] and isNotLive(event['openDate']):
            gameIds[event['eventId']] = event['competitionId']
    return gameIds


def decimal_to_american(decimal_odds):
    if decimal_odds == 1.0:
        american_odds = 0
    elif decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)


def makeKey(unit, points, name=None):
    period = -1
    if name == 'Game':
        period = 0
    switcher = {
        # NBA switches
        "H": f"pp;0;ss;asst;{points}",
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
        # NBA game switches
        "Point Spread": f"s;0;s;{points}",
        "Moneyline": f"s;0;m",
        "Total": f"s;0;ou;{points}",
        "Home Total": f"s;0;tt;{points};home",
        "Away Total": f"s;0;tt;{points};away",

        # THIS IS THE ONLY CURRENTLY ACCURATE KEY MAKER, THE REST IS FROM DRAFTKINGS
        # MLB switches
        re.compile(r'^PITCHER_[A-Z]_TOTAL_STRIKEOUTS'): f"pp;0;ou;so;{points}",
        re.compile(r'^PITCHER_[A-Z]_STRIKEOUTS'): f"pp;0;ss;so;{points}",
        "TO_HIT_A_HOME_RUN": f"pp;0;ss;hr;0.5",
        "PLAYER_TO_RECORD_A_HIT": f"pp;0;ss;hit;0.5",
        "PLAYER_TO_RECORD_2+_HITS": f"pp;0;ss;hit;1.5",
        "PLAYER_TO_RECORD_3+_HITS": f"pp;0;ss;hit;2.5",
        "TO_RECORD_A_STOLEN_BASE": f"pp;0;ss;sb;0.5",
        "TO_RECORD_A_RUN": f"pp;0;ss;run;0.5",
        "TO_RECORD_2+_RUNS": f"pp;0;ss;run;1.5",
        "TO_RECORD_3+_RUNS": f"pp;0;ss;run;2.5",
        "TO_RECORD_AN_RBI": f"pp;0;ss;rbi;0.5",
        "TO_RECORD_2+_RBIS": f"pp;0;ss;rbi;1.5",
        # For sake of comparison, im writing the next one down as an Over/Under in the key and not an alternate
        "TO_RECORD_2+_TOTAL_BASES": f"pp;0;ou;tb;1.5",
        "TO_RECORD_3+_TOTAL_BASES": f"pp;0;ss;tb;2.5",
        "TO_RECORD_4+_TOTAL_BASES": f"pp;0;ss;tb;3.5",
        "TO_RECORD_5+_TOTAL_BASES": f"pp;0;ss;tb;4.5",
        "TO_HIT_A_SINGLE": f"pp;0;ss;sin;0.5",
        "TO_HIT_A_DOUBLE": f"pp;0;ss;dbl;0.5",
        "TO_HIT_A_TRIPLE": f"pp;0;ss;trp;0.5",
        # MLB game switches
        "MONEY_LINE": f"s;0;m",
        "MATCH_HANDICAP_(2-WAY)": f"s;0;s;{points}",
        "TOTAL_POINTS_(OVER/UNDER)": f"s;0;ou;{points}",
        "ALTERNATE_TOTAL_RUNS": f"s;0;ou;{points}",
        "AWAY_TOTAL_RUNS": f"s;0;tt;{points};away",
        "AWAY_TEAM_ALTERNATE_TOTAL_RUNS": f"s;0;tt;{points};away",
        "HOME_TOTAL_RUNS": f"s;0;tt;{points};home",
        "HOME_TEAM_ALTERNATE_TOTAL_RUNS": f"s;0;tt;{points};home",

        # Nfl switches
        "ALTERNATE_TOTAL": f"s;0;ou;{points}",
        "AWAY_TOTAL_POINTS": f"s;0;tt;{points};away",
        "HOME_TOTAL_POINTS": f"s;0;tt;{points};home",
        "ANY_TIME_TOUCHDOWN_SCORER": f"pp;0;ou;td;0.5",

        re.compile(r'^PLAYER_[A-Z]_-_ALT_PASSING_TDS$'): f"pp;0;ss;tdp;{points}",
        re.compile(r'^PLAYER_[A-Z]_-_ALT_PASSING_YARDS$'): f"pp;0;ss;pay;{points}",
        re.compile(r'^PLAYER_[A-Z]_-_ALT_RUSH_YARDS$'): f"pp;0;ss;ruy;{points}",
        re.compile(r'^PLAYER_[A-Z]_-_ALT_RECEIVING_YARDS$'): f"pp;0;ss;rey;{points}",
        re.compile(r'^PLAYER_[A-Z]_-_ALT_RECEPTIONS$'): f'pp;0;ss;rec;{points}',

        re.compile(r'^PLAYER_[A-Z]_TOTAL_RECEIVING_YARDS$'): f'pp;0;ou;rey;{points}',
        re.compile(r'^PLAYER_[A-Z]_LONGEST_RECEPTION$'): f'pp;0;ou;lrc;{points}',
        re.compile(r'^PLAYER_[A-Z]_TOTAL_RECEPTIONS$'): f'pp;0;ou;rec;{points}',
        re.compile(r'^PLAYER_[A-Z]_INTERCEPTION$'): f'pp;0;ou;int;0.5',
        re.compile(r'^PLAYER_[A-Z]_LONGEST_PASS_COMPLETION$'): f'pp;0;ou;lco;{points}',
        re.compile(r'^PLAYER_[A-Z]_PASS_ATTEMPTS$'): f'pp;0;ou;pat;{points}',
        re.compile(r'^PLAYER_[A-Z]_TOTAL_PASS_COMPLETIONS$'): f'pp;0;ou;com;{points}',
        re.compile(r'PLAYER_[A-Z]_TOTAL_PASSING_TOUCHDOWNS^$'): f'pp;0;ou;tdp;{points}',
        re.compile(r'^PLAYER_[A-Z]_TOTAL_PASSING_YARDS$'): f'pp;0;ou;pay;{points}',
        re.compile(r'^PLAYER_[A-Z]_TOTAL_RUSH_ATTEMPTS$'): f'pp;0;ou;rut;{points}',
        re.compile(r'^PLAYER_[A-Z]_TOTAL_RUSHING_YARDS$'): f'pp;0;ou;ruy;{points}',
        re.compile(r'^PLAYER_[A-Z]_LONGEST_RUSH$'): f'pp;0;ou;lru;{points}',

        # NHL switches
        re.compile(r'^Away Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Away Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        re.compile(r'^Home Player [A-Z] Points Over/Under$'): f"pp;0;ou;pts;{points}",
        re.compile(r'^Home Player [A-Z] Assists Over/Under$'): f"pp;0;ou;asst;{points}",
        "Home Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Away Goalie Saves Over/Under": f"pp;0;ou;saves;{points}",
        "Home Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",
        "Away Goalie Shutout Over/Under": f"pp;0;ou;sho;{points}",
        # NHL game switches
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


def getTeamName(name):
    switcher = {
        # Mlb
        "Arizona Diamondbacks": "ARI",
        "Atlanta Braves": "ATL",
        "Baltimore Orioles": "BAL",
        "Boston Red Sox": "BOS",
        "Chicago White Sox": "CWS",
        "Chicago Cubs": "CHC",
        "Cincinnati Reds": "CIN",
        "Cleveland Guardians": "CLE",
        "Colorado Rockies": "COL",
        "Detroit Tigers": "DET",
        "Houston Astros": "HOU",
        "Miami Marlins": "MIA",
        "Kansas City Royals": "KAN",
        "Los Angeles Angels": "LAA",
        "Los Angeles Dodgers": "LAD",
        "Milwaukee Brewers": "MIL",
        "Minnesota Twins": "MIN",
        "New York Yankees": "NYY",
        "New York Mets": "NYM",
        "Oakland Athletics": "OAK",
        "Philadelphia Phillies": "PHI",
        "Pittsburgh Pirates": "PIT",
        "San Diego Padres": "SD",
        "San Francisco Giants": "SF",
        "Seattle Mariners": "SEA",
        "St. Louis Cardinals": "STL",
        "Tampa Bay Rays": "TB",
        "Texas Rangers": "TEX",
        "Toronto Blue Jays": "TOR",
        "Washington Nationals": "WAS",

        # NFL
        "Arizona Cardinals": "ARI",
        "Atlanta Falcons": "ATL",
        "Baltimore Ravens": "BAL",
        "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL",
        "Denver Broncos": "DEN",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GB",
        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Kansas City Chiefs": "KC",
        "Las Vegas Raiders": "LV",
        "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR",
        "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN",
        "New England Patriots": "NE",
        "New Orleans Saints": "NO",
        "New York Giants": "NYG",
        "New York Jets": "NYJ",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "San Francisco 49ers": "SF",
        "Seattle Seahawks": "SEA",
        "Tampa Bay Buccaneers": "TB",
        "Tennessee Titans": "TEN",
        "Washington Commanders": "WAS"
    }

    return switcher.get(name, name)


def getLeague(competitionId):
    switcher = {
        11196870: "MLB",
        12282733: 'NFL',
        # Add other leagues in the future
    }

    return switcher.get(competitionId, 'Unknown competitionId')


# This function is going to make the request links useful for FanDuel
def makeRequestLinks(data):
    nflProps = ['passing-props', 'receiving-props', 'rushing-props']
    games = listGameIds(data)
    urls = []

    for x in games:
        urls.append({'url': "https://sbapi.on.sportsbook.fanduel.ca/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=" + str(x) + "&tab=popular&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true",
                     'headers': {
                         'accept': 'application/json',
                         'referer': 'https://on.sportsbook.fanduel.ca/',
                         'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                         'sec-ch-ua-mobile': '?1',
                         'sec-ch-ua-platform': '"Android"',
                         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
        }})
        if games[x] == 12282733:
            for prop in nflProps:
                urls.append({'url': 'https://sbapi.az.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=' + str(x) + '&tab=' + prop + '&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true&useQuickBetsNFL=true',
                            'headers': {
                                "authority": "sbapi.az.sportsbook.fanduel.com",
                                "method": "GET",
                                "path": "/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=" + str(x) + "&tab=" + prop + "&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true&useQuickBetsNFL=true",
                                "scheme": "https",
                                "accept": "application/json",
                                "accept-encoding": "identity",
                                "accept-language": "en-US,en;q=0.9",
                                "origin": "https://sportsbook.fanduel.com",
                                "referer": "https://sportsbook.fanduel.com/",
                                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
                }})
    return urls


# For Game props
def validMarketTypeGame(marketType):
    if marketType in ['MONEY_LINE', 'MATCH_HANDICAP_(2-WAY)', "ALTERNATE_TOTAL_RUNS", "TOTAL_POINTS_(OVER/UNDER)",
                      "AWAY_TOTAL_RUNS", "HOME_TOTAL_RUNS", "AWAY_TEAM_ALTERNATE_TOTAL_RUNS", "HOME_TEAM_ALTERNATE_TOTAL_RUNS",
                      "AWAY_TOTAL_POINTS", "HOME_TOTAL_POINTS", "ALTERNATE_TOTAL"]:
        return True
    else:
        return False


# For Over/Under
def validMarketTypeOUPP(marketType):
    patternsOUPP = [
        r'^PITCHER_[A-Z]_TOTAL_STRIKEOUTS$',

        r'^PLAYER_[A-Z]_TOTAL_RECEIVING_YARDS$',
        r'^PLAYER_[A-Z]_LONGEST_RECEPTION$',
        r'^PLAYER_[A-Z]_TOTAL_RECEPTIONS$',

        r'^PLAYER_[A-Z]_INTERCEPTION$',
        r'^PLAYER_[A-Z]_LONGEST_PASS_COMPLETION$',
        r'^PLAYER_[A-Z]_PASS_ATTEMPTS$',
        r'^PLAYER_[A-Z]_TOTAL_PASS_COMPLETIONS$',
        r'PLAYER_[A-Z]_TOTAL_PASSING_TOUCHDOWNS^$',
        r'^PLAYER_[A-Z]_TOTAL_PASSING_YARDS$',

        r'^PLAYER_[A-Z]_TOTAL_RUSH_ATTEMPTS$',
        r'^PLAYER_[A-Z]_TOTAL_RUSHING_YARDS$',
        r'^PLAYER_[A-Z]_LONGEST_RUSH$',

        # r'^$',
        # r'^$'
    ]
    if any(re.match(pattern, marketType) for pattern in patternsOUPP):
        return True
    else:
        return False


# For Atleasts
def validMarketTypeAlternatePP(marketType):
    patternsAlternatePP = [
        r'^PITCHER_[A-Z]_STRIKEOUTS$',

        r'^PLAYER_[A-Z]_-_ALT_PASSING_TDS$',
        r'^PLAYER_[A-Z]_-_ALT_PASSING_YARDS$',

        r'^PLAYER_[A-Z]_-_ALT_RUSH_YARDS$',

        r'^PLAYER_[A-Z]_-_ALT_RECEIVING_YARDS$',
        r'^PLAYER_[A-Z]_-_ALT_RECEPTIONS$',

        # r'^$',
        # r'^$',
        # r'^$'
        # Add more patterns here
    ]

    if marketType in ["TO_HIT_A_HOME_RUN", "PLAYER_TO_RECORD_A_HIT", "PLAYER_TO_RECORD_2+_HITS", "PLAYER_TO_RECORD_3+_HITS", "TO_RECORD_A_STOLEN_BASE", "TO_RECORD_A_RUN",
                      "TO_RECORD_2+_RUNS", "TO_RECORD_3+_RUNS", "TO_RECORD_AN_RBI", "TO_RECORD_2+_RBIS", "TO_RECORD_2+_TOTAL_BASES", "TO_RECORD_3+_TOTAL_BASES",
                      "TO_RECORD_4+_TOTAL_BASES", "TO_RECORD_5+_TOTAL_BASES", "TO_HIT_A_SINGLE", "TO_HIT_A_DOUBLE", "TO_HIT_A_TRIPLE",
                      "ANY_TIME_TOUCHDOWN_SCORER", ]:
        return True
    elif any(re.match(pattern, marketType) for pattern in patternsAlternatePP):
        return True
    else:
        return False


def gigaDump2(response):
    league = []
    teams = []
    points = []
    odds = []
    americanOdds = []
    side = []
    categories = []
    names = []
    designation = []
    games = []
    keys = []
    dates = []

    # This is saving all the games and their dates to see if there are multiple games in a day
    gamesDatesDict = dict()

    for x in response:
        data = x.json()

        eventId = list(data['attachments']['events'].keys())[0]
        eventName = data['attachments']['events'][eventId]['name']

        # if eventName == 'Las Vegas Raiders @ Los Angeles Chargers':
        #     with open('fanduelNflGame.json', 'w') as file:
        #         json.dump(data, file, indent=4)

        matchMLB = re.match(r"(.+?) \(.+?\) @ (.+?) \(.+?\)", eventName)
        matchNFL = re.match(r"(.+) @ (.+)", eventName)
        if matchMLB:
            # MLB format matched
            awayTeam = matchMLB.group(1)
            homeTeam = matchMLB.group(2)
        elif matchNFL:
            # NFL format matched
            awayTeam = matchNFL.group(1)
            homeTeam = matchNFL.group(2)
        homeAwayTeams = getTeamName(awayTeam) + \
            '(away)' + ' vs ' + getTeamName(homeTeam) + '(home)'
        currentLeague = getLeague(
            data['attachments']['events'][eventId]['competitionId'])

        # The date is sometimes after midnight of the next day
        # this code makes sure it grabs the date of the start of the game
        datetimeStr = data['attachments']['events'][eventId]['openDate']
        dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S.%fZ")
        if dt.time() < datetime.strptime("05:30:00", "%H:%M:%S").time():
            dt -= timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")

        # TEST THIS AUGUST 11 BECAUSE IDK IF IT WORKS!!!!!!!!!!!
        # if gamesDatesDict.get(homeAwayTeams) == date:
        #     teamsArray = np.array(teams)
        #     teamsArray = np.where(
        #         teamsArray == homeAwayTeams, teamsArray + '1', teamsArray)
        #     teams = teamsArray.tolist()

        # gamesDatesDict[homeAwayTeams] = date

        markets = data['attachments']['markets']

        for market in markets.values():
            if validMarketTypeGame(market['marketType']):
                for runner in market['runners']:
                    league.append(currentLeague)
                    teams.append(homeAwayTeams)

                    # This checks if a string ends with (0.5) for ex,
                    # sometimes this is where the line is actually stored rather than the handicap
                    if bool(re.search(r"\(\d+(\.\d+)?\)$", runner['runnerName'])):
                        number = re.search(
                            r"\((\d+(\.\d+)?)\)$", runner['runnerName']).group(1)
                        point = float(number)
                        points.append(point)
                    else:
                        point = runner['handicap']
                        points.append(point)

                    if 'winRunnerOdds' not in runner:
                        print(runner)

                    odds.append(runner['winRunnerOdds']
                                ['trueOdds']['decimalOdds']['decimalOdds'])
                    americanOdds.append(
                        runner['winRunnerOdds']['americanDisplayOdds']['americanOddsInt'])
                    if runner['result'].get('type', '').lower() in ['away', 'home']:
                        side.append(runner['result']['type'].lower())
                        designation.append(None)
                    elif runner['result'].get('type', '').lower() in ['under', 'over']:
                        designation.append(runner['result']['type'].lower())
                        if market['marketType'][:4] in ['AWAY', 'HOME']:
                            side.append(market['marketType'][:4].lower())
                        else:
                            side.append(None)
                    elif runner['runnerName'].split(' ')[0].lower() in ['under', 'over']:
                        designation.append(
                            runner['runnerName'].split(' ')[0].lower())
                        if market['marketType'][:4] in ['AWAY', 'HOME']:
                            side.append(market['marketType'][:4].lower())
                        else:
                            side.append(None)
                    categories.append(market['marketName'])
                    names.append(None)

                    # This makes sure that the run line is the same for both home and away inside the key
                    if market['marketType'] == 'MATCH_HANDICAP_(2-WAY)' and runner['result'].get('type', '') == 'AWAY':
                        keys.append(makeKey(market['marketType'], point * -1))
                    else:
                        keys.append(makeKey(market['marketType'], point))
                    dates.append(date)

            elif validMarketTypeOUPP(market['marketType']):
                for runner in market['runners']:
                    league.append(currentLeague)
                    teams.append(homeAwayTeams)
                    point = runner['handicap']
                    points.append(point)
                    odds.append(runner['winRunnerOdds']
                                ['trueOdds']['decimalOdds']['decimalOdds'])
                    americanOdds.append(
                        runner['winRunnerOdds']['americanDisplayOdds']['americanOddsInt'])
                    side.append(None)

                    if 'Yes' in runner['runnerName']:
                        designation.append('over')
                    elif 'No' in runner['runnerName']:
                        designation.append('under')
                    else:
                        if 'type' not in runner['result']:
                            print(runner['runnerName'])
                            print(market['marketType'])
                        designation.append(runner['result']['type'].lower())

                    categories.append(market['marketName'])

                    # Finds a way to store the names same way as all the other sites do
                    playerName = re.sub(r'\s\d.*', '', runner['runnerName'])
                    nsplit = playerName.split()
                    name = playerName.replace(
                        nsplit[0], nsplit[0][0] + '.', 1).replace('Over', '').replace('Under', '').replace('Yes', '').replace('No', '').strip()
                    names.append(name)
                    keys.append(makeKey(market['marketType'], point))
                    dates.append(date)

            elif validMarketTypeAlternatePP(market['marketType']):
                point = 'Cant find point'
                # This gets the points value from the marketType since it isnt stored inside handicap
                if bool(re.search(r'\d+\+', market['marketType'])):
                    number = re.search(
                        r"(\d+)\+", market['marketType']).group(1)
                    point = float(number)-0.5
                elif bool(re.search(r'(_A_|_AN_)', market['marketType'])):
                    point = 0.5
                for runner in market['runners']:
                    league.append(currentLeague)
                    teams.append(homeAwayTeams)

                    # This checks to see if the points value is in the name, else it goes with the marketType value
                    if bool(re.search(r'\d+\+', runner['runnerName'])):
                        number = re.search(
                            r"(\d+)\+", runner['runnerName']).group(1)
                        point = float(number)-0.5
                        points.append(point)
                    else:
                        points.append(point)

                    if 'winRunnerOdds' not in runner:
                        print(
                            f'Error, winRunnerOdds cant be found, here is the runner: ', runner)
                    odds.append(runner['winRunnerOdds']
                                ['trueOdds']['decimalOdds']['decimalOdds'])
                    americanOdds.append(
                        runner['winRunnerOdds']['americanDisplayOdds']['americanOddsInt'])
                    side.append(None)
                    categories.append(market['marketName'])
                    designation.append('over')

                    # Finds a way to store the names same way as all the other sites do
                    playerName = re.sub(r'\s\d.*', '', runner['runnerName'])
                    nsplit = playerName.split()
                    name = playerName.replace(
                        nsplit[0], nsplit[0][0] + '.', 1).replace('Over', '').replace('Under', '').strip()
                    names.append(name)
                    keys.append(makeKey(market['marketType'], point))
                    dates.append(date)

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': categories, 'Designation': designation,
                       'Side': side, 'Name': names, 'Points': points, 'FD Decimal Odds': odds, 'FD American Odds': americanOdds, 'Key': keys, 'Date': dates})
    df = df.drop_duplicates()

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/FanDuelGigaDump.csv', index=False)


class MyCmd(cmd.Cmd):
    prompt = '> '

    def __init__(self):  # initalize console with default values set to MLB
        super(MyCmd, self).__init__()
        self.data = getData()
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
        # nba = getDataNba()
        # nhl = getDataNhl()
        # nfl = getDataNfl()
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
