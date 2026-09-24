import pandas as pd
import ta


def analyze_market(df):
    if df is None or len(df) < 200:
        return {"signal": "NO SIGNAL", "score": 0}

    df = df.copy()

    df["ema20"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["Close"], window=50)
    df["ema200"] = ta.trend.ema_indicator(df["Close"], window=200)

    df["rsi"] = ta.momentum.rsi(df["Close"], window=14)

    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    last = df.iloc[-1]

    buy_score = 0
    sell_score = 0

    if last["Close"] > last["ema20"]:
        buy_score += 1
    else:
        sell_score += 1

    if last["ema20"] > last["ema50"]:
        buy_score += 1
    else:
        sell_score += 1

    if last["ema50"] > last["ema200"]:
        buy_score += 1
    else:
        sell_score += 1

    if last["rsi"] > 50:
        buy_score += 1
    elif last["rsi"] < 50:
        sell_score += 1

    if last["macd"] > last["macd_signal"]:
        buy_score += 1
    else:
        sell_score += 1

    if buy_score >= 4:
        signal = "BUY"
        score = buy_score
    elif sell_score >= 4:
        signal = "SELL"
        score = sell_score
    else:
        signal = "NO SIGNAL"
        score = max(buy_score, sell_score)

    return {
        "signal": signal,
        "score": score
    }
