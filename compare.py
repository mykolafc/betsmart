import pandas as pd

# Read data from the first CSV file
df1 = pd.read_csv('./bin/PointsBetGigaDump.csv')

# Read data from the second CSV file
df2 = pd.read_csv('./bin/BetOnlineGigaDump.csv')

# Read data from the third CSV file
df3 = pd.read_csv('./bin/DraftKingsGigaDump.csv')

def calculate_ratio(row):
    odds = [row['BO dec_odds'], row['PB Decimal Odds'], row['DK Decimal Odds']]
    max_odds = max(odds)
    min_odds = min(odds)
    ratio = max_odds / min_odds if min_odds != 0 else float('inf')  # Handle division by zero
    return ratio



#Make names match before they get to this point

print(df1.columns)
print(df2.columns)
print(df3.columns)

# Create a new dataframe to store the matching entries
merged_df = pd.DataFrame()

merged_df = pd.merge(df1, df2, how='inner', on=['Key', 'Designation', 'Name'])
merged_df = pd.merge(merged_df, df3, how='inner', on=['Key', 'Designation', 'Name'])
merged_df['Odds Ratio'] = merged_df.apply(calculate_ratio, axis=1) # Calculate the odds ratio

merged_df = merged_df.drop(['League_x', 'League_y', 'Category_x', 'Category_y', 'Side_x', 'Side_y', 'Points_x', 'Points_y', 'Teams_x', 'Teams_y'], axis=1)
merged_df = merged_df.reindex(columns=['Key', 'Designation', 'Name', 'Teams', 'League', 'Category', 'Side', 'Points', 'BO dec_odds', 'PB Decimal Odds', 'DK Decimal Odds', 'BO Odds', 'PB American Odds', 'DK American Odds', 'Odds Ratio'])



merged_df.to_csv('./bin/combined.csv', index=False)

