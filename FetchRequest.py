import requests
import json

# URL to send the request to
url = "https://sportsbook-tsb.ca-on.thescore.bet/graphql/persisted_queries/1628ec48be355f3d526a035d232bfa53cbb53121e5c40d99f674489762d39ce8?operationName=Marketplace&variables=%7B%22includeSectionDefaultField%22%3Atrue%2C%22includeDefaultChild%22%3Atrue%2C%22canonicalUrl%22%3A%22%2Fsport%2Ffootball%2Forganization%2Funited-states%2Fcompetition%2Fnfl%22%2C%22oddsFormat%22%3A%22AMERICAN%22%2C%22pageType%22%3A%22PAGE%22%2C%22includeRichEvent%22%3Atrue%2C%22includeMediaUrl%22%3Afalse%2C%22selectedFilterId%22%3A%22%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%221628ec48be355f3d526a035d232bfa53cbb53121e5c40d99f674489762d39ce8%22%7D%7D"

# Headers to include in the request
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'referer': 'https://thescore.bet/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'x-anonymous-authorization': 'Bearer eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkExMjhDQkMtSFMyNTYifQ.U94YujtTQDI1pKrelntcs5pLErM7ac8lCW62L8QKdGEXyc89s69P4qWo4iH8rgpcaOxoj-xWa2jInMLfAYuyxUktSdsARYSTBLzFPYYKhM9WXcrhlwhz-5GWJr1Gu6AWwtP8_9SwdvmgB2lyaU1bRMz69AYQNR8AAmRoR4c03IO7eZtV48yT3Zsf_NMEOqJ4pO5XEqunFFWGZ6zJ8dUr2Rn4tkMCcEEJ2wu5lsZP_zwcusGEGBj4-ItiXBlvm1_yJcDyS3nMd-zFki0JN1MBDJLEupVjJlV7pjetokYdj5COcqYnXFUQStWVJuUK5THFqU_b6-OgJJpYA9WaKby_trLs39_zwqhQPVZcfT7BPn6nS6CnHyAsOjoI98MaX-w25Zt_3Zx8AXT8jB2kpdTEbbOy9C9-OP_neUKs3DYlQ04yHn7ACkC_AKO4oUXz7g4Xm3iBiDy8H28PbM8G_G1OHENBtkcAjTXjXIZHgwQ2HRivVTKjqXfqPA7uQVVuGbXq7fZenkx-PGOUSK_UY-jjiez0WjS98au5KPIUj8PLeHPPV9D0dgYARvlfmH7gGRPBdGfqPvaYqvCbbwh7vmEvv_BTSwrguTNLxikGPgy1N9bY58R2Vbf45h1HOZzPkWugapedoi9-U1DyY82x9wKdhK1Mban4-6ZJpVadDuvgro8.OsSVwPMC63wbXbUiKTaa0w.JhKizANjKuqVoJJ35ks56j8WkPcjT-vZxlYmWZdHZioEAR8D06b3Puxjlnr6500s2qA45sW0TImSaHTMkREm-yEtp3yR_pQPUmtOD7k7b1zuVKNtBvFkg4koW45RVAfRHOih8gc0scYuJsp6GmjShM0JlcFgtADIw008WpSQKdiiRLf0bu_8OaDcqGKuhr2j7vq0IwKNEPEUQ2wrmGqKDeH-WEi-bD8z0g5SLs3P3KGDUG1arHafp4XGpIsc097QXnjvcxyZwpTdJ6IUd8WbeA.vxOp0P7NaesZIRKRAGsN6w',
    'x-app': 'tsb',
    'x-app-version': '24.17.1',
    'x-platform': 'web',
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Save the JSON data to a file
    with open('thescore_nfl_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved successfully to response_data.json")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
