import pandas as pd
import numpy as np
import json
import timeit

# Defining an event class with EventID, Sport, League, Name and Date/Time information
class Event:
    def __init__(self,item):
        self.id = item['eventId']
        (self.sport, self.league) = getLeague(item['competitionId'],item['eventTypeId'])
        self.name = item['name']
        time = item['openDate'].split('-')
        DD = time[2].split('T')
        Time = DD[1].split('.')
        self.date = time[0] +"-" + time[1] + "-" +DD[0] + "/" +Time[0]

def getLeague(competitionID, eventTypeID):
    match eventTypeID:
        # Baseball Cases
        case 7511:
            match competitionID:
                case 11196870:
                    return('Baseball','MLB')
                case 12365620:
                    return('Baseball','Triple-A')
                case 12290183:
                    return('Baseball','CPBL (China)')
                case 11085810:
                    return('Baseball','KBO League (Korea)')
                case 11085800:
                    return('Baseball','NPB (Japan)')
                case _:
                    return('Baseball','Could not find')
        # Hockey Cases
        case 7524:
            match competitionID:
                case 12300973:
                    return('Hockey','NHL')
                case 11082000:
                    return('Hockey','IIHF World Championship (Women)')
                case _:
                    return('Hockey','Could not find')
        case _:
            return('Could not find','Could not find')

def getConditions(df, sport):  
    if sport == 'baseball':
        runnerConditions = [
            df['marketType'] == 'TO_RECORD_2+_RBIS',
            df['marketType'] == 'TO_RECORD_2+_RUNS',
            df['marketType'] == 'ALTERNATE_RUN_LINES',
            df['marketType'] == 'ALTERNATE_TOTAL_RUNS',
            df['marketType'] == 'MONEY_LINE',
            df['marketType'] == 'TO_RECORD_A_STOLEN_BASE',
            df['marketType'] == 'PITCHER_C_STRIKEOUTS',
            df['marketType'] == '***OVER/UNDER_0.5_RUNS_1ST_INNINGS',
            df['marketType'] == '1ST_HALF_RUN_LINE',
            df['marketType'] == 'PITCHER_E_TOTAL_STRIKEOUTS',
            df['marketType'] == 'TO_HIT_A_HOME_RUN',
            df['marketType'] == 'PLAYER_TO_RECORD_3+_HITS',
            df['marketType'] == 'TOTAL_POINTS_(OVER/UNDER)',
            df['marketType'] == 'TO_HIT_2+_HOME_RUNS',
            df['marketType'] == '1ST_HALF_TOTAL_RUNS',
            df['marketType'] == 'PITCHER_D_STRIKEOUTS',
            df['marketType'] == 'MATCH_HANDICAP_(2-WAY)',
            
            df['marketType'] == 'PITCHER_C_TOTAL_STRIKEOUTS',
            df['marketType'] == 'PLAYER_TO_RECORD_A_HIT',
            df['marketType'] == 'PLAYER_TO_RECORD_2+_HITS',
            df['marketType'] == 'TO_RECORD_2+_TOTAL_BASES',
            df['marketType'] == 'TO_RECORD_3+_RBIS',
            df['marketType'] == 'HOME_TOTAL_RUNS',
            df['marketType'] == 'TO_RECORD_3+_TOTAL_BASES',
            df['marketType'] == 'TO_RECORD_A_RUN',
            df['marketType'] == '1ST_HALF_MONEY_LINE',
            df['marketType'] == 'AWAY_TOTAL_RUNS',
            df['marketType'] == 'TO_RECORD_AN_RBI',
            df['marketType'] == '1ST_INNING_RESULT',
            df['marketType'] == "PITCHER_A_OUTS_RECORDED",
            df['marketType'] == "PITCHER_B_OUTS_RECORDED"
        ]
        categoryResult = [
            'Player Props',
            'Player Props',
            'spread',
            'total',
            'moneyline',
            'Player Props',
            'Player Props',
            'rfi',              # Special condition for runs in first inning
            'spread',
            'Player Props',
            'Player Props',
            'Player Props',
            'total',
            'Player Props',
            'total',
            'Player Props',
            'spread',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'team_total',
            'Player Props',
            'Player Props',
            'firsthalfspread',           # Calling first half moneyline a spread because thats how it is on Pinnacle +-0 on spread
            'team_total',
            'Player Props',
            'moneyline',
            'Player Props',
            'Player Props'

        ]
        unitsResult = [
            'RBIs',
            'PlayerRuns',
            'Runs',
            'Runs',
            'moneyline',
            'StolenBases',
            'Strikeouts',
            'FirstInningRuns',
            'FirstHalfRuns',
            'Strikeouts',
            'HomeRuns',
            'Hits',
            'Runs',
            'HomeRuns',
            'FirstHalfRuns',
            'Strikeouts',
            'Runs',
            'Strikeouts',
            'Hits',             # Could also be O/U 0.5 bases
            'Hits',
            'TotalBases',
            'RBIs',
            'Runs',
            'TotalBases',
            'PlayerRuns',
            'spread',           # Calling first half moneyline a spread because thats how it is on Pinnacle +-0 on spread
            'Runs',
            'RBIs',
            'moneyline',
            'PitchingOuts',
            'PitchingOuts'
        ]
        sideResult = [
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                'home',
                '',
                '',
                '',           # Calling first half moneyline a  because thats how it is on Pinnacle +-0 on 
                'away',
                '',
                '',
                '',
                ''
        ]
        pointsConditions = [
                df['marketType'] == 'TO_RECORD_2+_RBIS',
                df['marketType'] == 'TO_RECORD_2+_RUNS',
                df['marketType'] == 'TO_RECORD_A_STOLEN_BASE',
                df['marketType'] == '***OVER/UNDER_0.5_RUNS_1ST_INNINGS',
                df['marketType'] == 'TO_HIT_A_HOME_RUN',
                df['marketType'] == 'PLAYER_TO_RECORD_3+_HITS',
                df['marketType'] == 'TO_HIT_2+_HOME_RUNS',
                df['marketType'] == 'PLAYER_TO_RECORD_A_HIT',
                df['marketType'] == 'PLAYER_TO_RECORD_2+_HITS',
                df['marketType'] == 'TO_RECORD_2+_TOTAL_BASES',
                df['marketType'] == 'TO_RECORD_3+_RBIS',
                df['marketType'] == 'TO_RECORD_3+_TOTAL_BASES',
                df['marketType'] == 'TO_RECORD_A_RUN',
                df['marketType'] == '1ST_HALF_MONEY_LINE',
                df['marketType'] == 'TO_RECORD_AN_RBI'
        ]
        pointsResult = [
                '1.5',
                '1.5',
                '0.5',
                '',  # This is YRFI/NRFI, could put 0.5 in here but the extractor kind of screws it up anyways, as long as shorthand is good should be fine
                '0.5',
                '2.5',
                '1.5',
                '0.5',             # Could also be O/U 0.5 bases
                '1.5',
                '1.5',
                '2.5',
                '2.5',
                '0.5',
                '0.0',           # Calling first half ml a spread because thats how it is on Pinnacle +-0 on spread
                '0.5'
        ]
        shorthandResult = [
                'pp;0;ou;rbi;',# + ppName,
                'pp;0;ou;run;',# + ppName,
                's;0;s;', # + line,
                's;0;ou;', # + line,
                's;0;m',
                'pp;0;ou;sb;',# + ppName,
                'pp;0;ou;k;',# + line + ';' + ppName,
                's;3;ou;0.5',# + line,
                's;1;s;',# + line,
                'pp;0;ou;k;',# + line +';'+ ppName,
                'pp;0;ou;hr;',# + ppName,
                'pp;0;ou;hit;',# + ppName,
                's;0;ou;',# + line,
                'pp;0;ou;hr;',# + ppName,
                's;1;ou;',# + line,
                'pp;0;ou;k;',# + line +';'+ ppName,
                's;0;s;',# + line,
                'pp;0;ou;k;',# + line +';'+ ppName,
                'pp;0;ou;hit;',# + ppName,
                'pp;0;ou;hit;',# + ppName,
                'pp;0;ou;tb;',# + ppName,
                'pp;0;ou;rbi;',# + ppName,
                's;0;tt;',# + home + ';home',
                'pp;0;ou;tb;',# + ppName,
                'pp;0;ou;run;',# + ppName,
                's;1;s;0.0',           # Calling first half moneyline a spread because thats how it is on Pinnacle +-0 on spread
                's;0;tt;',# + away + ';home',
                'pp;0;ou;rbi;',# + ppName,
                's;3;m',
                'pp;0;ou;po;',  
                'pp;0;ou;po;'
        ]
    
    elif sport == 'football':
        runnerConditions = [
            df['marketType'] == "ANY_TIME_TOUCHDOWN_SCORER",
            df['marketType'] == "TO_SCORE_2+_TOUCHDOWNS",
            df['marketType'] == "TO_SCORE_3+_TOUCHDOWNS",
            df['marketType'].str.contains('PASSING_YARDS'),
            df['marketType'].str.contains('RECEIVING'),
            df['marketType'].str.contains('RUSH'),
            df['marketType'].str.contains('PASSING_T'),
            df['marketType'].str.contains('INTERCEPTION'),

            df['marketType'] == 'MONEY_LINE',
            df['marketType'] == "ALTERNATE_HANDICAP",
            df['marketType'] == "ALTERNATE_TOTAL",
            df['marketType'] == "HOME_TOTAL_POINTS",
            df['marketType'] == "AWAY_TOTAL_POINTS",
            df['marketType'] == "TOTAL_TOUCHDOWNS_SCORED",
            df['marketType'] == "TOTAL_TOUCHDOWNS_-_AWAY_TEAM",
            df['marketType'] == "TOTAL_TOUCHDOWNS_-_HOME_TEAM",

            df['marketType'] == "HANDICAP_-_FIRST_HALF",
            df['marketType'] == "TOTAL_POINTS_-_FIRST_HALF",
            df['marketType'] == "1ST_HALF_WINNER_THREE_WAY",
            df['marketType'] == "HOME_TOTAL_POINTS_-_FIRST_HALF",
            df['marketType'] == "AWAY_TOTAL_POINTS_-_FIRST_HALF"

            #Could add first quarter props here
        ]
        categoryResult = [
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',

            'moneyline',
            'spread',
            'total',
            'team_total',
            'team_total',
            'total_tds',
            'team_total_tds',
            'team_total_tds',

            'spread',
            'total',
            'moneyline',
            'team_total',
            'team_total'
        ]
        unitsResult = [
            'Touchdowns',
            'Touchdowns',
            'Touchdowns',
            'PassingYards',
            'ReceivingYards',
            'RushingYards',
            'TouchdownPasses',
            'Interceptions',

            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            
            '',
            '',
            '',
            '',
            ''
        ] 
        sideResult = [
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',

                '',
                '',
                '',
                'home',
                'away',
                '',
                'away',
                'home',

                '',
                '',
                '',
                'home',
                'away'
            ]        
        pointsConditions = [
                df['marketType'] == "ANY_TIME_TOUCHDOWN_SCORER",
                df['marketType'] == "TO_SCORE_2+_TOUCHDOWNS",
                df['marketType'] == "TO_SCORE_3+_TOUCHDOWNS"
        ]
        pointsResult = [
                '0.5',
                '1.5',
                '2.5'
            ]      
        shorthandResult = [
                'pp;0;ou;td;',          #df['marketType'] == "ANY_TIME_TOUCHDOWN_SCORER",
                'pp;0;ou;td;',          #df['marketType'] == "TO_SCORE_2+_TOUCHDOWNS",
                'pp;0;ou;td;',          #df['marketType'] == "TO_SCORE_3+_TOUCHDOWNS",
                'pp;0;ou;passyds;',     #df['marketType'] == "PLAYER_A_-_ALT_PASSING_YARDS",
                'pp;0;ou;recyds;',      #df['marketType'] == "PLAYER_A_-_ALT_RECEIVING_YARDS",
                'pp;0;ou;rushyds;',     #df['marketType'] == "PLAYER_A_-_ALT_RUSH_YARDS",
                'pp;0;ou;passtds;',     #df['marketType'] == "PLAYER_A_-_ALT_PASSING_TDS",
                'pp;0;ou;passint;',     #df['marketType'] == "PLAYER_A_INTERCEPTION",

                's;0;m',                #df['marketType'] == 'MONEY_LINE',
                's;0;s;',               #df['marketType'] == "ALTERNATE_HANDICAP",
                's;0;ou;',              #df['marketType'] == "ALTERNATE_TOTAL",
                's;0;tt;',              #df['marketType'] == "HOME_TOTAL_POINTS",
                's;0;tt;',              #df['marketType'] == "AWAY_TOTAL_POINTS",
                's;0;td;',              #df['marketType'] == "TOTAL_TOUCHDOWNS_SCORED",
                's;0;ttd;',             #df['marketType'] == "TOTAL_TOUCHDOWNS_-_AWAY_TEAM",
                's;0;ttd;',             #df['marketType'] == "TOTAL_TOUCHDOWNS_-_HOME_TEAM",

                's;1;s;',               #df['marketType'] == "HANDICAP_-_FIRST_HALF",
                's;1;ou;',              #df['marketType'] == "TOTAL_POINTS_-_FIRST_HALF",
                's;1;m;3w',             #df['marketType'] == "1ST_HALF_WINNER_THREE_WAY",
                's;0;tt;',              #df['marketType'] == "HOME_TOTAL_POINTS_-_FIRST_HALF",
                's;0;tt;'               #df['marketType'] == "AWAY_TOTAL_POINTS_-_FIRST_HALF"
            ]
    
    elif sport == 'hockey':
        runnerConditions = [
            df['marketType'].str.contains("+_POINTS"),
            df['marketType'] == "PLAYER_X_POINTS_IH_SW",
            df['marketType'].str.contains("+_ASSISTS"),
            df['marketType'] == "PLAYER_X_ASSISTS_IH_SW",
            df['marketType'].str.contains("+_SHOTS"),
            df['marketType'] == "PLAYER_X_SHOTS_IH_SW",
            df['marketType'].str.contains("+_GOALS"),
            df['marketType'] == "ANY_TIME_GOAL_SCORER",
            df['marketType'] == "PLAYER_X_GOALS_IH_SW",
            df['marketType'].str.contains("+_POWERPLAY"),
            df['marketType'] == "PLAYER_X_POWERPLAY_POINTS_IH_SW",
            df['marketType'].str.contains("+_SAVES"),
            df['marketType'].str.contains("TOTAL_SAVES"),

            df['marketType'] == "MONEY_LINE",
            df['marketType'] == "MATCH_HANDICAP_(2-WAY)",
            df['marketType'] == "ALTERNATE_PUCK_LINE",
            df['marketType'] == "TOTAL_POINTS_(OVER/UNDER)",
            df['marketType'] == "ALTERNATE_TOTAL_GOALS",
            df['marketType'] == "TOTAL_GOALS_(FLAT_LINE)",
            df['marketType'] == "AWAY_TOTAL_GOALS",
            df['marketType'] == "HOME_TOTAL_GOALS",
            
            df['marketType'] == "FIRST_TO_5_SHOTS_ON_GOAL",
            df['marketType'] == "1ST_PERIOD_HANDICAP",
            df['marketType'] == "1ST_PERIOD_MONEY_LINE",
            df['marketType'] == "1ST_PERIOD_TOTAL_GOALS",
            df['marketType'] == "1ST_PERIOD_AWAY_TOTAL",
            df['marketType'] == "1ST_PERIOD_HOME_TOTAL",
            df['marketType'] == "GOAL_SCORED_IN_FIRST_FIVE_MINUTES_(00:00-04:59)",
            df['marketType'] == "GOAL_SCORED_IN_FIRST_TEN_MINUTES_(00:00-09:59)"

            # Could add regulation time markets if you want
        ]

        categoryResult = [
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',
            'Player Props',

            'moneyline',
            'spread',
            'spread',
            'total',
            'total',
            'total',
            'team_total',
            'team_total',

            'shots_on_goal',
            'spread',
            'moneyline',
            'team_total',
            'team_total',
            'goal_in_first_five',
            'goal_in_first_ten',
        ]

        unitsResult = [
            'Points',
            'Points',
            'Assists',
            'Assists',
            'ShotsOnGoal',
            'ShotsOnGoal',
            'Goals',
            'Goals',
            'Goals',
            'PowerPlayPoints',
            'PowerPlayPoints',
            'Saves',
            'Saves',

            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ]
    
        sideResult = [
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',

            '',
            '',
            '',
            '',
            '',
            '',
            'away',
            'home',
            
            '',
            '',
            '',
            '',
            'away',
            'home',
            '',
            ''
        ]
        
        pointsConditions = [
            df['marketType'].str.contains('1+'),
            df['marketType'].str.contains('2+'),
            df['marketType'].str.contains('3+'),
            df['marketType'].str.contains('4+'),
            df['marketType'].str.contains('5+'),
            df['marketType'].str.contains('6+')
        ]
        pointsResult = [
            '0.5',
            '1.5',
            '2.5',
            '3.5',
            '4.5',
            '5.5',
            ]
        
        shorthandResult = [
            'pp;0;ou;pts;',         #df['marketType'].str.contains("+_POINTS"),
            'pp;0;ou;pts;',         #df['marketType'] == "PLAYER_X_POINTS_IH_SW",
            'pp;0;ou;asst;',        #df['marketType'].str.contains("+_ASSISTS"),
            'pp;0;ou;asst;',        #df['marketType'] == "PLAYER_X_ASSISTS_IH_SW",
            'pp;0;ou;sog;',         #df['marketType'].str.contains("+_SHOTS"),
            'pp;0;ou;sog;',         #df['marketType'] == "PLAYER_X_SHOTS_IH_SW",
            'pp;0;ou;goals;',       #df['marketType'].str.contains("+_GOALS"),
            'pp;0;ou;goals;',       #df['marketType'] == "ANY_TIME_GOAL_SCORER",
            'pp;0;ou;goals;',       #df['marketType'] == "PLAYER_X_GOALS_IH_SW",
            'pp;0;ou;pppts;',       #df['marketType'].str.contains("+_POWERPLAY"),
            'pp;0;ou;pppts;',       #df['marketType'] == "PLAYER_X_POWERPLAY_POINTS_IH_SW",
            'pp;0;ou;saves;',       #df['marketType'].str.contains("+_SAVES"),
            'pp;0;ou;saves;',       #df['marketType'].str.contains("TOTAL_SAVES"),

            's;0;m',                #df['marketType'] == "MONEY_LINE"
            's;0;s;',               #df['marketType'] == "MATCH_HANDICAP_(2-WAY)",
            's;0;s;',               #df['marketType'] == "ALTERNATE_PUCK_LINE",
            's;0;ou;',              #df['marketType'] == "TOTAL_POINTS_(OVER/UNDER)",
            's;0;ou;',              #df['marketType'] == "ALTERNATE_TOTAL_GOALS",
            's;0;ou;',              #df['marketType'] == "TOTAL_GOALS_(FLAT_LINE)",
            's;0;tt;',              #df['marketType'] == "AWAY_TOTAL_GOALS",
            's;0;tt;',              #df['marketType'] == "HOME_TOTAL_GOALS",
            
            's;0;ftf;',             #df['marketType'] == "FIRST_TO_5_SHOTS_ON_GOAL",
            's;1;s;',               #df['marketType'] == "1ST_PERIOD_HANDICAP",
            's;1;m;',               #df['marketType'] == "1ST_PERIOD_MONEY_LINE",
            's;1;ou;',              #df['marketType'] == "1ST_PERIOD_TOTAL_GOALS",
            's;1;tt;',              #df['marketType'] == "1ST_PERIOD_AWAY_TOTAL",
            's;1;tt;',              #df['marketType'] == "1ST_PERIOD_HOME_TOTAL",
            's;0;giff;',            #df['marketType'] == "GOAL_SCORED_IN_FIRST_FIVE_MINUTES_(00:00-04:59)",
            's;0;gift;',            #df['marketType'] == "GOAL_SCORED_IN_FIRST_TEN_MINUTES_(00:00-09:59)"
        ]
    
    df['Category']= np.select(runnerConditions, categoryResult, default=pd.NA)    
    df['Units'] = np.select(runnerConditions, unitsResult, default=pd.NA)
    df['side'] = np.select(runnerConditions, sideResult, default=pd.NA)
    df['Points'] = np.select(pointsConditions, pointsResult, default=pd.NA)
    df['Shorthand'] = np.select(runnerConditions, shorthandResult, default=pd.NA)

    return df

def designationParsing(df, sport):
    if sport == 'baseball':
        runnerConditions = [
            df['result.type'].notna(),
            df['marketType'].str.contains('TO_'),
            df['marketType'].str.contains('STRIKEOUTS'),
            df['marketType'] == 'ALTERNATE_TOTAL_RUNS',
            df['marketType'] == '***OVER/UNDER_0.5_RUNS_1ST_INNINGS',
            df['marketType'] == '1ST_INNING_RESULT'
        ]

        designationResult = [
            df['result.type'], # df['result.type'].str[0].capitalize() + df['result.type'].str[1:] to remove capitalization in theory
            'Over',
            'Over',
            df['runnerName'].str.split().str[0],
            df['runnerName'],
            'First Inning Moneyline (Replace this later)' 
        ]
    elif sport == 'football':
        runnerConditions = [
            df['result.type'].notna(),
            df['marketType'].str.contains('ALT_'),
            df['marketType'].str.contains('TOUCHDOWN'),
            df['marketType'].str.contains('TO_')            # Should not be a used condition in football but there for consistency
        ]
        designationResult = [
            df['result.type'],
            'Over',
            'Over',
            'Over'
        ]

    df['Designation'] = np.select(runnerConditions, designationResult, default=pd.NA)
    df['Designation'] = df['Designation'].str.slice(0, 1).str.upper() + df['Designation'].str.slice(1).str.lower()
    return df 

def pointsConditions(df, sport):

    if sport == 'baseball':
        # Extracting appropriate points line from the dataframe
        conditions = [
            df['handicap'] != 0,                                            # If the handicap is not 0, that becomes points
            (df['Category'] == 'total') | (df['Category'] == 'spread'),     # If bet type is a total or spread we gotta remove parentheses or grab the spread [ex: Over (9.5) becomes '9.5', or Baltimore Orioles +2.5 becomes '2.5']
            ((df['Category'] == 'Player Props') & (df['Points'].isna()))      
        ]
        pointsResult = [
            df['handicap'],
            df['runnerName'].str.extract(r'([-+]?\d*\.\d+|\d+)').astype(str).squeeze(),
            df['runnerName'].str.extract(r'(\d+\.\d+|\d+)').astype(float).sub(0.5).squeeze()
        ]
        
    elif sport == 'football':
        # Extracting appropriate points line from the dataframe
        conditions = [
            df['handicap'] != 0,                                            # If the handicap is not 0, that becomes points
            (df['Category'] == 'total') | (df['Category'] == 'spread'),     # If bet type is a total or spread we gotta remove parentheses or grab the spread [ex: Over (9.5) becomes '9.5', or Baltimore Orioles +2.5 becomes '2.5']
            ((df['Category'] == 'Player Props') & (df['Units'] != 'Touchdowns'))
        ]

        # Debugging conditions
        #debug_choices = ['Condition 1', 'Condition 2', 'Condition 3']
        #df['debug'] = np.select(conditions, debug_choices)
        
        pointsResult = [
            df['handicap'],
            df['runnerName'].str.extract(r'([-+]?\d*\.\d+|\d+)').astype(str).squeeze(),
            df['runnerName'].str.extract(r'(\d+\.\d+|\d+)').astype(float).sub(0.5).squeeze()
        ]

    df['Points'] = np.select(conditions, pointsResult, default=df['Points'])
    return df 

def playerPropName(df, sport):
    if sport == 'baseball':
        # Selecting correct name for Player Prop
        condition = [
            df['Category'] != 'Player Props',
            df['Shorthand'] != 'pp;0;ou;k;',
            df['handicap'] != 0,
            df['handicap'] == 0
        ]
        #debug_choices = ['Condition 1', 'Condition 2', 'Condition 3', 'Condition 4']
        #df['debug'] = np.select(condition, debug_choices)
        choice = [
            ' ',
            df['runnerName'],
            df['runnerName'].str.split().str[:-1].apply(' '.join),
            df['runnerName'].str.split().str[:-2].apply(' '.join)
        ]
    elif sport == 'football':
        condition = [
            df['Category'] != 'Player Props',
            (df['handicap'] == 0) & (df['Units'] != 'Touchdowns'),
            df['handicap'] != 0,
            df['Units'] == 'Touchdowns'
        ]
        debug_choices = ['Condition 1', 'Condition 2', 'Condition 3','Condition 4']
        df['debug'] = np.select(condition, debug_choices)
        choice = [
            ' ',
            df['runnerName'].str.extract(r'^(.*?)(\d+)').iloc[:, 0].str.strip(),
            df['runnerName'].str.replace(r'\b(?:Over|Under)\b', '', regex=True).str.strip(),
            df['runnerName']
        ]
    #print(choice)
    ppColumn = np.select(condition, choice, default = pd.NA)
    return ppColumn

def generateKeys(df, sport):
    if (sport == 'baseball') | (sport == 'football'):
        conditions = [
            df['Category'] == 'Player Props',
            (df['Category'] == 'total') | (df['Category'] == 'spread'),
            (df['Category'] == 'moneyline') | (df['Shorthand'] == 's;3;ou;0.5') | (df['Category'] == 'firsthalfspread'),
            df['Category'] == 'team_total'
        ]
        choice = [
            df['Shorthand'] + df['Points'].astype(str),
            df['Shorthand'] + df['Points'].astype(str),
            df['Shorthand'],
            df['Shorthand'] + df['Points'].astype(str) + ';' + df['side']
        ]
    #debug_choices = ['Condition 1', 'Condition 2', 'Condition 3', 'Condition 4']
    #df['debug'] = np.select(conditions, debug_choices)
    keyColumn = np.select(conditions, choice)
    return keyColumn

def getOdds(df, sport):
    # Grabbing conditions to translate bet title to actual usable information to match up with Pinnacle result
    df = getConditions(df,sport)
    #df.to_csv('FanduelAfterConditions.csv')

    # Dropping unused bet types that are less likely to be +EV (such as 'Player to hit a Double')
    # If I want to add conditions do it here
    df.dropna(subset=['Category'], inplace=True)


    df = df.explode('runners')
    runner = pd.json_normalize(df['runners'])


    # Reset the row indices for both DataFrames
    df.reset_index(drop=True, inplace=True)
    runner.reset_index(drop=True, inplace=True)

    betInfo = pd.concat([df,runner],axis=1)

    betInfo = designationParsing(betInfo, 'football')

    betInfo = pointsConditions(betInfo, 'football')

    betInfo['Play Name'] = playerPropName(betInfo, 'football')

    betInfo['Key'] = generateKeys(betInfo, 'baseball')

    #print (timeit.timeit("playerPropName(betInfo, 'football')","from __main__ import playerPropName, betInfo",number=1))

    betInfo.to_csv('FanduelIntermediate.csv')
    columnsToKeep = ['Key', 'Designation', 'Play Name','winRunnerOdds.americanDisplayOdds.americanOdds'] # ['marketType','Key', 'Designation','Points', 'winRunnerOdds.americanDisplayOdds.americanOdds']
    betInfo = betInfo[columnsToKeep]
    betInfo.rename(columns={'winRunnerOdds.americanDisplayOdds.americanOdds': 'Fanduel Odds'}, inplace=True)
    betInfo['Designation'] = betInfo['Designation'].str.lower() 
    betInfo.to_csv('FanduelNFLTest.csv')
    return betInfo

if __name__ == '__main__':
    with open('C:\\Users\\alexf\\Desktop\\Sportsbook JSON\\NFL\\Fanduel.json') as json_file:
        data = json.load(json_file)

    eventData = data['attachments']['events']

    for key, value in eventData.items():
        print(key)  # This will print "32506145" 
        print(value)  # This will print the entire nested dictionary.
        print(value['name'])

    markets = data['attachments']['markets']

    # Here we convert the original json file to a more readable dataframe where each bet type is a row, example 'TO_RECORD_2+_HITS'
    df = pd.DataFrame.from_dict(markets, orient='index')

    betInfo = getOdds(df, 'football')

    print(betInfo)
    output_file_path = 'output.json'
    betInfo.to_json(output_file_path, orient='split', index=False)

    print("DataFrame successfully converted to JSON and saved to:", output_file_path)