import pandas as pd
import numpy as np

# Read data from the first CSV file
df1 = pd.read_csv('./bin/PointsBetGigaDump.csv')

# Read data from the second CSV file
df2 = pd.read_csv('./bin/BetOnlineGigaDump.csv')

# Read data from the third CSV file
df3 = pd.read_csv('./bin/DraftKingsGigaDump.csv')


def calculate_ratio(row):
    odds = [row['BO dec_odds'], row['PB Decimal Odds'], row['DK Decimal Odds']]
    # Filter out None values
    valid_odds = [odd for odd in odds if pd.notnull(odd)]

    if len(valid_odds) < 2:
        # Return None or some default value if there are fewer than 2 valid odds
        return None

    max_odds = max(valid_odds)
    min_odds = min(valid_odds)
    # Handle division by zero
    ratio = (max_odds-1) / (min_odds-1) if min_odds != 0 else float('inf')
    return ratio


def average_and_furthest(row):
    # Calculate the average
    odds = [row['BO dec_odds'], row['PB Decimal Odds'], row['DK Decimal Odds']]
    avg = sum(odds) / 3

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
    return max([row['BO Odds'], row['PB American Odds'], row['DK American Odds']])


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

# Make names match before they get to this point


print(df1.columns)
print(df2.columns)
print(df3.columns)

# Create a new dataframe to store the matching entries
merged_df = pd.DataFrame()

merged_df = pd.merge(df1, df2, how='inner', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'])
merged_df = pd.merge(merged_df, df3, how='outer', on=[
                     'Key', 'Designation', 'Side', 'Name', 'Teams', 'Date'])
merged_df['Profits Ratio'] = merged_df.apply(
    calculate_ratio, axis=1)  # Calculate the odds ratio
merged_df['Best Deal'] = np.maximum.reduce(
    [merged_df['BO Odds'], merged_df['PB American Odds'], merged_df['DK American Odds']])


merged_df = merged_df.drop(['League_x', 'League_y', 'Category_x', 'Category_y',
                           'Points_x', 'Points_y'], axis=1)
merged_df = merged_df.reindex(columns=['Key', 'Designation', 'Name', 'Date', 'Teams', 'League', 'Category', 'Side', 'Points', 'BO dec_odds',
                              'PB Decimal Odds', 'DK Decimal Odds', 'BO Odds', 'PB American Odds', 'DK American Odds', 'Profits Ratio', 'Best Deal'])
merged_df['arb'] = np.nan
calculate_arbitrage(merged_df)

# best_arbitrage = find_best_arbitrage(merged_df)
# if best_arbitrage:
#     row, opp_row, arb_value = best_arbitrage
#     print(f"Best arbitrage found with value {arb_value}:")
#     print("Row 1:", row)
#     print("Row 2:", opp_row)
# else:
#     print("No arbitrage opportunities found.")


merged_df.to_csv('./bin/combined.csv', index=False)
