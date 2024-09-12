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

dataNfl = pn.getDataNfl()
dataMlb = pn.getDataMlb()

nameUrlsNfl, oddsUrlsNfl = pn.makeRequestLinks(dataNfl)
nameUrlsMlb, oddsUrlsMlb = pn.makeRequestLinks(dataMlb)
nameUrls = nameUrlsNfl + nameUrlsMlb
oddsUrls = oddsUrlsNfl + oddsUrlsMlb

# Prepare the GET requests
name_requests = [grequests.get(u['url'], headers=u['headers'])
                 for u in nameUrls]
odds_requests = [grequests.get(u['url'], headers=u['headers'])
                 for u in oddsUrls]

# Send the requests and get the responses
respName = grequests.map(name_requests)
respOdds = grequests.map(odds_requests)


pn.gigaDump2(respName, respOdds)
