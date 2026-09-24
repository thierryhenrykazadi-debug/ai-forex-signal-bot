from market_data import get_data
from strategy import analyze_market


SYMBOLS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "AUDUSD",
    "USDCAD",
    "NZDUSD",
    "XAUUSD",
]


def main():
    print("AI Forex Signal Bot starting...")
    print("-" * 50)

    for symbol in SYMBOLS:
        print(f"\nAnalyzing {symbol}...")

        data = get_data(symbol, interval="1h", period="60d")

        if data is None:
            print(f"{symbol}: No market data")
            continue

        result = analyze_market(data)

        print(
            f"{symbol}: {result['signal']} "
            f"(score: {result['score']})"
        )


if __name__ == "__main__":
    main()
