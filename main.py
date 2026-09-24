from market_data import get_multi_timeframe_data
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


def format_signal(symbol, analysis_4h, analysis_1h, analysis_15m):
    return f"""🚨 MULTI-TIMEFRAME FOREX SIGNAL

💱 Pair: {symbol}

🟣 4H — MAIN TREND
Signal: {analysis_4h["signal"]}
Score: {analysis_4h["score"]}/7

🔵 1H — CONFIRMATION
Signal: {analysis_1h["signal"]}
Score: {analysis_1h["score"]}/7

🟢 15M — ENTRY
Signal: {analysis_15m["signal"]}
Score: {analysis_15m["score"]}/7

💰 Entry: {analysis_15m["entry"]}
🛑 Stop Loss: {analysis_15m["stop_loss"]}
🎯 Take Profit: {analysis_15m["take_profit"]}
⚖️ Risk/Reward: {analysis_15m["risk_reward"]}

📊 Confirmation:
4H + 1H + 15M aligned

⚠️ Analysis and alert only.
No automatic trade execution.
"""


def main():
    print("Multi-Timeframe Forex Signal Bot starting...")
    print("-" * 60)

    signals_sent = 0

    for symbol in SYMBOLS:
        print(f"\nAnalyzing {symbol}...")

        data = get_multi_timeframe_data(symbol)

        if data is None:
            print(f"{symbol}: Market data unavailable")
            continue

        analysis_4h = analyze_market(data["4h"])
        analysis_1h = analyze_market(data["1h"])
        analysis_15m = analyze_market(data["15m"])

        print(
            f"{symbol} | "
            f"4H: {analysis_4h['signal']} | "
            f"1H: {analysis_1h['signal']} | "
            f"15M: {analysis_15m['signal']}"
        )

        # Les 3 timeframes doivent être parfaitement alignés
        aligned_buy = (
            analysis_4h["signal"] == "BUY"
            and analysis_1h["signal"] == "BUY"
            and analysis_15m["signal"] == "BUY"
        )

        aligned_sell = (
            analysis_4h["signal"] == "SELL"
            and analysis_1h["signal"] == "SELL"
            and analysis_15m["signal"] == "SELL"
        )

        if aligned_buy or aligned_sell:
            message = format_signal(
                symbol,
                analysis_4h,
                analysis_1h,
                analysis_15m
            )

            if send_telegram_message(message):
                print(f"{symbol}: Telegram signal sent.")
                signals_sent += 1
            else:
                print(f"{symbol}: Telegram sending failed.")

        else:
            print(f"{symbol}: NO SIGNAL — timeframes not aligned.")

    print("-" * 60)
    print(f"Signals sent: {signals_sent}")


if __name__ == "__main__":
    main()
