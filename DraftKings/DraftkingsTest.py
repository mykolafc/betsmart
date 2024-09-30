import Draftkings as dk
import grequests
import requests
import json

# URLs to request data from
# url1 = "https://sportsbook-nash.draftkings.com/api/sportscontent/navigation/dkcaon/v1/nav/leagues/84240?format=json"
# url2 = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkcaon/v1/events/30568799/categories/1342?appname=web"

# # Headers (based on the details you provided)
# headers = {
#     "accept": "*/*",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "en-US,en;q=0.9",
#     "origin": "https://sportsbook.draftkings.com",
#     "referer": "https://sportsbook.draftkings.com/",
#     "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
#     "sec-ch-ua-mobile": "?1",
#     "sec-ch-ua-platform": '"Android"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
#     "x-client-feature": "event-slider",
#     "x-client-name": "web",
#     "x-client-page": "event",
#     "x-client-version": "2439.1.1.22",
# }

dataNfl = dk.getDataNfl()
dataMlb = dk.getDataMlbNEW()
urlsNfl = dk.makeRequestLinksNEW(dataNfl)
urlsMlb = dk.makeRequestLinksNEW(dataMlb)
urls = urlsNfl + urlsMlb
responses = (grequests.get(u['url'], headers=u['headers'])
             for u in urls)
responses = grequests.map(responses)
dk.gigaDump(responses)
