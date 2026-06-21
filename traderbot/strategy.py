import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas_ta as ta
from traderbot.utils import f1, f2, percent


def run_strategy(df: pd.DataFrame, ema_length: int, rsi_length: int, tp: float, sl: float,
                 leverage: int, show_plot: bool = True) -> dict:
    close = df['close']
    ema200 = df.ta.ema(length=ema_length)
    rsi = df.ta.rsi(length=rsi_length)

    tp_b, sl_b = 1 + (tp / 100), 1 - (sl / 100)
    tp_s, sl_s = 1 - (tp / 100), 1 + (sl / 100)

    signals_buy, signals_sell = [np.nan], [np.nan]
    signals_buy_open, signals_sell_open = {}, {}
    win = loss = 0
    pds = 2
    percent_val, alpha = 1.4, 2 / (pds + 1)
    vidya, ls_, ss_, dir_, ott_ = [0], [0], [0], [1], [0]
    m1_, m2_, sm1_, sm2_, cmo_, k_ = [0], [0], [0], [0], [0], [0]

    for i in range(1, len(close)):
        c, cp = close.iloc[i], close.iloc[i-1]
        momm = c - cp
        m1_.append(f1(momm))
        m2_.append(f2(momm))

        if i > 9:
            for ob, entry in list(signals_buy_open.items()):
                if entry * tp_b <= df['high'].iloc[i]:
                    win += 1; signals_buy_open.pop(ob)
                elif entry * sl_b >= df['low'].iloc[i]:
                    loss += 1; signals_buy_open.pop(ob)

            for ob, entry in list(signals_sell_open.items()):
                if entry * tp_s >= df['low'].iloc[i]:
                    win += 1; signals_sell_open.pop(ob)
                elif entry * sl_s <= df['high'].iloc[i]:
                    loss += 1; signals_sell_open.pop(ob)

            sm1, sm2 = sum(m1_[-9:]), sum(m2_[-9:])
            sm1_.append(sm1); sm2_.append(sm2)
            cmo = percent(sm1 - sm2, sm1 + sm2)
            cmo_.append(cmo); k = abs(cmo) / 100; k_.append(k)
            vidia = (alpha * k * c) + (1 - alpha * k) * vidya[-1]
            vidya.append(vidia)

            fark = vidia * percent_val * 0.01
            long_stop, short_stop = vidia - fark, vidia + fark
            long_stop_prev, short_stop_prev = ls_[-1], ss_[-1]
            ls_.append(max(long_stop, long_stop_prev) if vidia > long_stop_prev else long_stop)
            ss_.append(min(short_stop, short_stop_prev) if vidia < short_stop_prev else short_stop)

            dirN = dir_[-1]
            if dirN == -1 and vidia > short_stop_prev: dirN = 1
            elif dirN == 1 and vidia < long_stop_prev: dirN = -1
            dir_.append(dirN)

            mt = ls_[-1] if dirN == 1 else ss_[-1]
            ott = mt * (200 + percent_val) / 200 if vidia > mt else mt * (200 - percent_val) / 200
            ott_.append(ott)

            if i < ema_length:
                signals_sell.append(np.nan); signals_buy.append(np.nan)
            elif ott_[-3] > vidya[-1] and ott_[-4] < vidya[-2]:
                signals_buy.append(np.nan); signals_sell.append(c)
                signals_sell_open[df.index[i]] = c
            elif ott_[-3] < vidya[-1] and ott_[-4] > vidya[-2]:
                signals_sell.append(np.nan); signals_buy.append(c)
                signals_buy_open[df.index[i]] = c
            else:
                signals_sell.append(np.nan); signals_buy.append(np.nan)
        else:
            sm1_.append(0); sm2_.append(0); cmo_.append(0); k_.append(0)
            vidya.append(0); ott_.append(0); ls_.append(0); ss_.append(0)
            dir_.append(1); signals_sell.append(np.nan); signals_buy.append(np.nan)

    if show_plot:
        plot_results(df, ema200, vidya, ott_, signals_buy, signals_sell)

    return {"win": win, "loss": loss, "signals_buy": signals_buy, "signals_sell": signals_sell}


def plot_results(df: pd.DataFrame, ema200: pd.Series, vidya: list, ott_: list,
                 signals_buy: list, signals_sell: list) -> None:
    plt.rcParams['figure.figsize'] = (20, 8); plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(); ax.set_title('BTC Strategy Results')

    w = np.min(np.diff(mdates.date2num(df.index)))
    width, width2 = w * 0.8, w / 8; ax.set_xlim(df.index[200], df.index[-1])

    up, down = df[df.close >= df.open], df[df.close < df.open]
    ax.bar(up.index, up.close-up.open, width, bottom=up.open, color='green')
    ax.bar(up.index, up.high-up.close, width2, bottom=up.close, color='green')
    ax.bar(up.index, up.low-up.open, width2, bottom=up.open, color='green')
    ax.bar(down.index, down.close-down.open, width, bottom=down.open, color='red')
    ax.bar(down.index, down.high-down.open, width2, bottom=down.open, color='red')
    ax.bar(down.index, down.low-down.close, width2, bottom=down.close, color='red')

    vidya = pd.Series([np.nan if x == 0 else x for x in vidya])
    vidya[:200] = [np.nan]*200; ott_[:200] = [np.nan]*200
    ax.plot(df.index, vidya, label="VIDYA", color='blue', linewidth=1)
    ax.plot(df.index, [np.nan, np.nan]+ott_[:-2], label="OTT", color='purple', linewidth=2)
    ax.plot(df.index, signals_sell, marker='^', markersize=8, color='red', linewidth=0, label='SELL')
    ax.plot(df.index, signals_buy, marker='^', markersize=8, color='green', linewidth=0, label='BUY')

    plt.legend(loc='best'); plt.tight_layout(); plt.show()
