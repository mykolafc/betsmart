import FanDuel_Liam as fd
import grequests
import requests
import json
import zlib

dataFD = fd.getData()
urlsFD = fd.makeRequestLinks(dataFD)
responsesGet = (grequests.get(u['url'], headers=u['headers']) for u in urlsFD)
responses = grequests.map(list(responsesGet))

fd.gigaDump2(responses)

# url = 'https://smp.ny.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices?priceHistory=1'
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "origin": "https://sportsbook.fanduel.com",
#     "referer": "https://sportsbook.fanduel.com/",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
#     "x-application": "FhMFpcPWXMeyZxOx"
# }
# payload = {
#     "marketIds": [
#         '736.97514125'
#     ]
# }

# response = requests.post(url, headers=headers, json=payload)
# with open('fanduelPostNfl.json', 'w') as file:
#     json.dump(response.json(), file, indent=4)

# response = requests.get(
#     'https://sbapi.on.sportsbook.fanduel.ca/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276281&tab=quarter-props&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true&useQuickBetsNFL=true')

# with open('fanduelEVERYTHINGPLEASE.json', 'w') as file:
#     json.dump(response.json(), file, indent=4)


# Define the URL
# this url needs to be implemented inside of the makeLinks function so that we can access bare odds of the nfl
# url = "https://sbapi.az.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33273135&tab=rushing-props&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true&useQuickBetsNFL=true"

# # Define the headers
# headers = {
#     "authority": "sbapi.az.sportsbook.fanduel.com",
#     "method": "GET",
#     "path": "/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33273135&tab=rushing-props&useCombinedTouchdownsVirtualMarket=true&usePulse=true&useQuickBets=true&useQuickBetsNFL=true",
#     "scheme": "https",
#     "accept": "application/json",
#     "accept-encoding": "identity",
#     "accept-language": "en-US,en;q=0.9",
#     "origin": "https://sportsbook.fanduel.com",
#     "referer": "https://sportsbook.fanduel.com/",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
# }


# # Make the GET request
# response = requests.get(url, headers=headers)

# # Check if the response was successful (status code 200)
# if response.status_code == 200:
#     # Parse the response JSON
#     try:
#         data = response.json()

#         # Save the data to a file
#         with open('fanduel_event_rushing_data.json', 'w') as file:
#             json.dump(data, file, indent=4)

#         print("Data saved successfully!")
#     except json.JSONDecodeError as e:
#         print("Failed to parse JSON. Error:", e)
# else:
#     print(f"Failed to retrieve data. Status Code: {response.status_code}")
