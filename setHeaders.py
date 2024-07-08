FanduelHeader = {               
        "authority": "sbapi.nj.sportsbook.fanduel.com",
        "method": "GET",
        "path": "/api/content-managed-page?page=SPORT&eventTypeId=7522&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York",
        "scheme": "https",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "If-None-Match": 'W/"c282f-bBffbN6JjwaBp0K5eHWIpZ6aNIM"',
        "Origin": "https://sportsbook.fanduel.com",
        "Referer": "https://sportsbook.fanduel.com/",
        "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "X-Px-Context": "_px3=4023213641e95360cc5624dca036f5bd4af426505d05286bac2520a21241b10c:y380XFR9u5hVTE8K9zRBqJsAYpFyvFWaezwza/j99OZyLjFOKigOXissVfEoYEWnIbOMc9olBHqkLNJwGzcWaw==:1000:1NzsN0M/+NLlUxwfNST3WVOsFOFoaOEu6RkopEJoFpYShSPMcExn4hl30Mp8cLEgzhLB3LV2eUrlDA+sD/DHpSX+KJvM1B7knmzvC7Bx2MTjENhHuCCamx4uYs24uwZS/KM11SYLIR11/v9y6DDiVpeatZ1wMZkN9cAoZO/tbgaqCWWlTWLi3pQ/fpRbxhT6fP1RR8mQUAHW+HXWqVdndCe7sagM6aGtk54rJfC/tyw=;_pxvid=463ea5a5-8c83-11ee-ae47-7c75298494fc;pxcts=463eb432-8c83-11ee-ae47-6f0eeb119bc8;"
}

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

def assignOld(sourceURLs):
    
    headerList = []

    headers = {
        "Fanduel": [FanduelHeader],
        "PinnacleS": [PinnacleHeader],
        "PinnacleR": [PinnacleHeader],
        # Add more headers as needed
    }

    for source, urls in sourceURLs.items():
        header = headers.get(source, "")
        headerList.append(header)

    
    print(len(headerList))

    exit(0)

def assign(source):
    conditions = [["fanduel"], ["pinnacle"]]
    results = [FanduelHeader, PinnacleHeader]

    # Initialize the output list
    output = []

    # Iterate through each item in the info list
    for item in source:
        # Initialize a variable to keep track if a condition set was matched
        matched = False
        
        # Iterate through each set of conditions and its corresponding result
        for condition_set, result in zip(conditions, results):
            # Check if all conditions in the condition set are substrings of the info item
            if all(condition in item for condition in condition_set):
                # Append the corresponding result to the output list
                output.append(result)
                matched = True
                break  # Break the loop as we found a match
        
        # If no match was found, append an empty string to the output list
        if not matched:
            output.append("")

    return(output)

if __name__ == '__main__':
    a = ['https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33270281', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33273135', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276281', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276291', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276770', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276756', 'https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=33276765','https://guest.api.arcadia.pinnacle.com/0.1/matchups/1591734385/related', 'https://guest.api.arcadia.pinnacle.com/0.1/matchups/1591734011/related', 'https://guest.api.arcadia.pinnacle.com/0.1/matchups/1591734148/related']
    assign (a)