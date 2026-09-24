import yfinance as yf


SYMBOLS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "USDCHF": "CHF=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X",
    "NZDUSD": "NZDUSD=X",
    "XAUUSD": "GC=F",
}


def get_data(symbol, interval="1h", period="60d"):
    ticker = SYMBOLS.get(symbol, symbol)

    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df is None or df.empty:
        return None

    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    required_columns = ["Open", "High", "Low", "Close"]

    for column in required_columns:
        if column not in df.columns:
            return None

    return df.dropna()


def get_multi_timeframe_data(symbol):
    """
    Récupère les données nécessaires au système multi-timeframe.

    15M = timing / entrée
    1H  = confirmation
    4H  = tendance principale
    """

    data_15m = get_data(
        symbol,
        interval="15m",
        period="60d"
    )

    data_1h = get_data(
        symbol,
        interval="1h",
        period="60d"
    )

    data_4h = get_data(
        symbol,
        interval="1h",
        period="60d"
    )

    if data_15m is None or data_1h is None or data_4h is None:
        return None

    # Création du 4H à partir des données 1H
    data_4h = data_4h.resample("4h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    return {
        "15m": data_15m,
        "1h": data_1h,
        "4h": data_4h
    }
