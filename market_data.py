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

    return df.dropna()
