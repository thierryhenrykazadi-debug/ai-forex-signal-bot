import pandas as pd
import ta


def analyze_market(df):
    """
    Analyse un timeframe.
    Retourne BUY, SELL ou NO SIGNAL.
    """

    if df is None or len(df) < 200:
        return {
            "signal": "NO SIGNAL",
            "score": 0,
            "entry": None,
            "stop_loss": None,
            "take_profit": None,
            "risk_reward": None,
            "reason": "Données insuffisantes"
        }

    df = df.copy()

    # Moyennes mobiles
    df["ema20"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["Close"], window=50)
    df["ema200"] = ta.trend.ema_indicator(df["Close"], window=200)

    # RSI
    df["rsi"] = ta.momentum.rsi(df["Close"], window=14)

    # MACD
    macd = ta.trend.MACD(df["Close"])
    df["macd_hist"] = macd.macd_diff()

    # ATR
    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["atr"] = atr.average_true_range()

    # Dernière bougie
    last = df.iloc[-1]
    previous = df.iloc[-2]

    close = float(last["Close"])
    ema20 = float(last["ema20"])
    ema50 = float(last["ema50"])
    ema200 = float(last["ema200"])
    rsi = float(last["rsi"])
    macd_hist = float(last["macd_hist"])
    atr_value = float(last["atr"])

    values = [
        close,
        ema20,
        ema50,
        ema200,
        rsi,
        macd_hist,
        atr_value
    ]

    if any(pd.isna(value) for value in values):
        return {
            "signal": "NO SIGNAL",
            "score": 0,
            "entry": None,
            "stop_loss": None,
            "take_profit": None,
            "risk_reward": None,
            "reason": "Indicateurs incomplets"
        }

    buy_score = 0
    sell_score = 0
    reasons = []

    # 1. Tendance
    if close > ema20 > ema50 > ema200:
        buy_score += 2
        reasons.append("trend bullish")

    elif close < ema20 < ema50 < ema200:
        sell_score += 2
        reasons.append("trend bearish")

    # 2. Prix vs EMA20
    if close > ema20:
        buy_score += 1

    elif close < ema20:
        sell_score += 1

    # 3. RSI
    if 52 <= rsi <= 68:
        buy_score += 1

    elif 32 <= rsi <= 48:
        sell_score += 1

    # 4. MACD
    if macd_hist > 0:
        buy_score += 1

    elif macd_hist < 0:
        sell_score += 1

    # 5. Momentum
    previous_close = float(previous["Close"])

    if close > previous_close:
        buy_score += 1

    elif close < previous_close:
        sell_score += 1

    score = max(buy_score, sell_score)

    signal = "NO SIGNAL"

    # Signal très strict
    if buy_score >= 5 and buy_score >= sell_score + 2:
        signal = "BUY"

    elif sell_score >= 5 and sell_score >= buy_score + 2:
        signal = "SELL"

    if signal == "NO SIGNAL":
        return {
            "signal": "NO SIGNAL",
            "score": score,
            "entry": None,
            "stop_loss": None,
            "take_profit": None,
            "risk_reward": None,
            "reason": "Configuration insuffisamment confirmée"
        }

    # Entry
    entry = close

    # Stop Loss / Take Profit basés sur ATR
    if signal == "BUY":
        stop_loss = entry - (1.2 * atr_value)
        take_profit = entry + (2.4 * atr_value)

    else:
        stop_loss = entry + (1.2 * atr_value)
        take_profit = entry - (2.4 * atr_value)

    return {
        "signal": signal,
        "score": score,
        "entry": round(entry, 5),
        "stop_loss": round(stop_loss, 5),
        "take_profit": round(take_profit, 5),
        "risk_reward": "1:2",
        "reason": ", ".join(reasons)
    }
