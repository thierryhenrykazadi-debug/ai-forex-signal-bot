import pandas as pd
import ta


def analyze_market(df):
    """
    Analyse technique stricte.
    Retourne BUY, SELL ou NO SIGNAL.
    Aucun ordre n'est exécuté automatiquement.
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

    # Indicateurs
    df["ema20"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["Close"], window=50)
    df["ema200"] = ta.trend.ema_indicator(df["Close"], window=200)

    df["rsi"] = ta.momentum.rsi(df["Close"], window=14)

    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    atr = ta.volatility.AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["atr"] = atr.average_true_range()

    # Dernière bougie
    last = df.iloc[-1]

    close = float(last["Close"])
    ema20 = float(last["ema20"])
    ema50 = float(last["ema50"])
    ema200 = float(last["ema200"])
    rsi = float(last["rsi"])
    macd_hist = float(last["macd_hist"])
    atr_value = float(last["atr"])

    if any(pd.isna(x) for x in [
        close,
        ema20,
        ema50,
        ema200,
        rsi,
        macd_hist,
        atr_value
    ]):
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

    # 1. Tendance principale
    if close > ema20 > ema50 > ema200:
        buy_score += 2
        reasons.append("tendance haussière")

    elif close < ema20 < ema50 < ema200:
        sell_score += 2
        reasons.append("tendance baissière")

    # 2. Position du prix
    if close > ema20:
        buy_score += 1

    elif close < ema20:
        sell_score += 1

    # 3. RSI
    if 52 <= rsi <= 68:
        buy_score += 1
        reasons.append("RSI favorable aux acheteurs")

    elif 32 <= rsi <= 48:
        sell_score += 1
        reasons.append("RSI favorable aux vendeurs")

    # 4. MACD
    if macd_hist > 0:
        buy_score += 1

    elif macd_hist < 0:
        sell_score += 1

    # 5. Momentum de la dernière bougie
    previous_close = float(df["Close"].iloc[-2])

    if close > previous_close:
        buy_score += 1

    elif close < previous_close:
        sell_score += 1

    # Décision stricte
    signal = "NO SIGNAL"
    score = max(buy_score, sell_score)

    if buy_score >= 5 and buy_score >= sell_score + 2:
        signal = "BUY"

    elif sell_score >= 5 and sell_score >= buy_score + 2:
        signal = "SELL"

    # Pas de signal si le marché est contradictoire
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

    # Gestion du risque basée sur ATR
    entry = close

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
