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
# Don't think keeping gameIds is necessary
gameIds, gamesDict = bet.getPropsgameIds(game_Ids)
urls = bet.getPropsUrls(gamesDict)
payloads = bet.makePayloads(gameIdsByLeague)
start = time.perf_counter()
teamsResponse, propsResponse = bet.threadedRequests(payloads, urls)
teamsDf = bet.manipulationLoop(teamsResponse)
propsDf = bet.dfByLoop(propsResponse, gamesDict)
bigDf = pd.concat([teamsDf, propsDf])
nfl = bigDf[bigDf['League'] == 'NFL'].copy()
nba = bigDf[bigDf['League'] == 'NBA'].copy()
nhl = bigDf[bigDf['League'] == 'NHL'].copy()
mlb = bigDf[bigDf['League'] == 'MLB'].copy()
print(
    f'Process of the stuff that will repeat takes {(time.perf_counter() - start)} seconds')
bigDf.to_csv('ALLODDSFINALIZING.csv')
nfl.to_csv('nflFinalizing.csv')
nba.to_csv('nbaFinalizing.csv')
nhl.to_csv('nhlFinalizing.csv')
mlb.to_csv('mlbFinalizing.csv')
