import grequests
import DraftKings.Draftkings as dk
import Pointsbet.PointsBetMyko as pb
import BetOnline.BetOnline as bo
import Fanduel.FanDuel_Liam as fd
import Pinnacle.Pinnacle_Liam as pn
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
import time
import os
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

# Checks if the urls were made within the hour, if it isnt we remake the urls
if time.time() - os.path.getmtime('urlsForRequests.json') > 3600:
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
    urlsGetBO = bo.getPropsUrls2(gamesDict)
    urlsGet = urlsGet + urlsGetBO
    urlsPostBO = bo.makeGameUrls(gameIdsByLeague)
    urlsPost = urlsPost + urlsPostBO

    # FanDuel
    dataFD = fd.getData()
    urlsFD = fd.makeRequestLinks(dataFD)
    urlsGet = urlsGet + urlsFD

    # Pinnacle
    mlbPN = pn.getDataMlb()
    nameUrlsPN, oddsUrlsPN = pn.makeRequestLinks(mlbPN)
    urlsGet = urlsGet + nameUrlsPN + oddsUrlsPN

    urls = {'urlsGet': urlsGet, 'urlsPost': urlsPost, 'urlsDKLength': len(urlsDK), 'urlsPBLength': len(urlsPB), 'urlsGetBOLength': len(
        urlsGetBO), 'urlsPostBOLength': len(urlsPostBO), 'urlsFDLength': len(urlsFD), 'nameUrlsPNLength': len(nameUrlsPN), 'oddsUrlsPNLength': len(oddsUrlsPN), 'gamesDictBO': gamesDict}

    with open('urlsForRequests.json', 'w') as file:
        json.dump(urls, file, indent=4)

else:
    with open('urlsForRequests.json', 'r') as file:
        urls = json.load(file)

timer = time.time()
responsesGet = (grequests.get(u['url'], headers=u['headers'])
                for u in urls['urlsGet'])
responsesPost = (grequests.post(
    u['url'], headers=u['headers'], json=u['payload']) for u in urls['urlsPost'])
responses = grequests.map(list(responsesGet) + list(responsesPost))

print(f'Requests of all sites took', time.time() - timer, ' seconds')

responsesDK = responses[:urls['urlsDKLength']]
responsesPB = responses[urls['urlsDKLength']:urls['urlsDKLength'] + urls['urlsPBLength']]
responsesGetBO = responses[urls['urlsDKLength'] + urls['urlsPBLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength']]
responsesFD = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength']]

responseNamePN = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength']]
responseOddsPN = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength']]

responsesPostBO = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength'] + urls['urlsPostBOLength']]


timer = time.time()
dk.gigaDump2(responsesDK)
print(time.time() - timer)
dKJsonResp = [response.json() for response in responsesDK]
with open("respDK.json", 'w') as json_file:
    json.dump(dKJsonResp[0], json_file, indent=4)

timer = time.time()
pb.gigaDump2(responsesPB)
print(time.time() - timer)

timer = time.time()
# this is ugly asf please cleanup later
# this whole thing is a mess it needs so much cleaning
# Look at repsonse json files to further understand
postBOJSonResp = [response.json() for response in responsesPostBO]
getBOJSonResp = [response.json()[0]
                 for response in responsesGetBO if response.json()]
# with open("postBO.json", 'w') as json_file:
#     json.dump(postBOJSonResp, json_file, indent=4)
teamsDf = bo.manipulationLoop(postBOJSonResp)
propsDf = bo.dfByLoop(getBOJSonResp, urls['gamesDictBO'])
bigDf = pd.concat([teamsDf, propsDf])
dir = git.Repo('.', search_parent_directories=True).working_tree_dir
bigDf.to_csv(str(dir) + '/bin/BetOnlineGigaDump.csv', index=False)
print(time.time() - timer)

timer = time.time()
fd.gigaDump2(responsesFD)
print(time.time() - timer)

timer = time.time()
pn.gigaDump2(responseNamePN, responseOddsPN)
print(time.time() - timer)


# json_file_path = 'urls.json'

# # Save the 'urls' object to a JSON file
# with open(json_file_path, 'w') as json_file:
#     json.dump(urls, json_file, indent=4)
