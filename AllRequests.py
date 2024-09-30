import grequests
import compare
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


def doAllRequests(betOnline=True):
    # Checks if the urls were made within the hour, if it isnt we remake the urls
    if time.time() - os.path.getmtime('urlsForRequests.json') > 30:

        with open('urlsForRequests.json', 'r') as file:
            urls = json.load(file)

        urlsGet = []
        urlsPost = []

        # DraftKings
        mlbDK = dk.getDataMlbNEW()
        nflDK = dk.getDataNfl()
        urlsMlbDK = dk.makeRequestLinksNEW(mlbDK)
        urlsNflDK = dk.makeRequestLinksNEW(nflDK)
        urlsDK = urlsMlbDK + urlsNflDK
        urlsGet = urlsGet + urlsDK

        # PointsBet
        mlbPB = pb.getDataMlb()
        nflPB = pb.getDataNfl()
        urlsMlbPB = pb.makeRequestLinks(mlbPB)
        urlsNflPB = pb.makeRequestLinks(nflPB)
        urlsPB = urlsMlbPB + urlsNflPB
        urlsGet = urlsGet + urlsPB

        # BetOnline
        if betOnline:
            game_Ids, gameIdsByLeague = bo.getGeneralGameIDs(days=5)
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
        nflPN = pn.getDataNfl()
        nameUrlsMlbPN, oddsUrlsMlbPN = pn.makeRequestLinks(mlbPN)
        nameUrlsNflPN, oddsUrlsNflPN = pn.makeRequestLinks(nflPN)
        nameUrlsPN = nameUrlsMlbPN + nameUrlsNflPN
        oddsUrlsPN = oddsUrlsMlbPN + oddsUrlsNflPN
        urlsGet = urlsGet + nameUrlsPN + oddsUrlsPN

        # Updating URLs dictionary based on BetOnline's inclusion
        urls = {'urlsGet': urlsGet, 'urlsPost': urlsPost, 'urlsDKLength': len(urlsDK), 'urlsPBLength': len(
            urlsPB), 'urlsFDLength': len(urlsFD), 'nameUrlsPNLength': len(nameUrlsPN), 'oddsUrlsPNLength': len(oddsUrlsPN)}
        if betOnline:
            urls.update({'urlsGetBOLength': len(urlsGetBO), 'urlsPostBOLength': len(
                urlsPostBO), 'gamesDictBO': gamesDict})

        with open('urlsForRequests.json', 'w') as file:
            json.dump(urls, file, indent=4)

    else:
        with open('urlsForRequests.json', 'r') as file:
            urls = json.load(file)

    timer = time.time()
    responsesGet = (grequests.get(
        u['url'], headers=u['headers']) for u in urls['urlsGet'])
    responsesPost = (grequests.post(
        u['url'], headers=u['headers'], json=u['payload']) for u in urls['urlsPost'])
    responses = grequests.map(list(responsesGet) + list(responsesPost))

    print(f'Requests of all sites took', time.time() - timer, ' seconds')

    # Process DraftKings responses
    responsesDK = responses[:urls['urlsDKLength']]
    dk.gigaDump(responsesDK)

    # Process PointsBet responses
    responsesPB = responses[urls['urlsDKLength']:urls['urlsDKLength'] + urls['urlsPBLength']]
    pb.gigaDump2(responsesPB)

    # Process BetOnline responses if enabled
    if betOnline:
        responsesGetBO = responses[urls['urlsDKLength'] + urls['urlsPBLength']                                   :urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength']]
        responsesPostBO = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength']                                    :urls['urlsDKLength'] + urls['urlsPBLength'] + urls['urlsGetBOLength'] + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength'] + urls['urlsPostBOLength']]

        postBOJSonResp = [response.json()
                          for response in responsesPostBO if response.json()]
        getBOJSonResp = [response.json()[0]
                         for response in responsesGetBO if response.json()]

        teamsDf = bo.manipulationLoop(postBOJSonResp)
        propsDf = bo.dfByLoop(getBOJSonResp, urls['gamesDictBO'])
        bigDf = pd.concat([teamsDf, propsDf])

        dir = git.Repo('.', search_parent_directories=True).working_tree_dir
        bigDf.to_csv(str(dir) + '/bin/BetOnlineGigaDump.csv', index=False)

    # Process FanDuel responses
    responsesFD = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + (
        urls['urlsGetBOLength'] if betOnline else 0):urls['urlsDKLength'] + urls['urlsPBLength'] + (urls['urlsGetBOLength'] if betOnline else 0) + urls['urlsFDLength']]
    fd.gigaDump2(responsesFD)

    # Process Pinnacle responses
    responseNamePN = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + (urls['urlsGetBOLength'] if betOnline else 0) + urls['urlsFDLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + (
        urls['urlsGetBOLength'] if betOnline else 0) + urls['urlsFDLength'] + urls['nameUrlsPNLength']]
    responseOddsPN = responses[urls['urlsDKLength'] + urls['urlsPBLength'] + (urls['urlsGetBOLength'] if betOnline else 0) + urls['urlsFDLength'] + urls['nameUrlsPNLength']:urls['urlsDKLength'] + urls['urlsPBLength'] + (
        urls['urlsGetBOLength'] if betOnline else 0) + urls['urlsFDLength'] + urls['nameUrlsPNLength'] + urls['oddsUrlsPNLength']]

    pn.gigaDump2(responseNamePN, responseOddsPN)


def sendNotif(message):
    # This uses the telegram bot to send me a notification
    botToken = '7604827625:AAGypvQCTaO-NqBMyHSIQBlxHAOT0b4BsEs'
    chatId = '7530223501'
    url = f"https://api.telegram.org/bot{botToken}/sendMessage"
    params = {
        'chat_id': chatId,
        'text': message
    }
    requests.get(url, params=params)


def findArb(roi):
    badRoi = True
    while (badRoi):
        try:
            doAllRequests(betOnline=False)
            merged_df = compare.compareOdds(betOnline=False)
            badRoi = not np.any(merged_df['arb ROI%'] > roi)
            if not badRoi:
                # Send notification immediately when an arb is found
                sendNotif(f'There is an arb with atleast a {roi}% roi')

                # Save the CSV file
                dir = git.Repo(
                    '.', search_parent_directories=True).working_tree_dir
                merged_df.to_csv(str(dir) + '/bin/combined.csv', index=False)

                # Break the loop as an arb has been found and notified
                break
            time.sleep(90)
        except ZeroDivisionError as e:
            print(f"ZeroDivisionError occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def runAlg():
    doAllRequests(betOnline=False)
    merged_df = compare.compareOdds(betOnline=False)
    dir = git.Repo('.', search_parent_directories=True).working_tree_dir
    merged_df.to_csv(str(dir) + '/bin/combined.csv', index=False)


option = input('Find arb(1) or Run algorithm(2)? ')
if (option == '1'):
    findArb(2)
elif (option == '2'):
    runAlg()
