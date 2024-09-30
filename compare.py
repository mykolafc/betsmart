import pandas as pd
import numpy as np
import requests


def calculate_ratio(row):
    odds = [row['BO dec_odds'], row['PB Decimal Odds'],
            row['DK Decimal Odds'], row['FD Decimal Odds'], row['PN Decimal Odds']]
    # Filter out None values
    valid_odds = [odd for odd in odds if pd.notnull(odd)]

    if len(valid_odds) < 2:
        # Return None or some default value if there are fewer than 2 valid odds
        return None

    max_odds = max(valid_odds)
    min_odds = min(valid_odds)
    # Handle division by zero
    ratio = (max_odds-1) / (min_odds-1) if min_odds != 1 else float('inf')
    return ratio


def calculate_fairOdds_ratio(row):
    # Extract the relevant odds, handling the case where BO dec_odds might be missing
    odds = [row['PB Decimal Odds'],
            row['FD Decimal Odds'], row['DK Decimal Odds']]

    # Add BO dec_odds only if it's not NaN
    if pd.notnull(row.get('BO dec_odds', None)):
        odds.append(row['BO dec_odds'])

    # Handle Pinnacle Fair Odds separately
    fair_odds_american = row['PN Fair Odds']

    # Filter out None or NaN values from the odds list
    valid_odds = [odd for odd in odds if pd.notnull(odd)]

    # If there are no valid odds or Pinnacle Fair Odds is NaN, return None
    if len(valid_odds) < 1 or pd.isnull(fair_odds_american):
        return None

    # Find the maximum odds from the valid odds
    max_odds = max(valid_odds)

    # Convert Pinnacle Fair Odds to decimal
    if fair_odds_american > 0:
        fair_decimal_odds = (fair_odds_american / 100) + 1
    else:
        fair_decimal_odds = (100 / abs(fair_odds_american)) + 1

    # Handle division by zero and calculate the profit ratio
    ratio = (max_odds - 1) / (fair_decimal_odds -
                              1) if fair_decimal_odds != 1 else float('inf')

    return ratio


def american_to_decimal(odds):
    if odds > 0:
        return odds / 100 + 1
    elif odds == 0:
        return 1
    else:
        return 100 / abs(odds) + 1


def calculate_arb(df):
    keys = np.where(df['Key'].isnull(), '', df['Key'].values)
    designations = np.where(df['Designation'].isnull(),
                            '', df['Designation'].values)
    sides = np.where(df['Side'].isnull(), '', df['Side'].values)
    names = np.where(df['Name'].isnull(), '', df['Name'].values)
    teams = np.where(df['Teams'].isnull(), '', df['Teams'].values)
    dates = np.where(df['Date'].isnull(), '', df['Date'].values)
    best_deals = np.where(df['Best Deal'].isnull(), 0, df['Best Deal'].values)

    arb = np.full(keys.shape, np.nan)

    for i in range(len(keys)):
        if designations[i].lower() == 'under':
            matching_rows = (
                (keys == keys[i]) &
                (designations == 'over') &
                (sides == sides[i]) &
                (names == names[i]) &
                (teams == teams[i]) &
                (dates == dates[i])
            )

            # Debugging output
            # print(f"Row {i}: Matching Rows: {matching_rows}")

            if np.any(matching_rows):
                j = np.where(matching_rows)[0][0]

                # Additional Debugging output
                # print(f"Matching Row for index {i} found at index {j}.")

                decimal_odds_team1 = american_to_decimal(best_deals[i])
                decimal_odds_team2 = american_to_decimal(best_deals[j])

                # Calculate implied probabilities
                implied_prob_team1 = 1 / decimal_odds_team1
                implied_prob_team2 = 1 / decimal_odds_team2

                # Calculate arbitrage percentage
                arbitrage_percentage = implied_prob_team1 + implied_prob_team2

                # Calculate ROI
                roi = (1 / arbitrage_percentage - 1) * 100
                arb[i] = arb[j] = roi

    return arb


def compareOdds(betOnline=True):
    # Read data from the first CSV file (PointsBet)
    df1 = pd.read_csv('./bin/PointsBetGigaDump.csv')

    # Conditionally read data from the BetOnline CSV file
    if betOnline:
        df2 = pd.read_csv('./bin/BetOnlineGigaDump.csv')

    # Read data from the third CSV file (DraftKings)
    df3 = pd.read_csv('./bin/DraftKingsGigaDump.csv')

    # Read data from FanDuel file
    df4 = pd.read_csv('./bin/FanDuelGigaDump.csv')

    # Read the Pinnacle file
    df5 = pd.read_csv('./bin/PinnacleGigaDump.csv')

    # Replace None values in 'Name' column with an empty string or a placeholder
    df1['Name'].fillna('', inplace=True)
    if betOnline:
        df2['Name'].fillna('', inplace=True)
    df3['Name'].fillna('', inplace=True)
    df4['Name'].fillna('', inplace=True)
    df5['Name'].fillna('', inplace=True)

    # Create a new dataframe to store the matching entries
    merged_df = pd.DataFrame()

    # Perform merging without BetOnline if betOnline is False
    if betOnline:
        merged_df = pd.merge(df1, df2, how='outer', on=[
            'Key', 'Designation', 'Side', 'Name', 'Teams', 'League', 'Date'], suffixes=('_df1', '_df2'))
    else:
        merged_df = df1.copy()  # Start with PointsBet data

    # Merge with DraftKings
    merged_df = pd.merge(merged_df, df3, how='outer', on=[
        'Key', 'Designation', 'Side', 'Name', 'Teams', 'League', 'Date'], suffixes=('_df1_df2', '_df3'))
    # Merge with FanDuel
    merged_df = pd.merge(merged_df, df4, how='outer', on=[
        'Key', 'Designation', 'Side', 'Name', 'Teams', 'League', 'Date'], suffixes=('', '_df4'))
    # Merge with Pinnacle
    merged_df = pd.merge(merged_df, df5, how='outer', on=[
        'Key', 'Designation', 'Side', 'Name', 'Teams', 'League', 'Date'], suffixes=('', '_df5'))

    # Calculate Fair Odds Ratio
    merged_df['Fair Odds Ratio'] = merged_df.apply(
        calculate_fairOdds_ratio, axis=1)

    # Conditionally include BetOnline odds in the comparison
    if betOnline:
        bo_odds = np.where(
            pd.isna(merged_df['BO Odds']), np.nan, merged_df['BO Odds'].values)
    else:
        bo_odds = np.nan  # If BetOnline is disabled, use NaN for BetOnline odds

    # Convert the DataFrame columns to NumPy arrays, replacing None with np.nan
    pb_odds = np.where(pd.isna(
        merged_df['PB American Odds']), np.nan, merged_df['PB American Odds'].values)
    dk_odds = np.where(pd.isna(
        merged_df['DK American Odds']), np.nan, merged_df['DK American Odds'].values)
    fd_odds = np.where(pd.isna(
        merged_df['FD American Odds']), np.nan, merged_df['FD American Odds'].values)
    pn_odds = np.where(pd.isna(
        merged_df['PN American Odds']), np.nan, merged_df['PN American Odds'].values)

    # Use np.nanmax to find the maximum value ignoring NaNs
    if betOnline:
        bo_odds = np.where(
            pd.isna(merged_df['BO Odds']), np.nan, merged_df['BO Odds'].values)
        # Include BO odds in the comparison
        best_deal = np.nanmax(
            [bo_odds, pb_odds, dk_odds, fd_odds, pn_odds], axis=0)
    else:
        # Exclude BO odds if betOnline is disabled
        best_deal = np.nanmax([pb_odds, dk_odds, fd_odds, pn_odds], axis=0)

    # Store the result in the dataframe
    merged_df['Best Deal'] = best_deal

    # Select the necessary columns, skipping BetOnline columns if betOnline=False
    columns_to_select = [
        'Key', 'Designation', 'Name', 'Date', 'Teams', 'League', 'Category', 'Side', 'Points',
        'PN Decimal Odds', 'PB Decimal Odds', 'DK Decimal Odds', 'FD Decimal Odds', 'PN American Odds',
        'PB American Odds', 'DK American Odds', 'FD American Odds', 'PN Fair Odds', 'Best Deal', 'Fair Odds Ratio'
    ]

    if betOnline:
        columns_to_select.insert(9, 'BO dec_odds')
        columns_to_select.insert(14, 'BO Odds')

    merged_df = merged_df[columns_to_select]

    # Calculate arb ROI% using the function `calculate_arb`
    merged_df['arb ROI%'] = calculate_arb(merged_df)

    return merged_df

    # requests.post('https://api.mynotifier.app', {
    #     "apiKey": '1539eb5f-8352-46f3-9d1b-193bc9d8f211',
    #     "message": "Arb Found",
    #     "description": "Go look at the csv file and find the > 2% arb",
    #     "type": "success",  # info, error, warning or success
    # })
