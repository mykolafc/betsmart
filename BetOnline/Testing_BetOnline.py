import grequests
import requests
import asyncio
import aiohttp
import concurrent.futures
import pandas as pd
import BetOnline as bet
# import testingNestedAsync as nest
from pandas import json_normalize
from datetime import datetime, timedelta, date
import time
import requests
import json
import numpy as np

game_Ids, gameIdsByLeague = bet.getGeneralGameIDs()
# print(game_Ids)
gameIds, gamesDict = bet.getPropsgameIds(game_Ids)
# print(gamesDict)
urls = bet.getPropsUrls(gamesDict)
# print(gameIdsByLeague)
# print(urls)
# This is wrong because it uses the propIds for the payloads instead of the team Ids
# I could probably assign the team Ids to the right sport inside of getGeneralGameIds()
payloads = bet.makePayloads(gameIdsByLeague)
# print(payloads)
start = time.perf_counter()
teamsResponse, propsResponse = bet.threadedRequests(payloads, urls)
teamsDf = bet.manipulationLoop(teamsResponse)
propsDf = bet.dfByLoop(propsResponse, gamesDict)
bigDf = pd.concat([teamsDf, propsDf])
nfl = bigDf[bigDf['League'] == 'NFL'].copy()
nba = bigDf[bigDf['League'] == 'NBA'].copy()
nhl = bigDf[bigDf['League'] == 'NHL'].copy()
print(
    f'Process of the stuff that will repeat takes {(time.perf_counter() - start)} seconds')
bigDf.to_csv('ALLODDSFINALIZING.csv')
nfl.to_csv('nflFinalizing.csv')
nba.to_csv('nbaFinalizing.csv')
nhl.to_csv('nhlFinalizing.csv')
