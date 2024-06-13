import json
import pandas as pd
import numpy as np
import time

home = 'Home'
away = 'Away'

def parseRelated(dataR):
    dataR = dataR.explode('participants')
    dataR = dataR.reset_index()
    dataR = dataR.drop('id', axis = 1)
    betInfo = pd.concat([dataR,pd.json_normalize(dataR['participants'])], axis=1) # Appending the participant information to the end of the dataframe
    
    return betInfo

def parseStraight(dataS,sport):
    dataS = dataS.explode('prices')
    dataS = dataS.reset_index()
    dataS = pd.concat([dataS, pd.json_normalize(dataS['prices'])], axis=1) # Appending the pricing information to the end of the dataframe

    dataS['points'] = dataS['points'].astype(str)

    dataS.to_csv('PinnacleIntermediateStep.csv')

    dataS['title'] = getTitle(dataS,sport,home,away)
    return dataS

def getTitle(dataS, sport, home, away):
    print(home+away)
    if 'participantId' in dataS:
        match sport:
            case "baseball":
                titleConditions = [
                dataS['participantId'].notnull(),
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'team_total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'team_total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'team_total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'team_total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away')
                ]
                titleChoices = [
                'Special Selection',
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Half Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Half Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Inning Total Runs',
                dataS['side'] + ' ' + dataS['designation'] + ' ' + dataS['points'] + ' Team Total',
                dataS['side'] + ' ' + dataS['designation'] + ' ' + dataS['points'] + ' First Half Team Total',
                dataS['side'] + ' ' + dataS['designation'] + ' ' + dataS['points'] + ' Second Half Team Total',
                dataS['side'] + ' ' + dataS['designation'] + ' ' + dataS['points'] + ' First Inning Team Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' First Half Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Half Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' First Inning Run Line',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Half Moneyline',
                dataS['designation'] + ' Second Half Moneyline',
                dataS['designation'] + ' First Inning Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Inning Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Inning Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case "hockey":
                titleConditions = [
                dataS['participantId'].notnull(),
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 6) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 6) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 6) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away'),
                ((dataS['period'] == 6) & dataS['side'] == 'home'),
                ((dataS['period'] == 6) & dataS['side'] == 'away'),
                ]
                titleChoices = [
                'Special Selection',
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Handicap',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Period Moneyline',
                dataS['designation'] + ' Second Period Moneyline',
                dataS['designation'] + ' Third Period Moneyline',
                dataS['designation'] + ' Regulation Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case "football":
                titleConditions = [
                dataS['participantId'].notnull(),
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 6) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 6) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 6) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away'),
                ((dataS['period'] == 6) & dataS['side'] == 'home'),
                ((dataS['period'] == 6) & dataS['side'] == 'away'),
                ]
                titleChoices = [
                'Special Selection',
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Handicap',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Period Moneyline',
                dataS['designation'] + ' Second Period Moneyline',
                dataS['designation'] + ' Third Period Moneyline',
                dataS['designation'] + ' Regulation Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case "basketball":
                titleConditions = [
                dataS['participantId'].notnull(),
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 6) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 6) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 6) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away'),
                ((dataS['period'] == 6) & dataS['side'] == 'home'),
                ((dataS['period'] == 6) & dataS['side'] == 'away'),
                ]
                titleChoices = [
                'Special Selection',
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Handicap',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Period Moneyline',
                dataS['designation'] + ' Second Period Moneyline',
                dataS['designation'] + ' Third Period Moneyline',
                dataS['designation'] + ' Regulation Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case _:
                titleConditions = []
                titleChoices = []
    else:
        match sport:
            case "Baseball":
                titleConditions = [
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away')
                ]
                titleChoices = [
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Half Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Half Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Inning Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' First Half Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Half Run Line',
                dataS['designation'] + ' ' + dataS['points'] + ' First Inning Run Line',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Half Moneyline',
                dataS['designation'] + ' Second Half Moneyline',
                dataS['designation'] + ' First Inning Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Half Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Inning Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Inning Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                ]
            case "Hockey":
                titleConditions = [
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 6) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 6) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 6) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away'),
                ((dataS['period'] == 6) & dataS['side'] == 'home'),
                ((dataS['period'] == 6) & dataS['side'] == 'away'),
                ]
                titleChoices = [
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Handicap',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Period Moneyline',
                dataS['designation'] + ' Second Period Moneyline',
                dataS['designation'] + ' Third Period Moneyline',
                dataS['designation'] + ' Regulation Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case "football":
                titleConditions = [
                ((dataS['period'] == 0) & (dataS['type'] == 'total')),
                ((dataS['period'] == 1) & (dataS['type'] == 'total')),
                ((dataS['period'] == 2) & (dataS['type'] == 'total')),
                ((dataS['period'] == 3) & (dataS['type'] == 'total')),
                ((dataS['period'] == 6) & (dataS['type'] == 'total')),
                ((dataS['period'] == 0) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 1) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 2) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 3) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 6) & (dataS['type'] == 'spread')),
                ((dataS['period'] == 0) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 1) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 2) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 3) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 6) & (dataS['type'] == 'moneyline')),
                ((dataS['period'] == 0) & dataS['side'] == 'home'),
                ((dataS['period'] == 0) & dataS['side'] == 'away'),
                ((dataS['period'] == 1) & dataS['side'] == 'home'),
                ((dataS['period'] == 1) & dataS['side'] == 'away'),
                ((dataS['period'] == 2) & dataS['side'] == 'home'),
                ((dataS['period'] == 2) & dataS['side'] == 'away'),
                ((dataS['period'] == 3) & dataS['side'] == 'home'),
                ((dataS['period'] == 3) & dataS['side'] == 'away'),
                ((dataS['period'] == 6) & dataS['side'] == 'home'),
                ((dataS['period'] == 6) & dataS['side'] == 'away'),
                ]
                titleChoices = [
                dataS['designation'] + ' ' + dataS['points'] + ' Total Runs',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Total', #Unclear if it exists
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Total',
                dataS['designation'] + ' ' + dataS['points'] + ' Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' First Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Second Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Third Period Handicap',
                dataS['designation'] + ' ' + dataS['points'] + ' Regulation Handicap',
                dataS['designation'] + ' Moneyline',
                dataS['designation'] + ' First Period Moneyline',
                dataS['designation'] + ' Second Period Moneyline',
                dataS['designation'] + ' Third Period Moneyline',
                dataS['designation'] + ' Regulation Moneyline',
                home + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' First Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Second Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Third Period Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                home + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points'],
                away + ' Regulation Team Total ' + dataS['designation'] + ' ' + dataS['points']
                ]
            case _:
                titleConditions = []
                titleChoices = []
    title = np.select(titleConditions,titleChoices, default = 'Error')
    return title

def getSpecialOdds(dataS, betInfo):
    dataRNew = betInfo[betInfo['id'].notnull()]
    dataRNew = dataRNew.reset_index()
    dataSNew = dataS[dataS['participantId'].notnull()]
    dataSNew = dataSNew.reset_index()
    
    # Merge dataRNew and dataSNew DataFrames on matching 'id' and 'participantId' columns
    merged_data = dataRNew.merge(dataSNew, left_on='id', right_on='participantId')

    # Create 'Odds' and 'Title' columns in betInfo
    betInfo['Price'] = merged_data['price']
    betInfo['Title'] = merged_data['title']
    return betInfo

def getSpecialInfo(df):
    df_special = pd.json_normalize(df['special'])
    df = pd.concat([df.drop(['special'], axis=1), df_special], axis=1)
    return df

def mergeBetInfo(betInfo,dataS, sport):

    dataRNew = betInfo[betInfo['id'].notnull()].reset_index()
    dataSNew = dataS[dataS['participantId'].notnull()].reset_index()
    dataRNew = dataRNew.merge(dataSNew[['participantId', 'price', 'title','points']], left_on='id', right_on='participantId', how='left')
    betInfo = dataRNew.rename(columns={'parentId':'GameId','points':'Points','price': 'Pinnacle Odds', 'title':'Title', 'category':'Category','name':'Designation','units':'Units'})

    #print(betInfo['participantId'])
    #print(dataS.columns)

    betInfo = betInfo[['Units','Designation','Category','Play Name','Pinnacle Odds','Points', 'GameId']]
    dataS = dataS[['matchupId','key','type','designation','title','side','price','points']]
    dataS = dataS.rename(columns={'matchupId':'GameId','key':'Key','price': 'Pinnacle Odds','type':'Category','designation':'Designation','points':'Points'})
    dataS = dataS[dataS['title'] != 'Special Selection']
    dataS = dataS.drop('title', axis=1)
    # Getting rid of non player prop special categories (such as "Correct Score" props and other options which are harder to gain an advantage in)
    betInfo = betInfo[betInfo['Category'] == 'Player Props']

    betInfo['Key'] = playerProp(betInfo, sport)
    betInfo['Designation'] = betInfo['Designation'].replace({'Yes': 'over', 'No': 'under'}, regex=True,)
    betInfo['Designation'] = betInfo['Designation'].str.lower()
    
    finalExport = pd.concat([dataS, betInfo])
    return finalExport

def playerProp(df, sport):
    if sport == 'baseball':
        playerPropConditions = [
            df['Units'] == 'TotalBases',
            df['Units'] == 'Strikeouts',
            df['Units'] == 'HitsAllowed',
            df['Units'] == 'EarnedRuns',
            df['Units'] == 'PitchingOuts',
            df['Units'] == 'HomeRuns'
        ]

        playerPropChoices = [
            'pp;0;ou;tb;'+ df['Points'] +';'+ df['Play Name'],      # Total bases
            'pp;0;ou;k;'+ df['Points'] +';'+ df['Play Name'],       # Strikeouts
            'pp;0;ou;ha;'+ df['Points'] +';'+ df['Play Name'],      # Hits Allowed (Pitcher)
            'pp;0;ou;er;'+ df['Points'] +';'+ df['Play Name'],      # Earned Runs
            'pp;0;ou;po;'+ df['Points'] +';'+ df['Play Name'],      # Pitching Outs
            'pp;0;ou;hr;'+ df['Points'] +';'+ df['Play Name']       # Home runs
        ]
    elif sport == 'football':
        playerPropConditions = [
            df['Units'] == 'PassingYards',
            df['Units'] == 'TouchdownPasses',
            df['Units'] == 'Interceptions',
            df['Units'] == 'LongestPassComplete',
            df['Units'] == 'Touchdowns',
            df['Units'] == 'ReceivingYards',
            df['Units'] == 'PassReceptions',
            df['Units'] == 'LongestReception',
            df['Units'] == 'RushingYards',
            df['Units'] ==  'PassAttempts',
            df['Units'] ==  'Completions',
            df['Units'] == 'KickingPoints'
        ]

        #playerPropChoices = [
        #    'pp;0;ou;passyds;'+ df['Points'] +';'+ df['Play Name'],     # Pass yards
        #    'pp;0;ou;passtds;'+ df['Points'] +';'+ df['Play Name'],     # Pass TDs
        #    'pp;0;ou;passint;'+ df['Points'] +';'+ df['Play Name'],     # Pass interceptions
        #    'pp;0;ou;lngpass;'+ df['Points'] +';'+ df['Play Name'],     # Longest pass complete
        #    'pp;0;ou;td;'+ df['Points'] +';'+ df['Play Name'],          # Anytime touchdown
        #    'pp;0;ou;recyds;'+ df['Points'] +';'+ df['Play Name'],      # Receiving yards
        #    'pp;0;ou;recpt;'+ df['Points'] +';'+ df['Play Name'],       # Receptions
        #    'pp;0;ou;lngrec;'+ df['Points'] +';'+ df['Play Name'],      # Longest reception
        #    'pp;0;ou;rushyds;'+ df['Points'] +';'+ df['Play Name'],     # Rushing yards
        #    'pp;0;ou;passatt;'+ df['Points'] +';'+ df['Play Name'],     # Passing attempts
        #    'pp;0;ou;passcomp;'+ df['Points'] +';'+ df['Play Name'],    # Completions
        #    'pp;0;ou;kickpts;'+ df['Points'] +';'+ df['Play Name']      # Kicking points
        #]
        playerPropChoices = [
            'pp;0;ou;passyds;'+ df['Points'],     # Pass yards
            'pp;0;ou;passtds;'+ df['Points'],     # Pass TDs
            'pp;0;ou;passint;'+ df['Points'],     # Pass interceptions
            'pp;0;ou;lngpass;'+ df['Points'],     # Longest pass complete
            'pp;0;ou;td;'+ df['Points'],          # Anytime touchdown
            'pp;0;ou;recyds;'+ df['Points'],      # Receiving yards
            'pp;0;ou;recpt;'+ df['Points'],       # Receptions
            'pp;0;ou;lngrec;'+ df['Points'],      # Longest reception
            'pp;0;ou;rushyds;'+ df['Points'],     # Rushing yards
            'pp;0;ou;passatt;'+ df['Points'],     # Passing attempts
            'pp;0;ou;passcomp;'+ df['Points'],    # Completions
            'pp;0;ou;kickpts;'+ df['Points']      # Kicking points
        ]

    elif sport == 'hockey':
        playerPropConditions = [
            df['Units'] == 'Points',
            df['Units'] == 'Assists',
            df['Units'] == 'Goals',
            df['Units'] == 'Saves',
            df['Units'] == 'ShotsOnGoal'
        ]
        playerPropChoices = [
            'pp;0;ou;pts;'+ df['Points'] +';'+ df['Play Name'],         # Pass yards
            'pp;0;ou;asst;'+ df['Points'] +';'+ df['Play Name'],        # Pass TDs
            'pp;0;ou;goals;'+ df['Points'] +';'+ df['Play Name'],       # Pass interceptions
            'pp;0;ou;saves;'+ df['Points'] +';'+ df['Play Name'],       # Longest pass complete
            'pp;0;ou;sog;'+ df['Points'] +';'+ df['Play Name'],         # Anytime touchdown
        ]
    elif sport == 'basketball':
        playerPropConditions = [
            df['Units'] == 'Points',
            df['Units'] == 'Assists',
            df['Units'] == 'ThreePointFieldGoals',
            df['Units'] == 'Rebounds',
            df['Units'] == 'PointsReboundsAssist',
            df['Units'] == 'DoubleDouble',
            df['Units'] == 'TripleDouble'
        ]
        playerPropChoices = [
            'pp;0;ou;pts;'+ df['Points'],           # Points
            'pp;0;ou;asst;'+ df['Points'],          # Assists
            'pp;0;ou;3pt;'+ df['Points'],           # Three Pointers Scored
            'pp;0;ou;reb;'+ df['Points'],           # Rebounds
            'pp;0;ou;pra;'+ df['Points'],           # Points+Rebounds+Assists
            'pp;0;ou;dbldbl;'+ df['Points'],        # To record a double double
            'pp;0;ou;trpltrpl;'+ df['Points']       # To record a triple triple
        ]
        print('yamudda')

    key = np.select(playerPropConditions,playerPropChoices, default = 'Undefined Bet')
    return key

def parseSpecial(betInfo, dataS):
    if 'participantId' in dataS:
        betInfo = getSpecialOdds(dataS, betInfo)
        betInfo = getSpecialInfo(betInfo)

    relatedColumns = ['type', 'units', 'category', 'description', 'name', 'id', 'Title', 'parentId']
    betInfo = betInfo[relatedColumns]
    betInfo['Play Name'] = betInfo['description'].str.extract(r'^(.*?)\s*\(')
    return betInfo

def getFairOdds(df):
    conditions = [
            df['Pinnacle Odds'] < 0, 
            df['Pinnacle Odds'] > 0
        ]

    choices = [
        (df['Pinnacle Odds'] / (df['Pinnacle Odds'] - 100)),
        (100/(df['Pinnacle Odds']+100))
        ]
    
    df['Percentage'] = np.select(conditions, choices, default=pd.NA)

    df['Play Name'] = df['Play Name'].fillna(' ')
    df['Vig'] = df.groupby(['Key', 'Play Name'])['Percentage'].transform('sum')
    df['Fair Percentage'] = df['Percentage']/df['Vig']

    conditions = [
            df['Fair Percentage'] < 0.5, 
            df['Fair Percentage'] >= 0.5
        ]

    choices = [
        (100 / df['Fair Percentage']) - 100,
        (100*df['Fair Percentage'])/(1-df['Fair Percentage'])*(-1)
        ]
    
    df['Pinnacle Fair Odds'] = np.select(conditions, choices)
    #df.drop(['Percentage', 'Fair Percentage', 'side'], axis = 1)


def getOdds(dataR, dataS, sport):
    start = time.time()

    betInfo = parseRelated(dataR)
    dataS = parseStraight(dataS, sport)
    betInfo = parseSpecial(betInfo, dataS)
    ## Trying to Merge Pricing Info
    finalExport = mergeBetInfo(betInfo, dataS, sport)
    getFairOdds(finalExport)

    end = time.time()
    finalExport.to_csv('PinnacleBaseballTest.csv')
    print(f"Runtime of the program is {end - start}")

    return finalExport

if __name__ == '__main__':
    relatedPath = 'C:\\Users\\alexf\\Desktop\\Sportsbook JSON\\NFL\\PinnacleRelated.json'    #Baseball\\PinnacleRelatedAug4.json'
    straightPath = 'C:\\Users\\alexf\\Desktop\\Sportsbook JSON\\NFL\\PinnacleStraight.json'   #Baseball\\PinnacleStraightAug4.json'

    with open(relatedPath) as json_file:
        dataRJson = json.load(json_file)

    dataR = pd.DataFrame(dataRJson)

    with open(straightPath) as json_file:
        dataSJson = json.load(json_file)

    dataS = pd.DataFrame(dataSJson)


    home = 'Home'
    away = 'Away'
    sport = 'football'

    getOdds(dataR, dataS, sport)





