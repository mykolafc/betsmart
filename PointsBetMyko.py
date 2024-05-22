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

# This should return the JSON file of the mlb front page from PointsBet
# I realized the problem is that we didnt include the headers parameter in the get request

# It's possible that some things in this link variable so it might not always be this EXACT link
url = "https://api.on.pointsbet.com/api/v2/competitions/7366/events/featured?includeLive=false&page=1"

headers = {
    "authority": "api.on.pointsbet.com",
    "method": "GET",
    "path": "/api/v2/competitions/7366/events/featured?includeLive=false&page=1",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",

    # This changes based on the current time obv so it needs to be a variable attributed to the time
    "If-Modified-Since": formatdate(timeval=datetime.now().timestamp(), localtime=False, usegmt=True),
    "Origin": "https://on.pointsbet.ca",
    "Priority": "u=1, i",
    "Referer": "https://on.pointsbet.ca/",
    "Request-Context": "appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd",
    "Request-Id": "|5f2a39d254164a50847559703c0e1f05.8a4cfc06025146c4",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Traceparent": "00-5f2a39d254164a50847559703c0e1f05-8a4cfc06025146c4-01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

response = requests.get(url, headers=headers)
data = response.json()

with open('PointsbetMlb.json', 'w') as f:
    json.dump(data, f, indent=4)

filtered_data = []

odds = {}
numodds = {}

for i, x in enumerate(data['events']):
    odds[i] = 0
    numodds[i] = 0
    for y in x['specialFixedOddsMarkets']:
        for z in y['outcomes']:
            filtered_data.append(z)
            odds[i] += z['price']
            numodds[i] += 1


for i in odds:
    if numodds[i] != 0:
        odds[i] = odds[i] / numodds[i]
            
df = pd.json_normalize(filtered_data)

df.to_csv('PointsBetMlb.csv', index=False)


print("Average Odds: \n")
for i in odds:
    print("Game " + str(i) + ": " + str(odds[i]) + "\n")