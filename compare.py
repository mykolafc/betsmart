import pandas as pd
import numpy as np

# Read data from the first CSV file
df1 = pd.read_csv('./bin/PointsBetGigaDump.csv')

# Read data from the second CSV file
df2 = pd.read_csv('./bin/BetOnlineGigaDump.csv')

# Read data from the third CSV file
df3 = pd.read_csv('./bin/DraftKingsGigaDump.csv')

# Read data from FanDuel file
df4 = pd.read_csv('./bin/FanDuelGigaDump.csv')

# Read the pinnacle file
df5 = pd.read_csv('./bin/PinnacleGigaDump.csv')


def calculate_ratio(row):
    odds = [row['BO dec_odds'], row['PB Decimal Odds'],
            row['DK Decimal Odds'], row['FD Decimal Odds']]
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


# THIS NEEDS FIXING
def average_and_furthest(row):
    # Calculate the average
    odds = [row['BO dec_odds'], row['PB Decimal Odds'],
            row['DK Decimal Odds'], row['FD American Odds'], row['PN American Odds']]
    avg = sum(odds) / 5

    # Calculate the absolute differences from the average
    diffs = [abs(odds[0] - avg), abs(odds[1] - avg), abs(odds[2] - avg)]

    # Find the index of the maximum difference
    max_diff_index = diffs.index(max(diffs))

    if max_diff_index == 0:
        return 'BetOnline'
    elif max_diff_index == 1:
        return 'PointsBet'
    else:
        return 'DraftKings'


def highest_odd(row):
    return max([row['BO Odds'], row['PB American Odds'], row['DK American Odds'], row['FD American Odds'], row['PN American Odds']])


# Function to calculate the arbitrage and update the 'arb' column
def calculate_arbitrage(df):
    for index, row in df.iterrows():
        if row['Designation'] in ['over', 'under']:
            opposite_designation = 'under' if row['Designation'] == 'over' else 'over'
            # Find the matching row with the opposite designation
            match = df[
                (df['Key'] == row['Key']) &
                (df['Name'] == row['Name']) &
                (df['Teams'] == row['Teams']) &
                (df['League'] == row['League']) &
                (df['Designation'] == opposite_designation)
            ]
            if not match.empty:
                match_index = match.index[0]
                match_best_deal = match['Best Deal'].values[0]
                arb_value = row['Best Deal'] + match_best_deal
                # Update the 'arb' column for both rows
                df.at[index, 'arb'] = arb_value
                df.at[match_index, 'arb'] = arb_value


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

                arb[i] = best_deals[i] + best_deals[j]
                arb[j] = arb[i]

    return arb


# Replace None values in 'Name' column with an empty string or a placeholder
df1['Name'].fillna('', inplace=True)
df2['Name'].fillna('', inplace=True)
df3['Name'].fillna('', inplace=True)
df4['Name'].fillna('', inplace=True)
df5['Name'].fillna('', inplace=True)

# print(df1.columns)
# print(df2.columns)
# print(df3.columns)

# Create a new dataframe to store the matching entries
merged_df = pd.DataFrame()

# Theres a problem with the merging, I think its because if the keys are None, it merges anyways
merged_df = pd.merge(df1, df2, how='outer', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'], suffixes=('_df1', '_df2'))
merged_df = pd.merge(merged_df, df3, how='outer', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'], suffixes=('_df1_df2', '_df3'))
merged_df = pd.merge(merged_df, df4, how='outer', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'], suffixes=('', '_df4'))
merged_df = pd.merge(merged_df, df5, how='outer', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'], suffixes=('', '_df5'))

merged_df['Profits Ratio'] = merged_df.apply(
    calculate_ratio, axis=1)  # Calculate the odds ratio
# Convert the DataFrame columns to NumPy arrays, replacing None with np.nan
bo_odds = np.where(
    pd.isna(merged_df['BO Odds']), np.nan, merged_df['BO Odds'].values)
pb_odds = np.where(pd.isna(
    merged_df['PB American Odds']), np.nan, merged_df['PB American Odds'].values)
dk_odds = np.where(pd.isna(
    merged_df['DK American Odds']), np.nan, merged_df['DK American Odds'].values)
fd_odds = np.where(pd.isna(
    merged_df['FD American Odds']), np.nan, merged_df['FD American Odds'].values)
pn_odds = np.where(pd.isna(
    merged_df['PN American Odds']), np.nan, merged_df['PN American Odds'].values)

# Use np.nanmax to find the maximum value ignoring NaNs
merged_df['Best Deal'] = np.nanmax(
    [bo_odds, pb_odds, dk_odds, fd_odds, pn_odds], axis=0)

merged_df = merged_df[['Key', 'Designation', 'Name', 'Date', 'Teams', 'League', 'Category', 'Side', 'Points', 'BO dec_odds', 'PN Decimal Odds',
                       'PB Decimal Odds', 'DK Decimal Odds', 'FD Decimal Odds', 'BO Odds', 'PN American Odds', 'PB American Odds',
                       'DK American Odds', 'FD American Odds', 'PN Fair Odds', 'Profits Ratio', 'Best Deal']]

merged_df['arb'] = calculate_arb(merged_df)

# best_arbitrage = find_best_arbitrage(merged_df)
# if best_arbitrage:
#     row, opp_row, arb_value = best_arbitrage
#     print(f"Best arbitrage found with value {arb_value}:")
#     print("Row 1:", row)
#     print("Row 2:", opp_row)
# else:
#     print("No arbitrage opportunities found.")


merged_df.to_csv('./bin/combined.csv', index=False)
