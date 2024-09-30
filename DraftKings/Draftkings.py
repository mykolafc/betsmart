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


def getDataMlbNEW():
    # This should return the JSON file of the mlb front page from DraftKings
    # I realized the problem is that we didnt include the headers parameter in the get request

    # It's possible that some things in this link variable so it might not always be this EXACT link
    url = "https://sportsbook-nash.draftkings.com/api/sportscontent/navigation/dkcaon/v1/nav/leagues/84240?format=json"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://sportsbook.draftkings.com",
        "referer": "https://sportsbook.draftkings.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "x-client-feature": "event-slider",
        "x-client-name": "web",
        "x-client-page": "event",
        "x-client-version": "2439.1.1.22",
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data


def getDataNfl():
    url = "https://sportsbook-nash.draftkings.com/api/sportscontent/navigation/dkcaon/v1/nav/leagues/88808?format=json"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://sportsbook.draftkings.com",
        "referer": "https://sportsbook.draftkings.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "x-client-feature": "event-slider",
        "x-client-name": "web",
        "x-client-page": "event",
        "x-client-version": "2439.1.1.22",
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data


def isNotLive(startDate):
    # Remove the last digit of the microseconds to match Python's 6-digit microsecond format
    cleaned_date_str = startDate[:-2] + 'Z'
    target_time = datetime.strptime(cleaned_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    threshold_time = target_time - timedelta(hours=4, minutes=1)
    current_time = datetime.now()
    # Check if the current time is before the threshold
    return current_time < threshold_time


def listGameIds(data):
    gameIds = []
    for event in data['eventGroup']['events']:
        if isNotLive(event['startDate']):
            gameIds.append(event['eventId'])
    return gameIds


def listGameIdsNEW(data):
    gameIds = dict()
    for event in data['events']:
        if isNotLive(event['startDate']):
            gameIds[event['eventId']] = event['eventGroupId']
    return gameIds


def decimal_to_american(decimal_odds):
    if decimal_odds == 1.0:
        american_odds = 0
    elif decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)


def fractional_to_american(fractional_odds_str):
    numerator, denominator = map(int, fractional_odds_str.split("/"))
    fraction = numerator / denominator
    if fraction >= 1:
        american_odds = fraction * 100
    else:
        american_odds = - (100 / fraction)

    return round(american_odds)


def getGameData(gameId):

    gameUrl = "https://sportsbook-ca-on.draftkings.com/api/team/markets/dkcaon/v3/event/" + \
        gameId+"?format=json"

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
        # "If-Modified-Since": "Fri, 24 May 2024 17:13:09 GMT",
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
                teams.append(x['awayTeam'] + '(away)' +
                             ' vs ' + x['homeTeam'] + '(home)')
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

        # MLB switches
        "Home Runs O/U": f"pp;0;ou;hr;{points}",
        "Home Runs Milestones": f"pp;0;ou;hr;{points}",
        "Hits O/U": f"pp;0;ou;hit;{points}",
        "Hits": f"pp;0;ss;hit;{points}",
        "Hits + Runs + RBIs": f"pp;0;ou;hrr;{points}",
        "Total Bases O/U": f"pp;0;ou;tb;{points}",
        "Total Bases": f"pp;0;ss;tb;{points}",
        "RBIs O/U": f"pp;0;ou;rbi;{points}",
        "RBIs": f"pp;0;ss;rbi;{points}",
        "Runs Scored": f"pp;0;ou;run;{points}",
        "Stolen Bases O/U": f"pp;0;ou;sb;{points}",
        "Singles": f"pp;0;ou;sin;{points}",
        "Doubles": f"pp;0;ou;dbl;{points}",
        "Walks (Batter) O/U": f"pp;0;ou;wlk;{points}",
        "Strikeouts Thrown O/U": f"pp;0;ou;so;{points}",
        "Strikeouts": f"pp;0;ou;so;{points}",
        "Strikeouts Thrown Milestones": f"pp;0;ss;so;{points}",
        "Earned Runs Allowed": f"pp;0;ou;era;{points}",
        "Walks Allowed O/U": f"pp;0;ou;wlka;{points}",
        "Walks Allowed": f"pp;0;ss;wlka;{points}",
        "Hits Allowed O/U": f"pp;0;ou;hita;{points}",
        "Hits Allowed": f"pp;0;ss;hita;{points}",
        # MLB game switches
        "Moneyline": f"s;0;m",
        "Run Line": f"s;0;s;{points}",
        "Total": f"s;0;ou;{points}",
        "Total Runs - AWAYTEAM OF": f"s;0;tt;{points};away",
        "Total Runs - HOMETEAM OF": f"s;0;tt;{points};home",

        # NFL Switches
        'Passing Yards O/U': f'pp;0;ou;pay;{points}',
        'Anytime Touchdown Scorer': f'pp;0;ou;td;0.5',
        'Alternate Passing Yards O/U': f'pp;0;ou;pay;{points}',
        'Alternate Rushing Yards O/U': f'pp;0;ou;ruy;{points}',
        'Receiving Yards Milestones': f'pp;0;ss;ruy;{points}',
        'Receiving Yards O/U': f'pp;0;ou;rey;{points}',
        'Receptions O/U': f'pp;0;ou;rec;{points}',
        'Rushing Attempts O/U': f'pp;0;ou;rut;{points}',
        'Passing Completions O/U': f'pp;0;ou;com;{points}',
        'Interceptions Thrown O/U': f'pp;0;ou;int;{points}',
        'Longest Reception O/U': f'pp;0;ou;lrc;{points}',
        # Maybe theres no over under on draftkings for this?
        'Passing Touchdowns Milestones': f'pp;0;ou;tdp;{points}',
        'Rushing Yards Milestones': f'pp;0;ss;ruy;{points}',
        'Passing Attempts O/U': f'pp;0;ou;pat;{points}',
        'Alternate Receiving Yards O/U': f'pp;0;ou;rey;{points}',
        'Passing Yards Milestones': f'pp;0;ss;pay;{points}',
        'Longest Passing Completion O/U': f'pp;0;ou;lco;{points}',
        'Spread': f's;0;s;{points}',

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


relevantPPSubCategoriesNFL = {'12093', '12094', '12438', '14113', '14114', '14115', '14117',
                              '14118', '14119', '15937', '15948', '15968', '15987', '9517', '9518', '9520', '9522', '9524'}
relevantGameSubCategoriesNFL = {'4518'}
relevantPPSubCategoriesMLB = {'11214', '12146', '12855', '12857',
                              '15221', '15520', '15524', '6607', '6719', '8025', '9872'}
relevantGameSubCategoriesMLB = {'4519'}

relevantPPSubCategories = relevantPPSubCategoriesNFL | relevantPPSubCategoriesMLB
relevantGameSubCategories = relevantGameSubCategoriesNFL | relevantGameSubCategoriesMLB

relevantSubCategories = relevantPPSubCategories | relevantGameSubCategories


def getTeamName(name):
    switcher = {
        # MLB
        "ARI Diamondbacks": "ARI",
        "ATL Braves": "ATL",
        "BAL Orioles": "BAL",
        "BOS Red Sox": "BOS",
        "CHI White Sox": "CWS",
        "CHI Cubs": "CHC",
        "CIN Reds": "CIN",
        "CLE Guardians": "CLE",
        "COL Rockies": "COL",
        "DET Tigers": "DET",
        "HOU Astros": "HOU",
        "MIA Marlins": "MIA",
        "KC Royals": "KAN",
        "LA Angels": "LAA",
        "LA Dodgers": "LAD",
        "MIL Brewers": "MIL",
        "MIN Twins": "MIN",
        "NY Yankees": "NYY",
        "NY Mets": "NYM",
        "OAK Athletics": "OAK",
        "PHI Phillies": "PHI",
        "PIT Pirates": "PIT",
        "SD Padres": "SD",
        "SF Giants": "SF",
        "SEA Mariners": "SEA",
        "STL Cardinals": "STL",
        "TB Rays": "TB",
        "TEX Rangers": "TEX",
        "TOR Blue Jays": "TOR",
        "WAS Nationals": "WAS",

        # NFL
        "ARI Cardinals": "ARI",
        "ATL Falcons": "ATL",
        "BAL Ravens": "BAL",
        "BUF Bills": "BUF",
        "CAR Panthers": "CAR",
        "CHI Bears": "CHI",
        "CIN Bengals": "CIN",
        "CLE Browns": "CLE",
        "DAL Cowboys": "DAL",
        "DEN Broncos": "DEN",
        "DET Lions": "DET",
        "GB Packers": "GB",
        "HOU Texans": "HOU",
        "IND Colts": "IND",
        "JAX Jaguars": "JAX",
        "KC Chiefs": "KC",
        "LA Rams": "LAR",
        "LAC Chargers": "LAC",
        "LV Raiders": "LV",
        "MIA Dolphins": "MIA",
        "MIN Vikings": "MIN",
        "NE Patriots": "NE",
        "NO Saints": "NO",
        "NY Giants": "NYG",
        "NY Jets": "NYJ",
        "PHI Eagles": "PHI",
        "PIT Steelers": "PIT",
        "SF 49ers": "SF",
        "SEA Seahawks": "SEA",
        "TB Buccaneers": "TB",
        "TEN Titans": "TEN",
        "WAS Commanders": "WAS",
    }

    return switcher.get(name, name)

# This function is going to make the request links useful for DraftKings


def makeRequestLinks(dataMlb):
    games = listGameIds(dataMlb)
    urls = []

    for x in games:
        urls.append({'url': "https://sportsbook-ca-on.draftkings.com/api/team/markets/dkcaon/v3/event/" + x + "?format=json",
                     'headers': {
                         'Accept': '*/*',
                         'Accept-Encoding': 'gzip, deflate, br',
                         'Referer': 'https://sportsbook.draftkings.com/',
                         'Sec-Fetch-Mode': 'cors',
                         'Sec-Fetch-Site': 'same-site',
                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                     }})
    return urls


def makeRequestLinksNEW(data):
    games = listGameIdsNEW(data)
    urls = []

    nflCategories = {'1000', '1001', '1003', '1342', '492'}
    mlbCategories = {'743', '1031', '493'}

    for x in games:
        if games[x] == '88808':
            for category in nflCategories:
                urls.append({'url': "https://sportsbook-nash.draftkings.com/api/sportscontent/dkcaon/v1/events/" + x + "/categories/" + category + "?appname=web",
                             'headers': {
                                 "accept": "*/*",
                                 "accept-encoding": "gzip, deflate, br, zstd",
                                 "accept-language": "en-US,en;q=0.9",
                                 "origin": "https://sportsbook.draftkings.com",
                                 "referer": "https://sportsbook.draftkings.com/",
                                 "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                                 "sec-ch-ua-mobile": "?1",
                                 "sec-ch-ua-platform": '"Android"',
                                 "sec-fetch-dest": "empty",
                                 "sec-fetch-mode": "cors",
                                 "sec-fetch-site": "same-site",
                                 "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
                                 "x-client-feature": "event-slider",
                                 "x-client-name": "web",
                                 "x-client-page": "event",
                                 "x-client-version": "2439.1.1.22"
                             }})
        elif games[x] == '84240':
            for category in mlbCategories:
                urls.append({'url': "https://sportsbook-nash.draftkings.com/api/sportscontent/dkcaon/v1/events/" + x + "/categories/" + category + "?appname=web",
                             'headers': {
                                 "accept": "*/*",
                                 "accept-encoding": "gzip, deflate, br, zstd",
                                 "accept-language": "en-US,en;q=0.9",
                                 "origin": "https://sportsbook.draftkings.com",
                                 "referer": "https://sportsbook.draftkings.com/",
                                 "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                                 "sec-ch-ua-mobile": "?1",
                                 "sec-ch-ua-platform": '"Android"',
                                 "sec-fetch-dest": "empty",
                                 "sec-fetch-mode": "cors",
                                 "sec-fetch-site": "same-site",
                                 "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
                                 "x-client-feature": "event-slider",
                                 "x-client-name": "web",
                                 "x-client-page": "event",
                                 "x-client-version": "2439.1.1.22"
                             }})
    return urls


def validAlternatePP(subcategoryName):
    return subcategoryName in ["Hits", "Home Runs", "Total Bases", "Strikeouts Thrown",
                               "RBIs", "Hits Allowed", "Walks Allowed"]


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

    for x in response:
        if x == None:
            continue
        data = x.json()
        homeTeam = data['event']['teamName2']
        awayTeam = data['event']['teamName1']
        homeAwayTeams = getTeamName(awayTeam) + \
            '(away)' + ' vs ' + getTeamName(homeTeam) + '(home)'
        currentLeague = (data['event']['eventGroupName'])

        # Game Props a.k.a. eventCategories index = 1
        eventCategory = next(
            (category for category in data['eventCategories'] if category['name'].lower() == 'game lines'), None)
        components = eventCategory['componentizedOffers']

        # The date is sometimes after midnight of the next day
        # this code makes sure it grabs the date of the start of the game
        datetimeStr = data['event']['startDate']
        dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%SZ")
        if dt.time() < datetime.strptime("05:30:00", "%H:%M:%S").time():
            dt -= timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")

        # components = data['eventCategories'][1]['componentizedOffers']
        for component in components:
            for offers in component['offers']:
                for offer in offers:
                    if 'label' not in offer:
                        continue
                    for outcome in offer['outcomes']:
                        league.append(currentLeague)
                        teams.append(homeAwayTeams)
                        categories.append(offer['label'])
                        if homeTeam in outcome['label']:
                            side.append('home')
                        elif awayTeam in outcome['label']:
                            side.append('away')
                        else:
                            side.append(None)
                        points.append(outcome.get('line', None))
                        pnt = outcome.get('line', None)
                        if offer['label'] == 'Run Line' and awayTeam in outcome['label']:
                            pnt = -1 * pnt
                        odds.append(outcome['oddsDecimal'])
                        americanOdds.append(outcome['oddsAmerican'])
                        names.append(None)
                        desi = outcome.get('label', None).lower()
                        if 'over' in desi or 'under' in desi:
                            designation.append(desi)
                        else:
                            designation.append(None)
                        keys.append(
                            makeKey(offer['label'], pnt, "Game"))
                        dates.append(date)

        # Player Props a.k.a. eventCategories index = 2 for batters and 3 for pitchers
        for category in data['eventCategories']:
            if category['name'] == 'Batter Props' or category['name'] == 'Pitcher Props':
                components = category['componentizedOffers']
                for component in components:
                    if component['componentId'] == 8:
                        for offer in component['offers'][0]:
                            for outcome in offer['outcomes']:
                                league.append(currentLeague)
                                teams.append(homeAwayTeams)
                                side.append(None)
                                designation.append(outcome['label'].lower())
                                points.append(outcome.get('line', None))
                                americanOdds.append(
                                    int(outcome['oddsAmerican'].strip('+')))
                                odds.append(
                                    float(outcome['oddsDecimalDisplay']))
                                categories.append(component['subcategoryName'])
                                playerName = outcome.get(
                                    'playerNameIdentifier', None)
                                if playerName is not None:
                                    nsplit = playerName.split()
                                    name = playerName.replace(
                                        nsplit[0], nsplit[0][0] + '.', 1)
                                    names.append(name)
                                else:
                                    names.append(None)
                                keys.append(
                                    makeKey(component['subcategoryName'], outcome.get('line', None), "Game"))
                                dates.append(date)
                    elif validAlternatePP(component['subcategoryName']):
                        for offer in component['offers'][0]:
                            for outcome in offer['outcomes']:
                                league.append(currentLeague)
                                teams.append(homeAwayTeams)
                                side.append(None)
                                designation.append('over')
                                points.append(
                                    float(outcome['label'].strip('+'))-0.5)
                                americanOdds.append(
                                    int(outcome['oddsAmerican'].strip('+')))
                                odds.append(
                                    float(outcome['oddsDecimalDisplay']))
                                categories.append(component['subcategoryName'])
                                playerName = outcome.get(
                                    'playerNameIdentifier', None)
                                if playerName is not None:
                                    nsplit = playerName.split()
                                    name = playerName.replace(
                                        nsplit[0], nsplit[0][0] + '.', 1)
                                    names.append(name)
                                else:
                                    names.append(None)
                                keys.append(makeKey(component['subcategoryName'], float(
                                    outcome['label'].strip('+'))-0.5, "Game"))
                                dates.append(date)

    print(len(teams), len(categories), len(league), len(designation), len(
        side), len(names), len(points), len(odds), len(americanOdds), len(keys))

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': categories, 'Designation': designation,
                       'Side': side, 'Name': names, 'Points': points, 'DK Decimal Odds': odds, 'DK American Odds': americanOdds, 'Key': keys, 'Date': dates})

    # This removes all rows where key is None
    df = df[np.logical_not(pd.isna(df['Key']))]

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/DraftKingsGigaDump.csv', index=False)


def gigaDump(responses):
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

    marketIds = dict()

    for response in responses:
        if response == None:
            continue
        data = response.json()
        if 'markets' not in data:
            continue
        for participant in data['events'][0]['participants']:
            if participant['venueRole'] == 'Home':
                homeTeam = getTeamName(participant['name'])
            elif participant['venueRole'] == 'Away':
                awayTeam = getTeamName(participant['name'])
        homeAwayTeams = getTeamName(awayTeam) + \
            '(away)' + ' vs ' + getTeamName(homeTeam) + '(home)'
        currentLeague = (data['leagues'][0]['name'])

        # The date is sometimes after midnight of the next day
        # this code makes sure it grabs the date of the start of the game
        datetimeStr = data['events'][0]['startEventDate'][:-2] + 'Z'
        dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S.%fZ")
        if dt.time() < datetime.strptime("05:30:00", "%H:%M:%S").time():
            dt -= timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")

        for market in data['markets']:
            if market['subcategoryId'] in relevantSubCategories:
                marketIds[market['id']] = market['marketType']['name']

        for selection in data['selections']:
            if selection['marketId'] not in marketIds:
                continue

            if selection['label'] in {'Under', 'Over'}:
                teams.append(homeAwayTeams)
                league.append(currentLeague)
                categories.append(marketIds[selection['marketId']])
                designation.append(selection['label'].lower())
                side.append(None)

                if 'participants' in selection:
                    name = selection['participants'][0]['name']
                    nsplit = name.split()
                    name = name.replace(
                        nsplit[0], nsplit[0][0] + '.', 1)
                    names.append(name)
                else:
                    names.append(None)

                point = selection['points']
                points.append(point)
                odds.append(selection['trueOdds'])
                americanOdds.append(fractional_to_american(
                    selection['displayOdds']['fractional']))
                keys.append(makeKey(marketIds[selection['marketId']], point))
                dates.append(date)

            elif selection['label'][-1] == '+':
                teams.append(homeAwayTeams)
                league.append(currentLeague)
                categories.append(marketIds[selection['marketId']])
                designation.append('over')
                side.append(None)

                name = selection['participants'][0]['name']
                nsplit = name.split()
                name = name.replace(
                    nsplit[0], nsplit[0][0] + '.', 1)
                names.append(name)

                point = int(selection['label'][:-1]) - 0.5
                points.append(point)
                odds.append(selection['trueOdds'])
                americanOdds.append(fractional_to_american(
                    selection['displayOdds']['fractional']))
                keys.append(makeKey(marketIds[selection['marketId']], point))
                dates.append(date)

            elif selection['outcomeType'] in {'Away', 'Home'}:
                teams.append(homeAwayTeams)
                league.append(currentLeague)
                categories.append(marketIds[selection['marketId']])
                designation.append(None)
                side.append(selection['outcomeType'].lower())
                names.append(None)
                point = selection.get('points', None)
                if point != None and selection['outcomeType'] == 'Away':
                    point = -1 * point
                points.append(point)
                odds.append(selection['trueOdds'])
                americanOdds.append(fractional_to_american(
                    selection['displayOdds']['fractional']))
                keys.append(makeKey(marketIds[selection['marketId']], point))
                dates.append(date)

            elif selection['outcomeType'] == 'ToScoreAnyTime' and 'participants' in selection:
                teams.append(homeAwayTeams)
                league.append(currentLeague)
                categories.append(marketIds[selection['marketId']])
                designation.append('over')
                side.append(None)

                name = selection['participants'][0]['name']
                nsplit = name.split()
                name = name.replace(
                    nsplit[0], nsplit[0][0] + '.', 1)
                names.append(name)

                point = 0.5
                points.append(point)
                odds.append(selection['trueOdds'])
                americanOdds.append(fractional_to_american(
                    selection['displayOdds']['fractional']))
                keys.append(makeKey(marketIds[selection['marketId']], point))
                dates.append(date)

    # print(set(categories))

    df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': categories, 'Designation': designation,
                       'Side': side, 'Name': names, 'Points': points, 'DK Decimal Odds': odds, 'DK American Odds': americanOdds, 'Key': keys, 'Date': dates})

    # This removes all rows where key is None
    # df = df[np.logical_not(pd.isna(df['Key']))]

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/DraftKingsGigaDump.csv', index=False)


class MyCmd(cmd.Cmd):
    prompt = '> '

    def __init__(self):  # initalize console with default values set to MLB
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
