import pandas as pd

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
    ratio = max_odds / min_odds if min_odds != 0 else float('inf')
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


# Make names match before they get to this point

print(df1.columns)
print(df2.columns)
print(df3.columns)

# Create a new dataframe to store the matching entries
merged_df = pd.DataFrame()

merged_df = pd.merge(df1, df2, how='inner', on=[
                     'Key', 'Designation', 'Name', 'Teams'])
merged_df = pd.merge(merged_df, df3, how='inner', on=[
                     'Key', 'Designation', 'Name', 'Teams'])
merged_df['Odds Ratio'] = merged_df.apply(
    calculate_ratio, axis=1)  # Calculate the odds ratio
merged_df['Best Deal'] = merged_df.apply(
    average_and_furthest, axis=1)  # Calculate the best deal

merged_df = merged_df.drop(['League_x', 'League_y', 'Category_x', 'Category_y',
                           'Side_x', 'Side_y', 'Points_x', 'Points_y'], axis=1)
merged_df = merged_df.reindex(columns=['Key', 'Designation', 'Name', 'Teams', 'League', 'Category', 'Side', 'Points', 'BO dec_odds',
                              'PB Decimal Odds', 'DK Decimal Odds', 'BO Odds', 'PB American Odds', 'DK American Odds', 'Odds Ratio', 'Best Deal'])


merged_df.to_csv('./bin/combined.csv', index=False)
