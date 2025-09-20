import csv
from itertools import combinations

BUDGET = 500
CSV_FILE = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"


def load_actions(csv_path):
    """
    Read the CSV file and return a clean list of actions.
    Each action is a dict: {"name": str, "cost": float, "profit": float}
    - profit is in euros (not a percent)
    """
    actions = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # skip header row

        for row in reader:
            name = row[0].strip()
            cost = float(row[1])

            # Convert percent "5%" -> 0.05
            percent_str = row[2].replace("%", "").strip()
            percent = float(percent_str) / 100.0

            # Calculate real profit in euros
            profit = cost * percent

            # Ignore useless data
            if cost <= 0 or profit <= 0:
                continue

            actions.append({"name": name, "cost": cost, "profit": profit})

    return actions


def total_cost_of(combo):
    """Compute the total cost of a combination using a loop."""
    total = 0.0
    for action in combo:
        total += action["cost"]
    return total


def total_profit_of(combo):
    """Compute the total profit of a combination using a loop."""
    total = 0.0
    for action in combo:
        total += action["profit"]
    return total


def best_portfolio_bruteforce(actions, budget=BUDGET):
    """
    Try all possible combinations (brute force) and keep the best one
    under the given budget. Returns (best_combo, best_cost, best_profit).
    """
    best_combo = []
    best_profit = 0.0
    best_cost = 0.0

    n = len(actions)

    for r in range(1, n + 1):
        for combo in combinations(actions, r):
            combo_cost = total_cost_of(combo)

            if combo_cost > budget:
                continue

            combo_profit = total_profit_of(combo)

            if combo_profit > best_profit:
                best_combo = list(combo)   # convert tuple -> list
                best_profit = combo_profit
                best_cost = combo_cost

    return best_combo, best_cost, best_profit


def main():
    actions = load_actions(CSV_FILE)
    best_combo, total_cost, total_profit = best_portfolio_bruteforce(actions, BUDGET)

    print("=== BEST PORTFOLIO (BRUTE FORCE) ===")
    print("Budget:", BUDGET, "€")
    print("Chosen actions:", [a["name"] for a in best_combo])
    print("Total cost:", round(total_cost, 2), "€")
    print("Total profit after 2 years:", round(total_profit, 2), "€")


if __name__ == "__main__":
    main()

