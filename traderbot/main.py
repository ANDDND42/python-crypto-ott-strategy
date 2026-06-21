import pandas as pd
from traderbot.datafetcher import fetch_num_candles
from traderbot.strategy import run_strategy
from traderbot.utils import print_performance

SHOW_PLOT = True #True  # Toggle visuals on/off

# Config
SYMBOL = "BTCUSDT"
TIMEFRAME = 60
LOOKBACK_DAYS = 14
EMA_LENGTH = 200
RSI_LENGTH = 31
TP = 2.0
SL = 1.0
LEVERAGE = 20


def main():
    df = fetch_num_candles(
        symbol=SYMBOL,
        timeframe=TIMEFRAME,
        num_candles=int((1440 / TIMEFRAME) * LOOKBACK_DAYS + EMA_LENGTH),
        local_mode=False,
        local_copy=False,
    )
    results = run_strategy(
        df=df,
        ema_length=EMA_LENGTH,
        rsi_length=RSI_LENGTH,
        tp=TP,
        sl=SL,
        leverage=LEVERAGE,
        show_plot=SHOW_PLOT,
    )
    print_performance(results["win"], results["loss"], LOOKBACK_DAYS)


if __name__ == "__main__":
    main()
