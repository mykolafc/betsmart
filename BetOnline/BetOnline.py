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
import json
import numpy as np


###########################################################################################################
# RESPONSE REQUESTS
###########################################################################################################

# Doing Grequests for post requests since for some reason Asyncio seems to not work with payloads
def fetchGrequests(url, headers, payloads):
    unsentRequests = [grequests.post(
        url, headers=headers, json=payload) for payload in payloads]
    responses = grequests.map(unsentRequests)
    jsonResponses = [response.json() for response in responses]
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
    # I don't think theres gonna be baseball for a while
    requestPayloadBaseball = {"Sport": "baseball", "League": "mlb",
                              "ScheduleText": None, "Period": -1}
    # Soccer is different but below is the one for the premier league
    # requestPayload = {"Sport": "soccer", "League": "epl", "ScheduleText": "english-premier-league", "Period": -1}
    payloads = [requestPayloadFootball,
                requestPayloadBasket, requestPayloadHockey]
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
        league = gamesByLeague['GameOffering']['League']
        gamesData = gamesByLeague['GameOffering']['GamesDescription']
        game_IdsByLeague = []
        now = datetime.now()
        for game in gamesData:
            gameDate = datetime.strptime(game['GameDate'], '%m/%d/%Y')
            if abs((now - gameDate).days) <= days:
                game_Id = game['Game']['GameId']
                game_IdsByLeague.append(game_Id)
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
            "https://bv2.digitalsportstech.com/api/game?sb=betonline&event="+str(game_Id))
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
            gamesDict[gameId] = [jr[0]['team2']['title'] +
                                 '(away) vs ' + jr[0]['team1']['title'] + '(home)', jr[0]['league'].upper()]
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
    payloads = nflPayloads + nbaPayloads + nhlPayloads
    return payloads


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
    odds = []
    category = []

    periodEvents = []
    for game in data:
        periodEvents = periodEvents + game['EventOffering']['PeriodEvents']
    for event in periodEvents:
        game_Id = event['Event']['GameId']
        teams1 = event['Event']['AwayTeam'].lower() + '(away) vs ' + \
            event['Event']['HomeTeam'].lower() + '(home)'
        league1 = event['Event']['CorrelationId'].split('-')[1].split(' ')[0]
        name1 = event['Name']
        # Home
        # SpreadLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('spread')
        point.append(event['Event']['AwayLine']['SpreadLine']['Point'])
        designation.append(None)
        odds.append(event['Event']['AwayLine']['SpreadLine']['Line'])
        name.append(name1)
        # MoneyLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('moneyline')
        point.append(None)
        designation.append(None)
        odds.append(event['Event']['AwayLine']['MoneyLine']['Line'])
        name.append(name1)
        # TeamTotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('team_total')
        point.append(event['Event']['AwayLine']['TeamTotalLine']['Point'])
        designation.append('over')
        odds.append(event['Event']['AwayLine']
                    ['TeamTotalLine']['Over']['Line'])
        name.append(name1)
        # TeamTotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('away')
        category.append('team_total')
        point.append(event['Event']['AwayLine']['TeamTotalLine']['Point'])
        designation.append('under')
        odds.append(event['Event']['AwayLine']
                    ['TeamTotalLine']['Under']['Line'])
        name.append(name1)
        # Home
        # SpreadLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('spread')
        point.append(event['Event']['HomeLine']['SpreadLine']['Point'])
        designation.append(None)
        odds.append(event['Event']['HomeLine']['SpreadLine']['Line'])
        name.append(name1)
        # MoneyLine
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('moneyline')
        point.append(None)
        designation.append(None)
        odds.append(event['Event']['HomeLine']['MoneyLine']['Line'])
        name.append(name1)
        # TeamTotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('team_total')
        point.append(event['Event']['HomeLine']['TeamTotalLine']['Point'])
        designation.append('over')
        odds.append(event['Event']['HomeLine']
                    ['TeamTotalLine']['Over']['Line'])
        name.append(name1)
        # TeamTotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append('home')
        category.append('team_total')
        point.append(event['Event']['HomeLine']['TeamTotalLine']['Point'])
        designation.append('under')
        odds.append(event['Event']['HomeLine']
                    ['TeamTotalLine']['Under']['Line'])
        name.append(name1)
        # TotalLine over
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append(None)
        category.append('total')
        point.append(event['Event']['TotalLine']['TotalLine']['Point'])
        designation.append('over')
        odds.append(event['Event']['TotalLine']['TotalLine']['Over']['Line'])
        name.append(name1)
        # TotalLine under
        gameId.append(game_Id)
        teams.append(teams1)
        league.append(league1)
        side.append(None)
        category.append('total')
        point.append(event['Event']['TotalLine']['TotalLine']['Point'])
        designation.append('under')
        odds.append(event['Event']['TotalLine']['TotalLine']['Under']['Line'])
        name.append(name1)

    finalData = {'Name': name, 'GameId': gameId, 'teams': teams, 'League': league, 'Designation': designation,
                 'Side': side, 'Point': point, 'Odds': odds, 'Category': category}
    df = pd.DataFrame(finalData)
    df = df[df['Odds'] != 0]
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
        atleastLinks(gameIdsBySport.get('NHL'), categoriesAtleastHockey)
    # if sport == 'football':
    #     urls = overUnderLinks(gameIds, categoriesOUFootball) + \
    #         atleastLinks(gameIds, categoriesAtleastFootball)
    # elif sport == 'hockey':
    #     urls = overUnderLinks(gameIds, categoriesOUHockey) + \
    #         atleastLinks(gameIds, categoriesAtleastHockey)
    # elif sport == 'basketball':
    #     urls = overUnderLinks(gameIds, categoriesOUBasket) + \
    #         atleastLinks(gameIds, categoriesAtlestBasket)
    return urls


def decToAmerican(odd):
    if odd >= 2.0:
        odd = 100*(odd - 1)
    else:
        odd = (-100)/(odd - 1)
    return round(odd)


def makeKey(unit, point):
    if unit == 'Touchdowns':
        key = 'pp;0;ou;td;' + str(point)
    elif unit == 'Receiving Yards':
        key = 'pp;0;ou;recyds;' + str(point)
    # Finish this when you figure out what becomes what key cuz this hella weird


def dfByLoop(combined, gamesDict):
    # Making a pandas dataframe, I also need to add the key column later on
    gameId = []
    teams = []
    league = []
    units = []
    points = []
    category = []
    designation = []
    odds = []
    betOdds = []
    playName = []

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
                # print(statistic + plyr["name"] + "\nLine: " + str(plyr["markets"][0]
                #                                                  ["value"]) + "\nOver: " + str(over_odds) + "\nUnder: " + str(under_odds))
                gameId.append(plyr["markets"][0]["game1Id"])
                teams.append(gamesDict[plyr["markets"][0]["game1Id"]][0])
                league.append(gamesDict[plyr["markets"][0]["game1Id"]][1])
                units.append(statistic)
                points.append(plyr["markets"][0]["value"])
                category.append('Player Props')
                designation.append("over")
                odds.append(over_odds)
                betOdds.append(decToAmerican(over_odds))
                playName.append(plyr["name"])
                gameId.append(plyr["markets"][0]["game1Id"])
                teams.append(gamesDict[plyr["markets"][0]["game1Id"]][0])
                league.append(gamesDict[plyr["markets"][0]["game1Id"]][1])
                units.append(statistic)
                points.append(plyr["markets"][0]["value"])
                category.append('Player Props')
                designation.append("under")
                odds.append(under_odds)
                betOdds.append(decToAmerican(under_odds))
                playName.append(plyr["name"])

        elif r["type"] == "ss":
            # print(r["statistic"] + " Atleast")
            statistic = r["statistic"]
            for plyr in r["players"]:
                for mrkt in plyr["markets"]:
                    # print(statistic + plyr["name"] + "\nLine: " + str(mrkt["value"]) + "\nOver: " + str(
                    #    mrkt["odds"]))
                    gameId.append(plyr["markets"][0]["game1Id"])
                    teams.append(gamesDict[plyr["markets"][0]["game1Id"]][0])
                    league.append(gamesDict[plyr["markets"][0]["game1Id"]][1])
                    units.append(statistic)
                    points.append(mrkt["value"] - 0.5)
                    category.append('Player Props')
                    designation.append("over")
                    odds.append(mrkt["odds"])
                    betOdds.append(decToAmerican(mrkt['odds']))
                    playName.append(plyr["name"])

    data = {"GameId": gameId, 'teams': teams, 'League': league, "Units": units, "Point": points, "Category": category,
            "Designation": designation, "dec_odds": odds, 'Odds': betOdds, "PlayName": playName}
    df = pd.DataFrame(data)
    return df


def generateColumns(df, sport, gamesDict):
    if sport == 'football':
        df['Category'] = 'Player Props'

        designationConditions = [
            df['condition'] == 3,
            df['condition'] == 1,
        ]
        designationChoices = [
            'over',
            'under',
        ]
        df['Designation'] = np.select(
            designationConditions, designationChoices, default='')

        unitConditions = [
            df['statistic.title'] == 'Pass Attempts',
            df['statistic.title'] == 'Passing TDs',
            df['statistic.title'].str.contains("Pass "),
            df['statistic.title'] == 'Receptions',
            df['statistic.title'] == 'Interceptions'
        ]
        unitChoices = [
            'PassAttempts',
            'TouchdownPasses',
            df['statistic.title'].str.replace('Pass ', ''),
            'PassReceptions',
            'InterceptionsCaught'
        ]
        df['Units'] = np.select(unitConditions, unitChoices,
                                default=df['statistic.title'].str.replace(' ', ''))

        df['Points'] = np.where(
            df['type'] == 1, df['value'].sub(0.5).squeeze(), df['value'])

        df['teams'] = df['game1Id'].map(gamesDict)

        keyConditions = [
            df['Units'] == 'Touchdowns',
            df['Units'] == 'ReceivingYards',
            df['Units'] == 'RushingYards',
            df['Units'] == 'Sacks',
            df['Units'] == 'InterceptionsCaught',
            df['Units'] == 'PassReceptions',
            df['Units'] == 'Carries',
            df['Units'] == 'PassAttempts',
            df['Units'] == 'TouchdownPasses',
            df['Units'] == 'PassingYards',
            df['Units'] == 'Interceptions',
            df['Units'] == 'Completions'
        ]
        keyChoices = [
            'pp;0;ou;td;' + df['Points'].astype(str),
            'pp;0;ou;recyds;' + df['Points'].astype(str),
            'pp;0;ou;rushyds;' + df['Points'].astype(str),
            'pp;0;ou;sacks;' + df['Points'].astype(str),
            'pp;0;ou;defint;' + df['Points'].astype(str),
            'pp;0;ou;recept;' + df['Points'].astype(str),
            'pp;0;ou;carry;' + df['Points'].astype(str),
            'pp;0;ou;passatt;' + df['Points'].astype(str),
            'pp;0;ou;passtds;' + df['Points'].astype(str),
            'pp;0;ou;passyds;' + df['Points'].astype(str),
            'pp;0;ou;passint;' + df['Points'].astype(str),
            'pp;0;ou;passcomp;' + df['Points'].astype(str)
        ]
        df['Key'] = np.select(keyConditions, keyChoices, default='Error')
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
