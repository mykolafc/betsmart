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


def getDataMlb():
    # It's possible that some things in this link variable so it might not always be this EXACT link
    url = "https://guest.api.arcadia.pinnacle.com/0.1/sports/3/matchups?withSpecials=false&brandId=0"

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en-CA;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "origin": "https://www.pinnacle.com",
        "referer": "https://www.pinnacle.com/",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
        "x-device-uuid": "9fb7181d-89110321-9fcc237c-b457a792"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    return data


# For now this is only fetching MLB eventIds
def listGameIds(data):
    gameIds = []
    for game in data:
        # Id of mlb
        if game['league']['id'] == 246 and game['parentId'] != None:
            gameIds.append(game['id'])
    return gameIds


def decimal_to_american(decimal_odds):
    if decimal_odds == 1.0:
        american_odds = 0
    elif decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)


def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = (american_odds / 100) + 1
    else:
        decimal_odds = (100 / abs(american_odds)) + 1

    return decimal_odds


def americanToImpliedProb(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)


# Convert probabilities back to American odds

def impliedProbToAmerican(prob):
    if prob == 0:
        return None  # Handle zero probability edge case
    elif prob > 0.5:
        return -100 * prob / (1 - prob)
    else:
        return 100 * (1 - prob) / prob


def fairOdds(odds1, odds2):

    # Calculate implied probabilities
    prob1 = americanToImpliedProb(odds1)
    prob2 = americanToImpliedProb(odds2)

    # Normalize probabilities
    total_prob = prob1 + prob2
    no_vig_prob1 = prob1 / total_prob
    no_vig_prob2 = prob2 / total_prob

    no_vig_odds1 = impliedProbToAmerican(no_vig_prob1)
    no_vig_odds2 = impliedProbToAmerican(no_vig_prob2)

    return round(no_vig_odds1), round(no_vig_odds2)


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

        # THIS IS THE ONLY CURRENTLY ACCURATE KEY MAKER, THE REST IS FROM DRAFTKINGS
        # MLB switches
        'Total Strikeouts': f"pp;0;ou;so;{points}",
        "Home Runs": f"pp;0;ou;hr;{points}",
        "Earned Runs": f"pp;0;ou;er;{points}",
        "Total Bases": f"pp;0;ou;tb;{points}",
        "Hits Allowed": f"pp;0;ou;hita;{points}",
        # Idk wtf this is below
        "Pitching Outs": f'pp;ou;po;{points}',

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
    gameIds = listGameIds(data)
    nameUrls = []
    oddsUrls = []

    for gameId in gameIds:
        nameUrl = f"https://guest.api.arcadia.pinnacle.com/0.1/matchups/{gameId}/related"
        oddsUrl = f"https://guest.api.arcadia.pinnacle.com/0.1/matchups/{gameId}/markets/related/straight"

        nameUrls.append({'url': nameUrl, 'headers': {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en-CA;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.pinnacle.com",
            "referer": "https://www.pinnacle.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
            "x-device-uuid": "9fb7181d-89110321-9fcc237c-b457a792"
        }})
        oddsUrls.append({'url': oddsUrl, 'headers': {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en-CA;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.pinnacle.com",
            "referer": "https://www.pinnacle.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
            "x-device-uuid": "9fb7181d-89110321-9fcc237c-b457a792"
        }})
    return nameUrls, oddsUrls


# For Game props
def validMarketTypeGame(item):
    if item['type'] in ['moneyline', 'team_total', "spread", "total"] and item['period'] == 0 and 'designation' in item['prices'][0]:
        return True
    else:
        return False


def gigaDump2(respNameData, respOddsData):
    leagues = []
    teams = []
    points = []
    odds = []
    americanOdds = []
    noVigOdds = []
    side = []
    categories = []
    names = []
    designation = []
    keys = []
    dates = []

    for nameData, oddsData in zip(respNameData, respOddsData):
        nameData = nameData.json()
        oddsData = oddsData.json()
        matchupIds = dict()
        league = nameData[0]['league']['name']
        awayHomeTeams = getTeamName(nameData[0]['participants'][1]['name']) + \
            '(away) vs ' + \
            getTeamName(nameData[0]['participants'][0]['name']) + '(home)'

        for bet in nameData:
            if bet.get('special') and bet['special'].get('category') == 'Player Props':
                for participant in bet['participants']:
                    if participant['name'] == 'Over':
                        overId = participant['id']
                    elif participant['name'] == 'Under':
                        underId = participant['id']
                matchupIds[bet['id']] = {'description': bet['special']['description'],
                                         overId: 'over',
                                         underId: 'under'}

        # filtered_data = [item for item in oddsData if item.get(
        #     'matchupId') in matchupIds]

        for item in oddsData:
            # Getting the date of the game
            # this code makes sure it grabs the date of the start of the game
            datetimeStr = item['cutoffAt']
            # Try parsing with the first format
            try:
                dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                # If it fails, try the second format
                dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S.%f%z")
            if dt.time() < datetime.strptime("05:30:00", "%H:%M:%S").time():
                dt -= timedelta(days=1)
            date = dt.strftime("%Y-%m-%d")

            # This is for player props
            if item.get('matchupId') in matchupIds:
                # Getting the fair odds right off the bat
                fairOverOdd, fairUnderOdd = fairOdds(
                    item['prices'][0]['price'], item['prices'][1]['price'])
                # Getting the player name
                playerName = re.search(
                    r'^(.*?)\s*\(', matchupIds[item['matchupId']]['description']).group(1).strip()
                nsplit = playerName.split()
                name = playerName.replace(nsplit[0], nsplit[0][0] + '.', 1)

                # Over
                leagues.append(league)
                teams.append(awayHomeTeams)
                categories.append(
                    re.search(r'\(([^)]+)\)', matchupIds[item['matchupId']]['description']).group(1))
                names.append(name)
                side.append(None)
                designation.append(
                    matchupIds[item['matchupId']][item['prices'][0]['participantId']])
                points.append(item['prices'][0]['points'])
                dates.append(date)
                # This searches for whats inside the first parantheses (which is the category we're looking for)
                keys.append(
                    makeKey(re.search(r'\(([^)]+)\)', matchupIds[item['matchupId']]['description']).group(1), item['prices'][0]['points']))
                americanOdds.append(item['prices'][0]['price'])
                odds.append(american_to_decimal(item['prices'][0]['price']))
                noVigOdds.append(fairOverOdd)

                # Under
                leagues.append(league)
                teams.append(awayHomeTeams)
                categories.append(
                    re.search(r'\(([^)]+)\)', matchupIds[item['matchupId']]['description']).group(1))
                names.append(name)
                side.append(None)
                designation.append(
                    matchupIds[item['matchupId']][item['prices'][1]['participantId']])
                dates.append(date)
                keys.append(
                    makeKey(re.search(r'\(([^)]+)\)', matchupIds[item['matchupId']]['description']).group(1), item['prices'][1]['points']))
                points.append(item['prices'][1]['points'])
                americanOdds.append(item['prices'][1]['price'])
                odds.append(american_to_decimal(item['prices'][1]['price']))
                noVigOdds.append(fairUnderOdd)

            elif validMarketTypeGame(item):
                # this repeats twice cuz it needs to be done for both side, whether over/under or home/away
                fairFirstOdd, fairSecondOdd = fairOdds(
                    item['prices'][0]['price'], item['prices'][1]['price'])

                leagues.append(league)
                teams.append(awayHomeTeams)
                categories.append(item['type'])
                names.append(None)
                if 'side' in item or item['prices'][0]['designation'] in ['over', 'under']:
                    side.append(item.get('side', None))
                    designation.append(item['prices'][0]['designation'])
                else:
                    side.append(item['prices'][0]['designation'])
                    designation.append(None)
                dates.append(date)
                keys.append(item['key'])
                points.append(item['prices'][0].get('points', None))
                americanOdds.append(item['prices'][0]['price'])
                odds.append(american_to_decimal(item['prices'][0]['price']))
                noVigOdds.append(fairFirstOdd)

                leagues.append(league)
                teams.append(awayHomeTeams)
                categories.append(item['type'])
                names.append(None)
                if 'side' in item or item['prices'][1]['designation'] in ['over', 'under']:
                    side.append(item.get('side', None))
                    designation.append(item['prices'][1]['designation'])
                else:
                    side.append(item['prices'][1]['designation'])
                    designation.append(None)
                dates.append(date)
                keys.append(item['key'])
                points.append(item['prices'][1].get('points', None))
                americanOdds.append(item['prices'][1]['price'])
                odds.append(american_to_decimal(item['prices'][1]['price']))
                noVigOdds.append(fairSecondOdd)

    df = pd.DataFrame({'Key': keys, 'Date': dates, 'League': leagues, 'Teams': teams, 'Name': names, 'Category': categories, 'Side': side, 'Designation': designation,
                       'Points': points, 'PN American Odds': americanOdds, 'PN Decimal Odds': odds, 'PN Fair Odds': noVigOdds})

    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    df.to_csv(str(dir) + '/bin/PinnacleGigaDump.csv', index=False)


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
