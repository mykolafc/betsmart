# For some reason importing grequests as one of the last imports causes an error but doing it first doesn't
import grequests
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
import time
import asyncio
import aiohttp
import concurrent.futures
import requests
import re
import json
import numpy as np


###########################################################################################################
# RESPONSE REQUESTS
###########################################################################################################

# Doing Grequests for post requests since for some reason Asyncio seems to not work with payloads
def fetchGrequests(url, headers, payloads):
    start = time.time()
    unsentRequests = [grequests.post(
        url, headers=headers, json=payload) for payload in payloads]
    responses = grequests.map(unsentRequests)
    jsonResponses = [response.json() for response in responses]
    end = time.time()
    print(f'G Requests took {(end-start)} seconds')
    return jsonResponses


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


# AsycnIO request for list of urls
async def propsJsonAsyncio(urls):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url))
        respA = await asyncio.gather(*tasks)
    end = time.time()
    print(f'Asyncio requests for props takes {(end-start)} seconds')
    # Here I do [1:-1] because the each props response is surrounded by [] and that removes it
    # Also making sure that json returned data
    data = [json.loads(item[1:-1]) for item in respA if item != '[]']
    return data
# Find a way to do this with grequests to make sure asyncio is faster


# Threading both async requests so it can be best for time efficiency
def threadedRequests(payloads, urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        grequestsFuture = executor.submit(
            fetchGrequests, byEventUrl, byEventHeaders, payloads)
        asyncioFuture = executor.submit(asyncio.run, propsJsonAsyncio(urls))

        grequestsResult = grequestsFuture.result()
        asyncioResult = asyncioFuture.result()

    return grequestsResult, asyncioResult


###########################################################################################################
# Getting the original GameIds ands prop gameIds
###########################################################################################################

def isNotLive(wagerCutOff):
    target_time = datetime.strptime(wagerCutOff, "%Y-%m-%dT%H:%M:%S")
    threshold_time = target_time - timedelta(minutes=1)
    current_time = datetime.now()
    # Check if the current time is before the threshold
    return current_time < threshold_time

# Gets the gameIds for team odds as well as the gameIds by league


def getGeneralGameIDs(days=2):

    now = datetime.utcnow()
    headers = {
        'authority': 'api-offering.betonline.ag',
        'method': 'POST',
        'path': '/api/offering/sports/offering-by-default',
        'scheme': 'https',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Origin': 'https://api-offering.betonline.ag/api/offering/sports/offering-by-default',
        # Current time in milliseconds since the epoch,
        'Actual-Time': str(int(time.time() * 1000)),
        'Content-Length': '0',
        'Content-Type': 'application/json',
        'Contests': 'na',
        'Gmt-Offset': '-4',
        'Gsetting': 'bolnasite',
        'Iso-Time': now.isoformat() + 'Z',  # Current time in ISO 8601 format
        'Origin': 'https://www.betonline.ag',
        'Referer': 'https://www.betonline.ag/',
        'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Utc-Offset': '240',
        'Utc-Time': now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    }

    url = "https://api-offering.betonline.ag/api/offering/sports/offering-by-league"
    # soccer down below
    # url = "https://api-offering.betonline.ag/api/offering/sports/offering-by-scheduletext"

    # This changes based on the sport you're looking at ex: football can go in "Sport" and nlf in "League"
    requestPayloadFootball = {"Sport": "football", "League": "nfl",
                              "ScheduleText": None, "Period": -1}
    requestPayloadHockey = {"Sport": "hockey", "League": "nhl",
                            "ScheduleText": None, "Period": -1}
    requestPayloadBasket = {"Sport": "basketball", "League": "nba",
                            "ScheduleText": None, "Period": -1}
    requestPayloadBaseball = {"Sport": "baseball", "League": "mlb",
                              "ScheduleText": None, "Period": -1}
    # Soccer is different but below is the one for the premier league
    # requestPayload = {"Sport": "soccer", "League": "epl", "ScheduleText": "english-premier-league", "Period": -1}
    payloads = [requestPayloadFootball,
                requestPayloadBasket, requestPayloadHockey, requestPayloadBaseball]
    start = time.time()
    unsentRequests = [grequests.post(
        url, headers=headers, json=payload) for payload in payloads]
    responses = grequests.map(unsentRequests)
    data = [response.json() for response in responses]
    end = time.time()
    print(f'Grequesting by-league takes {(end-start)} seconds')
    # print(response)

    # Getting only the information of the games which is nested in the previous JSON file
    # gamesData = []
    # for gamesByLeague in data:
    #     gamesData += gamesByLeague['GameOffering']['GamesDescription']

    gameIdsByLeague = dict()
    game_Ids = []
    for gamesByLeague in data:
        gameOffering = gamesByLeague.get('GameOffering')
        if gameOffering is None:
            continue
        league = gamesByLeague['GameOffering']['League']
        gamesData = gamesByLeague['GameOffering']['GamesDescription']
        game_IdsByLeague = []
        now = datetime.now()
        for game in gamesData:
            gameDate = datetime.strptime(game['GameDate'], '%m/%d/%Y')
            if abs((now - gameDate).days) <= days:
                game_Id = game['Game']['GameId']
                game_IdsByLeague.append(game_Id)

                if isNotLive(game['Game']['WagerCutOff']):
                    game_Ids.append(game_Id)
        gameIdsByLeague[league] = game_IdsByLeague

    return game_Ids, gameIdsByLeague

    # game_Ids = []
    # now = datetime.now()
    # for game in gamesData:
    #     gameDate = datetime.strptime(game['GameDate'], '%m/%d/%Y')
    #     if abs((now - gameDate).days) <= days:
    #         game_Ids.append(game['Game']['GameId'])
    # return game_Ids


# Gets the gameIds for player prop odds with Asyncio
async def getAsyncPropsIDs(game_Ids):
    links = []
    for game_Id in game_Ids:
        links.append(
            "https://bv2-us.digitalsportstech.com/api/game?sb=betonline&event="+str(game_Id))
    gameIds = []
    gamesDict = {}
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in links:
            tasks.append(fetch(session, url))
        response = await asyncio.gather(*tasks)
    print(f'Getting the gameIds took {(time.time() - start)} seconds')
    for r in response:
        # Here is where you can find the game props ID inside of the json file, we're appending it to the dictionary
        # Makes sure json returned something
        if r != '[]':
            jr = json.loads(r)
            gameId = jr[0]['providers'][0]['id']
            gameIds.append(gameId)

            # The wager cut off is sometimes after midnight of the next day
            # this code makes sure it grabs the date of the start of the game
            datetimeStr = jr[0]['date']
            dt = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S.%fZ")
            if dt.time() < datetime.strptime("05:30:00", "%H:%M:%S").time():
                dt -= timedelta(days=1)
            date = dt.strftime("%Y-%m-%d")

            # This checks if two teams play each other in the same day multiple times
            game = jr[0].get('mlbDoubleHeader', '')
            if game:
                game = game[-1]

            gamesDict[str(gameId)] = [getTeamAbr(jr[0]['team2']['title']) +
                                      '(away) vs ' + getTeamAbr(jr[0]['team1']['title']) + '(home)' + game, jr[0]['league'].upper(), date]
            # gamesDict['date'] = jr[0]['date'][:10]
    return gameIds, gamesDict


###########################################################################################################
# MONEY LINE AND TEAM BETS FROM SPECIFIC GAMES
###########################################################################################################

# Headers for by Event
currentTime = datetime.utcnow()
byEventHeaders = {
    "authority": "api-offering.betonline.ag",
    "method": "POST",
    "path": "/api/offering/sports/get-event",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, POST",
    "Access-Control-Allow-Origin": "https://api-offering.betonline.ag/api/offering/sports/get-event",
    "Actual-Time": str(int(time.time() * 1000)),
    "Content-Length": "74",
    "Content-Type": "application/json",
    "Contests": "na",
    "Gmt-Offset": "-5",
    "Gsetting": "bolnasite",
    "Iso-Time": currentTime.isoformat() + 'Z',
    "Origin": "https://www.betonline.ag",
    "Referer": "https://www.betonline.ag/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Utc-Offset": "300",
    "Utc-Time": currentTime.strftime('%a, %d %b %Y %H:%M:%S GMT')
}

# Url for the by Event
byEventUrl = "https://api-offering.betonline.ag/api/offering/sports/get-event"


# Making the payloads for the events
def makePayloads(gameIdsBySport):
    nflGameIds = gameIdsBySport.get('NFL')
    nflPayloads = []
    if nflGameIds != None:
        for game_Id in nflGameIds:
            nflPayloads.append({
                "GameID": game_Id,
                "Sport": "football",
                "League": "nfl",
                "ScheduleText": None
            })
    nbaGameIds = gameIdsBySport.get('NBA')
    nbaPayloads = []
    if nbaGameIds != None:
        for game_Id in nbaGameIds:
            nbaPayloads.append({
                "GameID": game_Id,
                "Sport": "basketball",
                "League": "nba",
                "ScheduleText": None
            })
    nhlGameIds = gameIdsBySport.get('NHL')
    nhlPayloads = []
    if nhlGameIds != None:
        for game_Id in nhlGameIds:
            nhlPayloads.append({
                "GameID": game_Id,
                "Sport": "hockey",
                "League": "nhl",
                "ScheduleText": None
            })
    # BASEBALL
    mlbGameIds = gameIdsBySport.get('MLB')
    mlbPayloads = []
    if mlbGameIds != None:
        for game_Id in mlbGameIds:
            mlbPayloads.append({
                "GameID": game_Id,
                "Sport": "baseball",
                "League": "mlb",
                "ScheduleText": None
            })
    payloads = nflPayloads + nbaPayloads + nhlPayloads + mlbPayloads
    return payloads


def makeGameUrls(gameIdsBySport):
    nflGameIds = gameIdsBySport.get('NFL')
    urls = []
    if nflGameIds != None:
        for game_Id in nflGameIds:
            urls.append({'url': byEventUrl,
                         'headers': byEventHeaders,
                        'payload': {
                            "GameID": game_Id,
                            "Sport": "football",
                            "League": "nfl",
                            "ScheduleText": None
                        }
            })
    nbaGameIds = gameIdsBySport.get('NBA')
    if nbaGameIds != None:
        for game_Id in nbaGameIds:
            urls.append({'url': byEventUrl,
                         'headers': byEventHeaders,
                        'payload': {
                            "GameID": game_Id,
                            "Sport": "basketball",
                            "League": "nba",
                            "ScheduleText": None
                        }
            })
    nhlGameIds = gameIdsBySport.get('NHL')
    if nhlGameIds != None:
        for game_Id in nhlGameIds:
            urls.append({'url': byEventUrl,
                         'headers': byEventHeaders,
                        'payload': {
                            "GameID": game_Id,
                            "Sport": "hockey",
                            "League": "nhl",
                            "ScheduleText": None
                        }
            })
    # BASEBALL
    mlbGameIds = gameIdsBySport.get('MLB')
    if mlbGameIds != None:
        for game_Id in mlbGameIds:
            urls.append({'url': byEventUrl,
                         'headers': byEventHeaders,
                        'payload': {
                            "GameID": game_Id,
                            "Sport": "baseball",
                            "League": "mlb",
                            "ScheduleText": None
                        }
            })
    return urls


# Loop that manipulates the teams odds data and returns in df, for some reason its much faster than using pandas
def manipulationLoop(data):
    start = time.perf_counter()
    # Columns
    name = []
    gameId = []
    teams = []
    league = []
    designation = []
    side = []
    point = []
    keys = []
    odds = []
    dec_odds = []
    category = []
    dates = []

    periodEvents = []
    for game in data:
        if game == None:
            continue
        periodEvents = periodEvents + game['EventOffering']['PeriodEvents']
    for event in periodEvents:
        game_Id = event['Event']['GameId']

        # This checks if two teams play each other in the same day multiple times
        if re.search(r' - Game #\d+', event['Event']['AwayTeam']):
            awayTeam = re.sub(r' - Game #\d+.*', '',
                              event['Event']['AwayTeam']).lower()
            homeTeam = re.sub(r' - Game #\d+.*', '',
                              event['Event']['HomeTeam']).lower()
            teams1 = getTeamAbr(awayTeam) + '(away) vs ' + getTeamAbr(
                homeTeam) + '(home)' + event['Event']['AwayTeam'][-1]
        else:
            teams1 = getTeamAbr(event['Event']['AwayTeam'].lower()) + '(away) vs ' + \
                getTeamAbr(event['Event']['HomeTeam'].lower()) + '(home)'
        league1 = event['Event']['CorrelationId'].split('-')[1].split(' ')[0]
        name1 = event['Name']
        date = event['Event']['WagerCutOff'][:10]

        # Away
        # SpreadLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('spread')
        point.append(event['Event']['AwayLine']['SpreadLine']['Point'])
        keys.append(
            makeKey('spread', event['Event']['AwayLine']['SpreadLine']['Point'] * -1, name=name1))
        designation.append(None)
        odds.append(event['Event']['AwayLine']['SpreadLine']['Line'])
        dec_odds.append(americanToDecimal(
            event['Event']['AwayLine']['SpreadLine']['Line']))
        name.append(name1)
        dates.append(date)
        # MoneyLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('moneyline')
        point.append(None)
        keys.append(makeKey('moneyline', 0, name=name1))
        designation.append(None)
        odds.append(event['Event']['AwayLine']['MoneyLine']['Line'])
        dec_odds.append(americanToDecimal(
            event['Event']['AwayLine']['MoneyLine']['Line']))
        name.append(name1)
        dates.append(date)
        # TeamTotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('team_total')
        point.append(event['Event']['AwayLine']['TeamTotalLine']['Point'])
        keys.append(
            makeKey('team_totalaway', event['Event']['AwayLine']['TeamTotalLine']['Point'], name=name1))
        designation.append('over')
        odds.append(event['Event']['AwayLine']
                    ['TeamTotalLine']['Over']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['AwayLine']
                        ['TeamTotalLine']['Over']['Line']))
        name.append(name1)
        dates.append(date)
        # TeamTotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('team_total')
        point.append(event['Event']['AwayLine']['TeamTotalLine']['Point'])
        keys.append(
            makeKey('team_totalaway', event['Event']['AwayLine']['TeamTotalLine']['Point'], name=name1))
        designation.append('under')
        odds.append(event['Event']['AwayLine']
                    ['TeamTotalLine']['Under']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['AwayLine']
                        ['TeamTotalLine']['Under']['Line']))
        name.append(name1)
        dates.append(date)
        # Home
        # SpreadLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('spread')
        point.append(event['Event']['HomeLine']['SpreadLine']['Point'])
        keys.append(
            makeKey('spread', event['Event']['HomeLine']['SpreadLine']['Point'], name=name1))
        designation.append(None)
        odds.append(event['Event']['HomeLine']['SpreadLine']['Line'])
        dec_odds.append(americanToDecimal(
            event['Event']['HomeLine']['SpreadLine']['Line']))
        name.append(name1)
        dates.append(date)
        # MoneyLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('moneyline')
        point.append(None)
        keys.append(makeKey('moneyline', 0, name=name1))
        designation.append(None)
        odds.append(event['Event']['HomeLine']['MoneyLine']['Line'])
        dec_odds.append(americanToDecimal(
            event['Event']['HomeLine']['MoneyLine']['Line']))
        name.append(name1)
        dates.append(date)
        # TeamTotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('team_total')
        point.append(event['Event']['HomeLine']['TeamTotalLine']['Point'])
        keys.append(makeKey('team_totalhome',
                    event['Event']['HomeLine']['TeamTotalLine']['Point'], name=name1))
        designation.append('over')
        odds.append(event['Event']['HomeLine']
                    ['TeamTotalLine']['Over']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['HomeLine']
                        ['TeamTotalLine']['Over']['Line']))
        name.append(name1)
        dates.append(date)
        # TeamTotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('team_total')
        point.append(event['Event']['HomeLine']['TeamTotalLine']['Point'])
        keys.append(makeKey('team_totalhome',
                    event['Event']['HomeLine']['TeamTotalLine']['Point'], name=name1))
        designation.append('under')
        odds.append(event['Event']['HomeLine']
                    ['TeamTotalLine']['Under']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['HomeLine']
                        ['TeamTotalLine']['Under']['Line']))
        name.append(name1)
        dates.append(date)
        # TotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append(None)
        category.append('total')
        point.append(event['Event']['TotalLine']['TotalLine']['Point'])
        keys.append(
            makeKey('total', event['Event']['TotalLine']['TotalLine']['Point'], name=name1))
        designation.append('over')
        odds.append(event['Event']['TotalLine']['TotalLine']['Over']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['TotalLine']
                        ['TotalLine']['Over']['Line']))
        name.append(name1)
        dates.append(date)
        # TotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append(None)
        category.append('total')
        point.append(event['Event']['TotalLine']['TotalLine']['Point'])
        keys.append(
            makeKey('total', event['Event']['TotalLine']['TotalLine']['Point'], name=name1))
        designation.append('under')
        odds.append(event['Event']['TotalLine']['TotalLine']['Under']['Line'])
        dec_odds.append(americanToDecimal(event['Event']['TotalLine']
                        ['TotalLine']['Under']['Line']))
        name.append(name1)
        dates.append(date)

    finalData = {'Period': name, 'GameId': gameId, 'Teams': teams, 'League': league, 'Designation': designation,
                 'Side': side, 'Points': point, 'Key': keys, 'BO Odds': odds, 'BO dec_odds': dec_odds, 'Category': category, 'Date': dates}
    df = pd.DataFrame(finalData)
    df = df[df['BO Odds'] != 0]
    end = time.perf_counter()
    totaltime = end - start
    print(
        f'Loop manipulation took {totaltime} seconds')
    # df.to_csv('3SportsDataManipulationLoop.csv', index=False)
    return df

###########################################################################################################
# CODE FOR GAME PROPS
###########################################################################################################


# Categories to make the links later on
categoriesOUFootball = ["Carries", "Pass%2520Attempts", "Pass%2520Completions", "Interceptions", "Pass%2520Interceptions",
                        "Passing%2520TDs", "Passing%2520Yards", "Receiving%2520Yards", "Receptions", "Rushing%2520Yards", "Sacks"]
categoriesAtleastFootball = ["Carries", "Pass%2520Attempts", "Pass%2520Completions", "Pass%2520Interceptions",
                             "Passing%2520TDs", "Passing%2520Yards", "Receiving%2520Yards", "Receptions", "Rushing%2520Yards", "Sacks", "Touchdowns"]
categoriesOUHockey = ["Points", "Saves", "Shots%2520on%2520goal"]
categoriesAtleastHockey = ["Assists", "Goals",
                           "Points", "Saves", "Shots%2520on%2520goal"]
categoriesOUBasket = ['Assists', 'Points', 'Pts%2520%252B%2520Reb%2520%252B%2520Ast',
                      'Three%2520Point%2520Field%2520Goals%2520Made', 'Total%2520Rebounds']
categoriesAtleastBasket = ['Assists', 'Blocked%2520Shots', 'Points', 'Pts%2520%252B%2520Reb%2520%252B%2520Ast',
                           'Reb%2520%252B%2520Ast', 'Steals', 'hree%2520Point%2520Field%2520Goals%2520Made', 'Total%2520Rebounds']
# BASEBALL
# This is a lot of requests for the site to take so it often crashes at this point, maybe change shit up
categoriesOUBaseball = ['Earned%2520runs', 'Hits', 'Hits%2520Allowed', 'Runs%2520%252B%2520RBIs',
                        'Stolen%2520bases', 'Strikeouts', 'Total%2520bases']
categoriesAtleastBaseball = ['Earned%2520runs', 'Hits', 'Hits%2520Allowed', 'Home%2520runs', 'Runs%2520%252B%2520RBIs',
                             'Stolen%2520bases', 'Strikeouts']


# For list of gameIds
def overUnderLinks(gameIds, catagories):
    # When using dictionary.get(key) if the key doesn't exist it will return None
    # gameIds will return None if the league we're trying to get isn't there
    if gameIds == None:
        return []
    # Function to make a list of Urls that lead to json files filed with the stats
    links = ["https://bv2.digitalsportstech.com/api/dfm/marketsByOu?sb=betonline&gameId=" +
             str(gameId)+"&statistic="+catagory for gameId in gameIds for catagory in catagories]
    return links


# For list of gameIds
def atleastLinks(gameIds, catagories):
    if gameIds == None:
        return []
    # Function to make a list of Urls that lead to json files filed with the stats
    links = ["https://bv2.digitalsportstech.com/api/dfm/marketsBySs?sb=betonline&gameId=" +
             str(gameId)+"&statistic="+catagory for gameId in gameIds for catagory in catagories]
    return links


def getPropsUrls(gamesDict):
    gameIdsBySport = dict()
    for gameId, league in gamesDict.items():
        gameIdsBySport.setdefault(league[1], []).append(gameId)
    # IS THIS SHIT GONNA WORK????
    urls = overUnderLinks(gameIdsBySport.get('NFL'), categoriesOUFootball) + \
        atleastLinks(gameIdsBySport.get('NFL'), categoriesAtleastFootball) + \
        overUnderLinks(gameIdsBySport.get('NBA'), categoriesOUBasket) + \
        atleastLinks(gameIdsBySport.get('NBA'), categoriesAtleastBasket) + \
        overUnderLinks(gameIdsBySport.get('NHL'), categoriesOUHockey) + \
        atleastLinks(gameIdsBySport.get('NHL'), categoriesAtleastHockey) + \
        overUnderLinks(gameIdsBySport.get('MLB'), categoriesOUBaseball) + \
        atleastLinks(gameIdsBySport.get('MLB'), categoriesAtleastBaseball)
    return urls


def getPropsUrls2(gamesDict):
    gameIdsBySport = dict()
    for gameId, league in gamesDict.items():
        gameIdsBySport.setdefault(league[1], []).append(gameId)
    urlsDict = []
    # IS THIS SHIT GONNA WORK????
    urls = overUnderLinks(gameIdsBySport.get('NFL'), categoriesOUFootball) + \
        atleastLinks(gameIdsBySport.get('NFL'), categoriesAtleastFootball) + \
        overUnderLinks(gameIdsBySport.get('NBA'), categoriesOUBasket) + \
        atleastLinks(gameIdsBySport.get('NBA'), categoriesAtleastBasket) + \
        overUnderLinks(gameIdsBySport.get('NHL'), categoriesOUHockey) + \
        atleastLinks(gameIdsBySport.get('NHL'), categoriesAtleastHockey) + \
        overUnderLinks(gameIdsBySport.get('MLB'), categoriesOUBaseball) + \
        atleastLinks(gameIdsBySport.get('MLB'), categoriesAtleastBaseball)

    for url in urls:
        urlsDict.append({'url': url,
                         'headers': None})
    return urlsDict


def decToAmerican(odd):
    if odd == 1:
        return 0
    if odd >= 2.0:
        odd = 100*(odd - 1)
    else:
        odd = (-100)/(odd - 1)
    return round(odd)


def makeKey(unit, points, name=None):
    period = -1
    if name == 'Game':
        period = 0
    switcher = {
        "Assists": f"pp;0;ou;asst;{points}",
        "Points": f"pp;0;ou;pts;{points}",
        "Three Point Field Goals Made": f"pp;0;ou;3pt;{points}",
        "Total Rebounds": f"pp;0;ou;reb;{points}",
        "Pts + Reb + Ast": f"pp;0;ou;pra;{points}",
        "Player To Record A Double Double": f"pp;0;ou;dbldbl;{points}",
        "Player To Record A Triple Double": f"pp;0;ou;trpldbl;{points}",

        "Shots on goal": f"pp;0;ou;sog;{points}",
        "Saves": f"pp;0;ou;saves;{points}",
        "Goals": f"pp;0;ou;goals;{points}",

        "Hits": f"pp;0;ou;hit;{points}",
        "Stolen bases": f"pp;0;ou;sb;{points}",
        "Strikeouts": f"pp;0;ou;so;{points}",
        "Total bases": f"pp;0;ou;tb;{points}",
        "Earned runs": f"pp;0;ou;er;{points}",
        "Hits Allowed": f"pp;0;ou;hita;{points}",
        "Runs + RBIs": f"pp;0;ou;r+r;{points}",

        # Nfl
        'Alternate Touchdowns': f'pp;0;ou;td;{points}',
        'Interceptions': f'pp;0;ou;int;{points}',
        'Passing Yards': f'pp;0;ou;pay;{points}',
        'Receiving Yards': f'pp;0;ou;rey;{points}',
        'Rushing Yards': f'pp;0;ou;ruy;{points}',
        'Quarterback Passing Touchdowns': f'pp;0;ou;tdp;{points}',
        'Pass Attempts': f'pp;0;ou;pat;{points}',
        'Pass Completions': f'pp;0;ou;com;{points}',
        'Rushing Attempts Over/Under': f'pp;0;ou;rut;{points}',
        'Receptions': f'pp;0;ou;rec;{points}',
        'Quarterback To Get': f"pp;0;ss;tdp;{points}",
        'Receiver To Get': f"pp;0;ss;rey;{points}",
        'Running Back To Get': f"pp;0;ss;ruy;{points}",
        'Alternate Pass Attempts': f"pp;0;ss;pat;{points}",
        'Alternate Pass Completions': f'pp;0;ss;com;{points}',
        'Alternate Passing TDs': f"pp;0;ss;tdp;{points}",
        'Alternate Rush Attempts': f'pp;0;ss;rut;{points}',
        'Alternate Receptions': f'pp;0;ss;rec;{points}',

        "moneyline": f"s;{period};m",
        "spread": f"s;{period};s;{points}",
        "total": f"s;{period};ou;{points}",
        "team_totalhome": f"s;{period};tt;{points};home",
        "team_totalaway": f"s;{period};tt;{points};away",

        # Atleasts
        "Alternate Assists": f"pp;0;ss;asst;{points}",
        "Alternate Points": f"pp;0;ss;pts;{points}",
        "Alternate Three Point Field Goals Made": f"pp;0;ss;3pt;{points}",
        "Alternate Total Rebounds": f"pp;0;ss;reb;{points}",
        "Alternate Pts + Reb + Ast": f"pp;0;ss;pra;{points}",

        "Alternate Shots on goal": f"pp;0;ss;sog;{points}",
        "Alternate Saves": f"pp;0;ss;saves;{points}",
        "Alternate Goals": f"pp;0;ss;goals;{points}",

        "Alternate Hits": f"pp;0;ss;hit;{points}",
        "Alternate Home runs": f"pp;0;ou;hr;{points}",
        "Alternate Stolen bases": f"pp;0;ss;sb;{points}",
        "Alternate Strikeouts": f"pp;0;ss;so;{points}",
        "Alternate Earned runs": f"pp;0;ss;er;{points}",
        "Alternate Hits Allowed": f"pp;0;ss;hita;{points}",
        "Alternate Runs + RBIs": f"pp;0;ss;r+r;{points}"
    }

    # Return the result based on the unit
    return switcher.get(unit, None)


def getTeamAbr(teamName):
    switcher = {
        'arizona diamondbacks': 'ARI',
        'atlanta braves': 'ATL',
        'baltimore orioles': 'BAL',
        'boston red sox': 'BOS',
        'chicago cubs': 'CHC',
        'chicago white sox': 'CWS',  # You can add 'CWS' as an alternate if needed
        'cincinnati reds': 'CIN',
        'cleveland guardians': 'CLE',
        'colorado rockies': 'COL',
        'detroit tigers': 'DET',
        'miami marlins': 'MIA',
        'houston astros': 'HOU',
        'kansas city royals': 'KAN',
        'los angeles angels': 'LAA',
        'los angeles dodgers': 'LAD',
        'milwaukee brewers': 'MIL',
        'minnesota twins': 'MIN',
        'new york mets': 'NYM',
        'new york yankees': 'NYY',
        'oakland athletics': 'OAK',
        'philadelphia phillies': 'PHI',
        'pittsburgh pirates': 'PIT',
        'san diego padres': 'SD',
        'san francisco giants': 'SF',
        'seattle mariners': 'SEA',
        'st. louis cardinals': 'STL',
        'tampa bay rays': 'TB',
        'texas rangers': 'TEX',
        'toronto blue jays': 'TOR',
        'washington nationals': 'WAS',

        # NFL
        "arizona cardinals": "ARI",
        "atlanta falcons": "ATL",
        "baltimore ravens": "BAL",
        "buffalo bills": "BUF",
        "carolina panthers": "CAR",
        "chicago bears": "CHI",
        "cincinnati bengals": "CIN",
        "cleveland browns": "CLE",
        "dallas cowboys": "DAL",
        "denver broncos": "DEN",
        "detroit lions": "DET",
        "green bay packers": "GB",
        "houston texans": "HOU",
        "indianapolis colts": "IND",
        "jacksonville jaguars": "JAX",
        "kansas city chiefs": "KC",
        "las vegas raiders": "LV",
        "los angeles chargers": "LAC",
        "los angeles rams": "LAR",
        "miami dolphins": "MIA",
        "minnesota vikings": "MIN",
        "new england patriots": "NE",
        "new orleans saints": "NO",
        "new york giants": "NYG",
        "new york jets": "NYJ",
        "philadelphia eagles": "PHI",
        "pittsburgh steelers": "PIT",
        "san francisco 49ers": "SF",
        "seattle seahawks": "SEA",
        "tampa bay buccaneers": "TB",
        "tennessee titans": "TEN",
        "washington commanders": "WAS"
    }
    return switcher.get(teamName, teamName)


def dfByLoop(combined, gamesDict):
    # Making a pandas dataframe, I also need to add the key column later on
    gameId = []
    teams = []
    league = []
    units = []
    keys = []
    points = []
    designation = []
    odds = []
    betOdds = []
    playName = []
    dates = []

    # Gets all of the Over Under and Atleast odds of the same game
    for r in combined:
        if r["type"] == "ou":
            # print(r["statistic"] + " Over/Under")
            statistic = r["statistic"]
            for plyr in r["players"]:
                # I'm getting the over and under based on condition in the json
                over_odds = next(
                    (market["odds"] for market in plyr["markets"] if market["condition"] == 3), None)
                under_odds = next(
                    (market["odds"] for market in plyr["markets"] if market["condition"] == 1), None)
                if under_odds is None or over_odds is None:
                    continue
                # print(statistic + plyr["name"] + "\nLine: " + str(plyr["markets"][0]
                #                                                  ["value"]) + "\nOver: " + str(over_odds) + "\nUnder: " + str(under_odds))
                gameId.append(plyr["markets"][0]["game1Id"])
                teams.append(gamesDict[str(plyr["markets"][0]["game1Id"])][0])
                league.append(gamesDict[str(plyr["markets"][0]["game1Id"])][1])
                units.append(statistic)
                keys.append(makeKey(statistic, plyr["markets"][0]["value"]))
                points.append(plyr["markets"][0]["value"])
                designation.append("over")
                odds.append(over_odds)
                betOdds.append(decToAmerican(over_odds))

                playerName = plyr["name"]
                nsplit = playerName.split()
                name = playerName.replace(nsplit[0], nsplit[0][0] + '.', 1)
                playName.append(name)
                dates.append(gamesDict[str(plyr["markets"][0]["game1Id"])][2])

                gameId.append(str(plyr["markets"][0]["game1Id"]))
                teams.append(gamesDict[str(plyr["markets"][0]["game1Id"])][0])
                league.append(gamesDict[str(plyr["markets"][0]["game1Id"])][1])
                units.append(statistic)
                keys.append(makeKey(statistic, plyr["markets"][0]["value"]))
                points.append(plyr["markets"][0]["value"])
                designation.append("under")
                odds.append(under_odds)
                betOdds.append(decToAmerican(under_odds))
                playName.append(name)
                dates.append(gamesDict[str(plyr["markets"][0]["game1Id"])][2])

        elif r["type"] == "ss":
            # print(r["statistic"] + " Atleast")
            statistic = r["statistic"]
            for plyr in r["players"]:
                for mrkt in plyr["markets"]:
                    # print(statistic + plyr["name"] + "\nLine: " + str(mrkt["value"]) + "\nOver: " + str(
                    #    mrkt["odds"]))
                    gameId.append(str(plyr["markets"][0]["game1Id"]))
                    teams.append(
                        gamesDict[str(plyr["markets"][0]["game1Id"])][0])
                    league.append(
                        gamesDict[str(plyr["markets"][0]["game1Id"])][1])
                    units.append("Alternate " + statistic)
                    keys.append(
                        makeKey("Alternate " + statistic, mrkt["value"] - 0.5))
                    points.append(mrkt["value"] - 0.5)
                    designation.append("over")
                    odds.append(mrkt["odds"])
                    betOdds.append(decToAmerican(mrkt['odds']))
                    playerName = plyr["name"]
                    nsplit = playerName.split()
                    name = playerName.replace(nsplit[0], nsplit[0][0] + '.', 1)
                    playName.append(name)
                    dates.append(
                        gamesDict[str(plyr["markets"][0]["game1Id"])][2])

    data = {"GameId": gameId, 'Teams': teams, 'League': league, "Key": keys, "Points": points, "Category": units,
            "Designation": designation, "BO dec_odds": odds, 'BO Odds': betOdds, "Name": playName, 'Date': dates}
    df = pd.DataFrame(data)

    # This removes all rows where key is None
    df = df[np.logical_not(pd.isna(df['Key']))]

    return df


def decimalToAmerican(df):
    conditions = [
        df['odds'] >= 2.0,
        df['odds'] < 2.0
    ]
    choices = [
        100*(df['odds'] - 1),
        (-100)/(df['odds'] - 1)
    ]
    americanOdds = np.select(conditions, choices, default=0).round()
    return americanOdds


def americanToDecimal(americanOdd):
    if americanOdd > 0:
        decimalOdd = 1 + (americanOdd / 100)
    elif americanOdd < 0:
        decimalOdd = 1 + (100 / abs(americanOdd))
    else:
        decimalOdd = 1.0  # Odds of 0 would be an edge case
    return round(decimalOdd, 2)


def dfWPandas(df, sport, gamesDict):
    df = df.explode('players')
    df = json_normalize(df['players'])

    df = df.explode('markets')
    markets_df = json_normalize(df['markets'])

    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, markets_df], axis=1)

    df = generateColumns(df, sport, gamesDict)
    df['BetOnline Odds'] = decimalToAmerican(df)

    columnsToKeep = ['name', 'team', 'condition', 'game1Id',
                     'odds', 'Points', 'Category', 'Designation', 'Units', 'BetOnline Odds', 'Key']
    df = df[columnsToKeep]
    df.rename(columns={'name': 'Play Name', 'game1Id': 'GameId'}, inplace=True)
    return df


# Function that turns the dataframe into a csv file
def makeCsv(df, name):
    df.to_csv(name+"BetOnline.csv")


def getPropsgameIds(game_Ids):
    gameIds, gamesDict = asyncio.run(getAsyncPropsIDs(game_Ids))
    return gameIds, gamesDict
