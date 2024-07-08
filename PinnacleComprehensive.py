import grequests
import Pinnacle
import FetchEvents
import pandas as pd

PinnacleHeader = {
    "authority": "guest.api.arcadia.pinnacle.com",
    "method": "GET",
    "path": "/0.1/sports/3/matchups?withSpecials=false",
    "scheme": "https",
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.pinnacle.com",
    "referer": "https://www.pinnacle.com/",
    "sec-ch-ua": "Chromium",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
    "x-device-uuid": "017ad4ad-74b0d8f5-526e4a1d-cdd4c5cd"
}

if __name__ == '__main__':
    sport = 'baseball'

    linkList = FetchEvents.getLinkList(['Pinnacle'], sport)
    print(linkList['name'])

    pinnacleSUrl = linkList['PinnacleS Link'].astype(str).tolist()
    pinnacleRUrl = linkList['PinnacleR Link'].astype(str).tolist()

    urls = pinnacleSUrl + pinnacleRUrl
    # Divided by two since we have two lists to request
    numberOfEvents = int(len(urls)/2)

    # Create a list of unsent requests with headers
    unsent_requests = (grequests.get(url, headers=PinnacleHeader)
                       for url in urls)
    # Send requests asynchronously and get the responses
    responses = grequests.map(unsent_requests)

    # Process the responses
    df = []
    for response in responses:
        if response is not None and response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            # Convert JSON to DataFrame
            df.append(pd.DataFrame(data))
        else:
            print(
                f"Request failed with status code: {response.status_code if response else 'No response'}")

    testDataS = df[2]
    testDataR = df[numberOfEvents+2]

    export = Pinnacle.getOdds(testDataR, testDataS, sport)
    print(export)
