import requests
import json

# The URL and the headers for the GET request
url = "https://sportsbook.draftkings.com/event-status"
headers = {
    "authority": "sportsbook.draftkings.com",
    "method": "GET",
    "path": "/event-status?eventId=30568642&siteExperience=CA-ON-SB",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "identity",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://sportsbook.draftkings.com",
    "referer": "https://sportsbook.draftkings.com/event/buf-bills-%40-mia-dolphins/30568642",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
}

# The parameters for the GET request
params = {
    "eventId": "30568642",
    "siteExperience": "CA-ON-SB"
}

# Making the GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()

    # Save the response to a JSON file
    with open('draftkings_event_status.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully!")
else:
    print(f"Failed to get data. Status code: {response.status_code}")


# URL for the GET request
url = "https://sportsbook.draftkings.com/event-data/event/buf-bills-%40-mia-dolphins/30568642"

# Headers for the GET request
headers = {
    "authority": "sportsbook.draftkings.com",
    "method": "GET",
    "path": "/event-data/event/buf-bills-%40-mia-dolphins/30568642",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "site=US-DK; ASP.NET_SessionId=y1capzv3fvwac5pt2yaxhogd; VIDN=47252535058; SIDN=72946329857; SSIDN=76722244218; SN=1223548523; LID=1; SINFN=PID=&AOID=&PUID=0&SSEG=&GLI=0&LID=1&site=US-DK; EXC=76722244218:73; _csrf=3386828c-44c4-40fb-a784-6c383de7adb9;",
    "origin": "https://sportsbook.draftkings.com",
    "referer": "https://sportsbook.draftkings.com/event/buf-bills-%40-mia-dolphins/30568642",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    try:
        data = response.json()

        # Save the data to a JSON file
        with open('draftkings_event_data.json', 'w') as file:
            json.dump(data, file, indent=4)

        print("Data saved successfully!")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
