import ccxt
import pandas as pd
import os

def fetch_num_candles(symbol: str, timeframe: int, num_candles: int,
                      local_mode: bool = False, local_copy: bool = False) -> pd.DataFrame:
    if local_mode:
        file_name = f"{timeframe}-{symbol}-data.parquet"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        return pd.read_parquet(file_path, engine="pyarrow")

    candles = []
    exchange = getattr(ccxt, 'bybit')()
    for x in range(num_candles, 0, -1000):
        since = exchange.milliseconds() - (x * timeframe * 60 * 1000)
        limitz = min(1000, x)
        d = exchange.fetch_ohlcv(symbol, timeframe, limit=limitz, since=since)
        candles.extend(d)

    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')

    if df.index.duplicated().any():
        df = df[~df.index.duplicated()]

    if local_copy:
        file_name = f"{timeframe}-{symbol}-data.parquet"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        df.to_parquet(file_path, engine="pyarrow", compression="snappy")

    return df
