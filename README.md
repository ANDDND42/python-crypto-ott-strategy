# TraderBot

A backtesting and visualization tool for a custom **VIDYA + OTT crossover** trading strategy on cryptocurrency markets.

TraderBot fetches historical OHLCV candlestick data from Bybit (via [CCXT](https://github.com/ccxt/ccxt) — public market data, **no API key required**), backtests a VIDYA (Variable Index Dynamic Average) + OTT (Optimized Trend Tracker) crossover strategy with configurable risk settings, prints performance statistics, and can render an annotated candlestick chart of the signals.

> **Disclaimer:** This is a research and backtesting tool for studying a trading strategy on historical data. It is **not financial advice**, and backtested results do not predict future performance. Use at your own risk.

## Features

- Custom **VIDYA + OTT crossover** entry/exit logic
- Historical OHLCV data from **Bybit** via CCXT (public endpoints, no credentials)
- Optional **local caching** of candle data to Parquet (`local_mode` / `local_copy`) for fast, offline re-runs
- Configurable backtest: symbol, timeframe, lookback window, EMA/RSI lengths, take-profit, stop-loss, leverage
- **Performance summary**: wins, losses, total trades, win rate, and trades per day
- **Visual mode**: an annotated candlestick chart with the VIDYA and OTT lines plus buy/sell markers (matplotlib)

## Tech stack

Python · CCXT · pandas · numpy · pandas_ta · matplotlib · pyarrow

## Installation

```bash
git clone https://github.com/ANDDND42/python-crypto-ott-strategy.git
cd python-crypto-ott-strategy
pip install -r requirements.txt
```

## Usage

The run is configured with the constants at the top of `traderbot/main.py`:

```python
SHOW_PLOT     = True       # toggle the chart on/off
SYMBOL        = "BTCUSDT"
TIMEFRAME     = 60         # candle size in minutes
LOOKBACK_DAYS = 14
EMA_LENGTH    = 200
RSI_LENGTH    = 31
TP            = 2.0        # take-profit (%)
SL            = 1.0        # stop-loss (%)
LEVERAGE      = 20
```

Then run it as a module from the repository root:

```bash
python -m traderbot.main
```

The script downloads the required candles, runs the backtest, prints the performance summary, and (if `SHOW_PLOT` is `True`) opens the chart.

## Project structure

```
python-crypto-ott-strategy/
├── traderbot/
│   ├── main.py          # configuration + entry point
│   ├── datafetcher.py   # Bybit OHLCV fetching (CCXT) + optional Parquet caching
│   ├── strategy.py      # VIDYA + OTT crossover logic + plotting
│   ├── utils.py         # helper math + performance printout
│   └── __init__.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## License

See [LICENSE](LICENSE).