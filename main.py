from market_data import get_data
from strategy import analyze_market
from telegram_bot import send_telegram_message


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


def format_signal(symbol, result):
    return f"""🚨 FOREX SIGNAL

📊 Pair: {symbol}
📌 Signal: {result['signal']}
⭐ Score: {result['score']}/7

💰 Entry: {result['entry']}
🛑 Stop Loss: {result['stop_loss']}
🎯 Take Profit: {result['take_profit']}
⚖️ Risk/Reward: {result['risk_reward']}

📈 Reason:
{result['reason']}

⚠️ Analysis only — no automatic trade execution.
"""


def main():
    print("AI Forex Signal Bot starting...")
    print("-" * 50)

    signals_sent = 0

    for symbol in SYMBOLS:
        print(f"\nAnalyzing {symbol}...")

        data = get_data(
            symbol,
            interval="1h",
            period="60d"
        )

        if data is None:
            print(f"{symbol}: No market data")
            continue

        result = analyze_market(data)

        print(
            f"{symbol}: {result['signal']} "
            f"(score: {result['score']})"
        )

        if result["signal"] in ["BUY", "SELL"]:
            message = format_signal(symbol, result)

            if send_telegram_message(message):
                print(f"{symbol}: Telegram signal sent.")
                signals_sent += 1
            else:
                print(f"{symbol}: Telegram signal failed.")


    print("-" * 50)
    print(f"Signals sent: {signals_sent}")


if __name__ == "__main__":
    main()
