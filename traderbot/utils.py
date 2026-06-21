def f1(m: float) -> float:
    return m if m >= 0 else 0

def f2(m: float) -> float:
    return 0 if m >= 0 else -m

def percent(n: float, d: float) -> float:
    return 100 * n / d if d != 0 else 0

def print_performance(win: int, loss: int, lookback_days: int) -> None:
    total = win + loss
    print("Win:", win, "Loss:", loss, "Total trades:", total)
    if total:
        print("Win rate:", round(win / total * 100, 2), "%",
              "Trades/day:", round(total / lookback_days, 2))
