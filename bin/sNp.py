yearlyDeposit = 7000
years = 58
total = 35000
for year in range(years):
    if year <= 34:
        total += yearlyDeposit
        total = round(total * 1.07, 2)
        if year % 2 == 0:
            yearlyDeposit += 500
    else:
        total = round(total * 1.05, 2)
print(total)
