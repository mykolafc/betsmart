import grequests
import DraftKings.Draftkings as dk
import Pointsbet.PointsBetMyko as pb
import BetOnline.BetOnline as bo
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

urlsGet = []
urlsPost = []

# DraftKings
mlbDK = dk.getDataMlb()
urlsDK = dk.makeRequestLinks(mlbDK)
urlsGet = urlsGet + urlsDK

# PointsBet
mlbPB = pb.getDataMlb()
urlsPB = pb.makeRequestLinks(mlbPB)
urlsGet = urlsGet + urlsPB

# BetOnline
game_Ids, gameIdsByLeague = bo.getGeneralGameIDs()
# Don't think keeping gameIds is necessary
gameIds, gamesDict = bo.getPropsgameIds(game_Ids)
urlsBO = bo.getPropsUrls2(gamesDict)
urlsGet = urlsGet + urlsBO
urlsPostBO = bo.makeGameUrls(gameIdsByLeague)
urlsPost = urlsPost + urlsPostBO


timer = time.time()
responsesGet = (grequests.get(u['url'], headers=u['headers']) for u in urlsGet)
responsesPost = (grequests.post(
    u['url'], headers=u['headers'], json=u['payload']) for u in urlsPost)
responses = grequests.map(list(responsesGet) + list(responsesPost))

print(time.time() - timer)

responsesDK = responses[:len(urlsDK)]
responsesPB = responses[len(urlsDK):len(urlsDK)+len(urlsPB)]
responsesGetBO = responses[len(urlsDK)+len(urlsPB)
                               :len(urlsDK)+len(urlsPB)+len(urlsBO)]
responsesPostBO = responses[len(
    urlsDK)+len(urlsPB)+len(urlsBO):len(urlsDK)+len(urlsPB)+len(urlsBO)+len(urlsPostBO)]

timer = time.time()
dk.gigaDump2(responsesDK)
print(time.time() - timer)
timer = time.time()
pb.gigaDump2(responsesPB)
print(time.time() - timer)
timer = time.time()
# this is ugly asf please cleanup later
# this whole thing is a mess it needs so much cleaning
# Look at repsonse json files to further understand
postBOJSonResp = [response.json() for response in responsesPostBO]
getBOJSonResp = [response.json()[0] for response in responsesGetBO]
with open("getBO.json", 'w') as json_file:
    json.dump(getBOJSonResp, json_file, indent=4)
teamsDf = bo.manipulationLoop(postBOJSonResp)
propsDf = bo.dfByLoop(getBOJSonResp, gamesDict)
bigDf = pd.concat([teamsDf, propsDf])
dir = git.Repo('.', search_parent_directories=True).working_tree_dir
bigDf.to_csv(str(dir) + '/bin/BetOnlineGigaDump.csv', index=False)
print(time.time() - timer)


# json_file_path = 'urls.json'

# # Save the 'urls' object to a JSON file
# with open(json_file_path, 'w') as json_file:
#     json.dump(urls, json_file, indent=4)
