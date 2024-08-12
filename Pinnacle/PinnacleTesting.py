import grequests
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
import Pinnacle_Liam as pn
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

# Open and read the JSON file
with open('pinnacle_data.json', 'r') as json_file:
    nameData = json.load(json_file)
with open('pinnacle_data2.json', 'r') as json_file:
    oddsData = json.load(json_file)

# Put all this bullshit in the makeurls function

data = pn.getDataMlb()
nameUrls, oddsUrls = pn.makeRequestLinks(data)

# Prepare the GET requests
name_requests = [grequests.get(u['url'], headers=u['headers']) for u in nameUrls]
odds_requests = [grequests.get(u['url'], headers=u['headers']) for u in oddsUrls]

# Send the requests and get the responses
respName = grequests.map(name_requests)
respOdds = grequests.map(odds_requests)


pn.gigaDump2(respName, respOdds)