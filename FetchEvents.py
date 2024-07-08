import grequests
import requests
import os
import pandas as pd
import numpy as np
from pandas import json_normalize
import time

ONE_HOUR = 60*60
TIME_DELTA = ONE_HOUR * 3

def getPinnacle(sport):
    
    featherPath = sport+'PinnacleLinks.feather'
    if os.path.exists(featherPath):
        featherAge = os.path.getmtime(featherPath)
        currentTime = time.time()
        if (currentTime - featherAge) < TIME_DELTA:
            print(str((currentTime-featherAge)/60) + ' minutes since modification')
            df = pd.read_feather(featherPath)
            return df
    

    match sport:
        case 'badminton':
            num = 1
        case 'baseball':
            num = 3
        case 'basketball':
            num = 4
        case 'boxing':
            num = 6
        case 'cricket':
            num = 8
        case 'esports':
            num = 12
        case 'football':
            num = 15
        case 'futsal':
            num = 16
        case 'golf':
            num = 17
        case 'handball':
            num = 18
        case 'hockey':
            num = 19
        case 'mma':
            num = 22
        case 'rugby':
            num = 27
        case 'snooker':
            num = 28
        case 'soccer':
            num = 29
        case 'tennis':
            num = 33
        case 'volleyball':
            num = 34
    #print(num)

    headers = {
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

    urlBase = "https://guest.api.arcadia.pinnacle.com/0.1/matchups/"
    urlStraightSuffix = "/markets/related/straight"
    urlRelatedSuffix = "/related"
    eventURL = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{num}/matchups?withSpecials=false"

    dataEvents = requests.get(eventURL, headers=headers).json()
    df = pd.DataFrame(dataEvents)
    
    #df = df.explode('parent')
    #df = pd.json_normalize(df['participants'])

    # Use json_normalize to flatten the nested 'participants' column
    df_normalized = json_normalize(df['participants'])
    df_home = json_normalize(df_normalized[0])
    df_away = json_normalize(df_normalized[1])
    # Merge the normalized dataframe with the original dataframe
    df['home'] = df_home['name']
    df['away'] = df_away['name']

    # Removing duplicates for the top sports, sometimes itll have a game twice
    # May not be most consistent way to do it but it is relatively efficient
    # It also may remove some info we want but unlucky
    df = df[df['totalMarketCount'] > 2]
    df['id'] = df['id'].astype(int).astype(str)
    # Removing undesired columns and renaming the ID column
    columnsToKeep = ['id', 'home', 'away']
    df = df[columnsToKeep]
    df.rename(columns = {'id':'Pinnacle'}, inplace=True)
    
    featherStart = time.time()
    df.to_feather(featherPath)
    featherEnd = time.time()
    print(f'Saving to feather took {featherEnd - featherStart} seconds')

    #print(df)
    return df

def getFanduel(sport):
    fanduelFeatherPath = sport+'FanduelLinks.feather'
    if os.path.exists(fanduelFeatherPath):
        featherAge = os.path.getmtime('FanduelLinks.feather')
        currentTime = time.time()
        if (currentTime - featherAge) < TIME_DELTA:
            print(str((currentTime-featherAge)/60) + ' minutes since modification')
            df = pd.read_feather(fanduelFeatherPath)
            return df
        
    match sport:
        case 'badminton':
            num = 1
        case 'baseball':
            eventTypeId = 7511
        case 'basketball':
            eventTypeId = 7522
        case 'boxing':
            eventTypeId = 6
        case 'cricket':
            eventTypeId = 4
        case 'cycling':
            eventTypeId = 11
        case 'darts':
            eventTypeId = 3503
        case 'football':
            eventTypeId = 6423
        case 'eventTypeId':
            eventTypeId = 3
        case 'handball':
            eventTypeId = 468328
        case 'hockey':
            eventTypeId = 7524
        case 'lacrosse':
            eventTypeId = 28608997
        case 'mma':
            eventTypeId = 26420387
        case 'motorspot':
            eventTypeId = 8
        case 'rugby':
            # Aussie rules football
            eventTypeId = 61420
            # Rugby League
            eventTypeId = 1477
            # Rugby Union
            eventTypeId = 5
        case 'snooker':
            eventTypeId = 6422
        case 'soccer':
            eventTypeId = 1
        case 'tennis':
            eventTypeId = 2

    headers = {
        "authority": "sbapi.nj.sportsbook.fanduel.com",
        "method": "GET",
        "path": "/api/content-managed-page?page=SPORT&eventTypeId=7522&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York",
        "scheme": "https",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control":'no-cache',
        "If-None-Match": 'W/"c282f-bBffbN6JjwaBp0K5eHWIpZ6aNIM"',
        "Origin": "https://sportsbook.fanduel.com",
        "Pragma": "no-cache",
        "Referer": "https://sportsbook.fanduel.com/",
        "Sec-Ch-Ua": '"Google Chrome";v="120", "Chromium";v="120", "Not?A_Brand";v="8"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        #"X-Px-Context": "_px3=19fa8bc7255a75a514041348f68e78febfd066abb63c16f07c6aa4a439a15b6c:qP8WYQ6wIMV1/XqHSAhAPumjYKDF0tlYNqXnAQwHT9tBaKRgh1zWWWevcMRjjHm7TjwC+nZVrr7QaBmmxUxezA==:1000:pUxEKxuR2PIQ+Dcea1Ixav05fFxN14pvYK/Gsxf+XaiUHc5U56P8akxbEjb2zVuBZaGBGjeqoJFgrugZzhiuN6YoXFcwHRxhZve9qa8Xi9qxVJDunLI65gE1LUMLVlThefk8XvYUbIbyjTRW+IWJ+zh2PPUPlcitFm4VjT9/vSgGKgg3IzGoW2SJxXMqn/G8AXprwd4B/RTsPpwC26FqmMLuWSSntVRHvwGmeLZDFU8=;_pxvid=463ea5a5-8c83-11ee-ae47-7c75298494fc;pxcts=463eb432-8c83-11ee-ae47-6f0eeb119bc8;"
    }

    eventURL = f'https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId={eventTypeId}&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York'
    dataEvents = requests.get(eventURL, headers=headers).json()
    

    df = pd.DataFrame(dataEvents['attachments']['events']).transpose()

    # Define conditions and choices for np.select
    conditions = [
        df['name'].str.contains(' @ '),
        df['name'].str.contains(' v ')
    ]

    choices_home = [
        df['name'].str.split(' @ ').str[1],
        df['name'].str.split(' v ').str[0]
    ]

    choices_away = [
        df['name'].str.split(' @ ').str[0],
        df['name'].str.split(' v ').str[1]
    ]

    # Apply np.select to create 'home' and 'away' columns
    df['home'] = np.select(conditions, choices_home, default=np.nan)
    df['away'] = np.select(conditions, choices_away, default=np.nan)

    if sport == 'baseball':                 # Remove pitcher information
        df['home'] = df['home'].str.replace(r'\s*\(.*?\)', '', regex=True)
        df['away'] = df['away'].str.replace(r'\s*\(.*?\)', '', regex=True)

    # To do: Maybe separate them by leagues in case like FC Barcelona vs Real Madrid is happening twice in the same day between the men and women or wtv
    # Find all eventTypeIds for different sports
    # Split up the runners into home and away using the '@' and 'v' parts of the strings or whatnot
    
    # Removing the outright bets
    df = df[df['away'].notna()]

    df['eventId'] = df['eventId'].astype(int).astype(str)

    if sport == 'football':
        df = df[df['competitionId'] == 12282733]     # This deletes all rows except the ones that contain NFL games

    columnsToKeep = ['eventId','name', 'home', 'away']

    df = df[columnsToKeep]

    df.rename(columns = {'eventId':'Fanduel'}, inplace=True)
    featherStart = time.time()
    df.to_feather(fanduelFeatherPath)
    featherEnd = time.time()
    print(f'Saving to feather took {featherEnd - featherStart} seconds')
    #print(df)
    return df

def getURLs(sport):
    urls = {
        'Pinnacle': {
            'url_prefix': 'https://guest.api.arcadia.pinnacle.com/0.1/sports/',
            'url_suffix': '/matchups?withSpecials=false',
            'headers': { "authority": "guest.api.arcadia.pinnacle.com", "method": "GET","path": "/0.1/sports/3/matchups?withSpecials=false","scheme": "https","accept": "application/json","content-type": "application/json",
                "origin": "https://www.pinnacle.com","referer": "https://www.pinnacle.com/","sec-ch-ua": "Chromium","sec-ch-ua-platform": "Windows","sec-fetch-dest": "empty","sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36","x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
                "x-device-uuid": "017ad4ad-74b0d8f5-526e4a1d-cdd4c5cd"
            },
            'sport_endpoints': {
                'badminton': '1',
                'baseball': '3',
                'basketball': '4',
                'boxing': '6',
                'cricket': '8',
                'esports': '12',
                'football': '15',
                'futsal': '16',
                'golf': '17',
                'handball': '18',
                'hockey': '19',
                'mma': '22',
                'rugby_union': '27',
                'rugby_league': '27',
                'aussie_rules': '27',
                'snooker': '28',
                'soccer': '29',
                'tennis': '33',
                'volleyball': '34',
            },
        },
        'BetOnline': {
            'base_url': 'http://example.com/site2',
            'headers': {'User-Agent': 'Site2-Agent'},
            'animal_endpoints': {
                'tiger': '105',
                'elephant': '212',
                'penguin': '045',
                # Add other mappings as needed
            },
        },
        'Fanduel': {
            'url_prefix': 'https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId=',
            'url_suffix': '&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York',
            'headers': {"authority": "sbapi.nj.sportsbook.fanduel.com","method": "GET","path": "/api/content-managed-page?page=SPORT&eventTypeId=7522&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York","scheme": "https","Accept": "application/json",
                        "Accept-Encoding": "gzip, deflate","Accept-Language": "en-US,en;q=0.9","If-None-Match": 'W/"c282f-bBffbN6JjwaBp0K5eHWIpZ6aNIM"',"Origin": "https://sportsbook.fanduel.com","Referer": "https://sportsbook.fanduel.com/",
                        "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',"Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "Windows","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                        "X-Px-Context": "_px3=1b81fe28d0fe345155fd68578079731def3ac1eb257c862f19c5d78dcad55821:5VU0ZGz3Dwcs3QbcK9/5m2YArWmdF7oSZHXyV1PRlz2Apyp+POSXu/sMnX2TK8KPvEeeSdxmUvh7cxJdFOmWBQ==:1000:2RSr8mRfl8B0vdK+KJ0RwvmwDFmsdIy+0CCXSBWPh0vtPxSDeUDExsMB+y0npqv9UC87PZEuUa6XfzspNWoGk6L11oJ42AtOSbhKIzzFfzzLZZXyJF3w3mQV/Auxt+A7kyCT2rnNcKdV7bViwq4VJ0ORr9XFeu+RR53vNk3AnKGGDK/b3ZRUhEAzZjl+tLTkVR6aDyXcN3ZpYa9cowVCDeZev/lATZZTsLcKmSVEcYg=;_pxvid=71fd10aa-835d-11ee-a9ec-53a9ad46d88b;pxcts=71fd229f-835d-11ee-a9ec-fced129a17e0;"
            },
            'sport_endpoints': {
                'baseball': '7511',
                'basketball': '7522',
                'boxing': '6',
                'cricket': '4',
                'cycling': '11',
                'darts': '3503',
                'football': '6423',
                'eventTypeId': '3',
                'handball': '468328',
                'hockey': '7524',
                'lacrosse': '28608997',
                'mma': '26420387',
                'motorspot': '8',
                'rugby_union': '5',
                'aussie_rules': '61420',
                'rugby_league': '1477',
                'snooker': '6422',
                'soccer': '1',
                'tennis': '2'
            },
        },
    }


def getLinkList(sportsbook, sport):
    startTime = time.time()
    pinnacle = getPinnacle(sport)
    fanduel = getFanduel(sport)
    merge = pd.merge(pinnacle, fanduel, on=['home','away'], how='inner')    

        
    merge = merge.dropna(subset=['Pinnacle', 'Fanduel'])

    # Get the columns that are not 'Name' or 'Location'
    idColumns = merge.drop(columns=['home', 'away'])
    #nt('bing')
    #print(idColumns)
    #linkList = merge[idColumns].values.flatten('F').tolist()    # flatten('F') means that it is flattened by columns, so the resulting list will be (Fanduel1, Fanduel2, Fanduel3, etc, Pinnacle 1, Pinnacle 2, etc) instead of alternating
    #print(idColumns)
    #print(linkList)

    prefixDict = {
        'Fanduel': ['https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId='],
        'Pinnacle': ['https://guest.api.arcadia.pinnacle.com/0.1/matchups/','https://guest.api.arcadia.pinnacle.com/0.1/matchups/'],
        'BetOnline': 'Z_Coordinate: {}',
    }

    suffixDict = {
        'Fanduel': [''],
        'Pinnacle': ['/markets/related/straight','/related'],
        'BetOnline': 'Z_Coordinate: {}',
    }

    columnSuffix = {
        'Fanduel': [''],
        'Pinnacle': ['Straight','Related'],
        'BetOnline': 'Z_Coordinate: {}',
    }
    # Maybe the best way to do it is to have a loop that loops through columns
    # Then checks the length of the suffixDict, loops through it, creating a new column
    # for each item in it, name of the item is f'{column} {columnSuffix[x]} Link'

    
    idColumns['Fanduel Link'] = prefixDict['Fanduel'] + idColumns['Fanduel'] + suffixDict['Fanduel']
    idColumns['PinnacleS Link'] = prefixDict['Pinnacle'][0] + idColumns['Pinnacle'] + suffixDict['Pinnacle'][0]
    idColumns['PinnacleR Link'] = prefixDict['Pinnacle'][1] + idColumns['Pinnacle'] + suffixDict['Pinnacle'][1]
    endTime = time.time()
    print(f'Generating links took {endTime - startTime} seconds')

    #print(idColumns)
    idColumns.to_csv('FetchEvents.csv')
    return idColumns

if __name__ == '__main__':
    getLinkList('a', 'baseball')

    #pinnacle = getPinnacle('football')

    #start = time.time()
    #fanduel = getFanduel('football')
    #end = time.time()
    #print(fanduel)
    #print(f'{end - start} to fetch links')

    #merge = pd.merge(pinnacle, fanduel, on=['home','away'], how='outer')

    # Deletes the ones where Pinnacle and Fanduel dont both cover them
    # This part of the code has issues as sometimes it will fuck it up
    # like if Pinnacle has Florida in NCAA as 'Florida Gators' and Fanduel
    # has them as 'Florida'

    #merge = merge.dropna(subset=['Pinnacle', 'Fanduel'])
    #merge.to_csv('FetchEvents.csv')