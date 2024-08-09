import FanDuel_Liam as fd
import grequests
import json

dataFD = fd.getData()
urlsFD = fd.makeRequestLinks(dataFD)
responsesGet = (grequests.get(u['url'], headers=u['headers']) for u in urlsFD)
responses = grequests.map(list(responsesGet))
fd.gigaDump2(responses)

# marketNames = []
# marketTypes = []

# with open('./Fanduel/FanDuelMLBGame.json', 'r') as file:
#     mlbGame = json.load(file)

# markets = mlbGame['attachments']['markets']
# for market in markets.values():
#     marketNames.append(market['marketName'])
#     marketTypes.append(market['marketType'])

# print(marketNames)
# print(marketTypes)

marketTypes = [
    "MONEY_LINE",
    "MATCH_HANDICAP_(2-WAY)",  # Run Line
    "TOTAL_POINTS_(OVER/UNDER)",  # Total runs
    "ALTERNATE_TOTAL_RUNS",
    "AWAY_TOTAL_RUNS",
    "AWAY_TEAM_ALTERNATE_TOTAL_RUNS",
    "HOME_TOTAL_RUNS",
    "HOME_TEAM_ALTERNATE_TOTAL_RUNS",

    "TO_HIT_A_HOME_RUN",
    "PLAYER_TO_RECORD_A_HIT",
    "PLAYER_TO_RECORD_2+_HITS",
    "PLAYER_TO_RECORD_3+_HITS",
    "TO_RECORD_A_STOLEN_BASE",
    "TO_RECORD_A_RUN",
    "TO_RECORD_2+_RUNS",
    "TO_RECORD_3+_RUNS",
    "TO_RECORD_AN_RBI",
    "TO_RECORD_2+_RBIS",
    "TO_RECORD_2+_TOTAL_BASES",
    "TO_RECORD_3+_TOTAL_BASES",
    "TO_RECORD_4+_TOTAL_BASES",
    "TO_RECORD_5+_TOTAL_BASES",
    "TO_HIT_A_SINGLE",
    "TO_HIT_A_DOUBLE",
    "TO_HIT_A_TRIPLE",
    # The letter after PITCHER is probably variable so might have to use regular expressions
    "PITCHER_C_STRIKEOUTS",
    "PITCHER_D_STRIKEOUTS",
    "PITCHER_C_TOTAL_STRIKEOUTS",
    "PITCHER_E_TOTAL_STRIKEOUTS"
]
