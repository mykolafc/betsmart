def calculate_raer(odds_list, num_bets=4):
    best_raer = 0
    best_odds = 0

    for odds in odds_list:
        probability = 1 / odds if odds > 1 else 0
        expected_return = (odds - 1) * 10  # Free bet profits
        p_at_least_one_hit = 1 - (1 - probability) ** num_bets
        raer = p_at_least_one_hit ** 2 * expected_return

        if raer > best_raer:
            best_raer = raer
            best_odds = odds

    best_raer = best_raer / (num_bets * 10)

    return best_odds, best_raer


odds_list = [2.0, 2.5, 3.0, 3.5, 4.0, 4.125, 4.25, 4.375, 4.38, 4.4, 4.5, 4.75, 5.0, 7.0, 8.0, 9.0, 10.0,
             12.0, 20.0, 50.0, 100.0, 10000.0]  # Add as many odds as you want
best_odds, best_raer = calculate_raer(odds_list, num_bets=10000)

print(f"The best odds are {best_odds} with a RAER of {best_raer:.2f}")
