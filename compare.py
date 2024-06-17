import pandas as pd

# Read data from the first CSV file
df1 = pd.read_csv('./Pointsbet/PointsBetGigaDump.csv')

# Read data from the second CSV file
df2 = pd.read_csv('./BetOnline/nbaFinalizing.csv')

# Remove entries from df1 that don't have 'NBA' in the 'League' column
df1 = df1[df1['League'] == 'NBA']


#Make names match before they get to this point

print(df1.columns)
print(df2.columns)

# Create a new dataframe to store the matching entries
merged_df = pd.DataFrame()

merged_df = pd.merge(df1, df2, how='inner', left_on=['Key', 'Designation'], right_on=['Key', 'Designation'])
merged_df.to_csv('combined.csv', index=False)
