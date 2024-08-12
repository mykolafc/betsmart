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


# For now this is only fetching MLB eventIds
def listGameIds(data):
    gameIds = []
    for event in data['attachments']['events'].values():
        # This number is the number representing that its an mlb game
        if event['competitionId'] == 11196870:
            gameIds.append(event['eventId'])
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
        "TO_RECORD_2+_TOTAL_BASES": f"pp;0;ss;tb;1.5",
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
    switcherMLB = {
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
    }

    return switcherMLB.get(name, name)


def getLeague(competitionId):
    switcher = {
        11196870: "MLB",
        # Add other leagues in the future
    }

    return switcher.get(competitionId, 'Unknown competitionId')


# This function is going to make the request links useful for FanDuel
def makeRequestLinks(data):
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
    return urls


# For Game props
def validMarketTypeGame(marketType):
    if marketType in ['MONEY_LINE', 'MATCH_HANDICAP_(2-WAY)', "ALTERNATE_TOTAL_RUNS", "TOTAL_POINTS_(OVER/UNDER)",
                      "AWAY_TOTAL_RUNS", "HOME_TOTAL_RUNS", "AWAY_TEAM_ALTERNATE_TOTAL_RUNS", "HOME_TEAM_ALTERNATE_TOTAL_RUNS"]:
        return True
    else:
        return False


# For Over/Under
def validMarketTypeOUPP(marketType):
    if bool(re.match(r'^PITCHER_\w_TOTAL_STRIKEOUTS$', marketType)):
        return True
    else:
        return False


# For Atleasts
def validMarketTypeAlternatePP(marketType):
    if marketType in ["TO_HIT_A_HOME_RUN", "PLAYER_TO_RECORD_A_HIT", "PLAYER_TO_RECORD_2+_HITS", "PLAYER_TO_RECORD_3+_HITS", "TO_RECORD_A_STOLEN_BASE", "TO_RECORD_A_RUN",
                      "TO_RECORD_2+_RUNS", "TO_RECORD_3+_RUNS", "TO_RECORD_AN_RBI", "TO_RECORD_2+_RBIS", "TO_RECORD_2+_TOTAL_BASES", "TO_RECORD_3+_TOTAL_BASES",
                      "TO_RECORD_4+_TOTAL_BASES", "TO_RECORD_5+_TOTAL_BASES", "TO_HIT_A_SINGLE", "TO_HIT_A_DOUBLE", "TO_HIT_A_TRIPLE"]:
        return True
    elif bool(re.match(r'^PITCHER_\w_STRIKEOUTS$', marketType)):
        return True
    else:
        return False


def gigaDump2(respNameData, respOddsData):
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

    for nameData, oddsData in zip(respNameData, respOddsData):
        nameData = nameData.json()
        oddsData = oddsData.json()
        matchupIds = dict()
        for bet in nameData:
            if bet.get('special') and bet['special'].get('category') == 'Player Props':
                matchupIds[bet['id']] = bet['special']['description']

        # filtered_data = [item for item in oddsData if item.get(
        #     'matchupId') in matchupIds]

        for item in oddsData:
            if item.get('matchupId') in matchupIds:
                # Over
                categories.append(matchupIds[item['matchupId']])
                designation.append('over')
                points.append(item['prices'][0]['points'])
                odds.append(item['prices'][0]['price'])
                # Under
                categories.append(matchupIds[item['matchupId']])
                designation.append('under')
                points.append(item['prices'][1]['points'])
                odds.append(item['prices'][1]['price'])

    df = pd.DataFrame({'Category': categories, 'Designation': designation,
                       'Points': points, 'PN American Odds': odds})

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/PinnacleTestDump.csv', index=False)

    # df = pd.DataFrame({'Teams': teams, 'League': league, 'Category': categories, 'Designation': designation,
    #                    'Side': side, 'Name': names, 'Points': points, 'FD Decimal Odds': odds, 'FD American Odds': americanOdds, 'Key': keys, 'Date': dates})

    # dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    # df.to_csv(str(dir) + '/bin/FanDuelGigaDump.csv', index=False)


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
