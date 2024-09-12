import Pointsbet.PointsBetMyko as pb
import requests
import json

url = 'https://api.on.pointsbet.com/api/v2/competitions/6/events/featured?includeLive=false&page=1'

headers = {
    'method': 'GET',
    'scheme': 'https',
    'authority': 'api.on.pointsbet.com',
    'path': '/api/v2/competitions/194/events/featured?includeLive=false&page=1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'api.on.pointsbet.com',
    # 'If-Modified-Since': 'Fri, 31 May 2024 17:27:00 GMT',
    'Origin': 'https://on.pointsbet.ca',
    'Referer': 'https://on.pointsbet.ca/',
    'Request-Context': 'appId=cid-v1:ff4f1ff0-6b1a-4166-8ec4-45a41aaa53dd',
    'Request-Id': '|ad6bb16722724ade810782b0897de4cc.8f194ef6f10e4d44',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'traceparent': '00-ad6bb16722724ade810782b0897de4cc-8f194ef6f10e4d44-01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15'
}

response = requests.get(url, headers=headers)
with open('generalPointsbetNfl.json', 'w') as json_file:
    json.dump(response.json(), json_file, indent=4)


url = 'https://api.on.pointsbet.com/api/mes/v3/events/629705'
headers = {
    "authority": "api.on.pointsbet.com",
    "method": "GET",
    "path": "/api/mes/v3/events/629705",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}
response = requests.get(url, headers=headers)
with open('generalPointsbetNflGame.json', 'w') as json_file:
    json.dump(response.json(), json_file, indent=4)
