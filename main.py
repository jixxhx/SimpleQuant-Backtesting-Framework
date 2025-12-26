import matplotlib.pyplot as plt
from data_manager import get_stock_data
from strategy import MovingAverageStrategy

# ---------------- CONFIGURATION ----------------
TICKER = "SPY"          # ETF for S&P 500
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"
INITIAL_CAPITAL = 10000.0 # Starting cash in USD
# -----------------------------------------------

def run_backtest():
    # 1. Fetch Data
    df = get_stock_data(TICKER, START_DATE, END_DATE)
    if df is None: return

    # 2. Initialize and Run Strategy
    print(f"[INFO] Running Moving Average Strategy ({START_DATE} to {END_DATE})...")
    strategy = MovingAverageStrategy(short_window=50, long_window=200)
    result_df = strategy.run(df)

    # 3. Calculate Performance Metrics
    # Market Return: Buy & Hold strategy
    result_df['Market_Return'] = result_df['Close'].pct_change()
    
    # Strategy Return: Strategy Logic
    # We shift(1) to simulate trading at the next day's open based on today's close signal
    result_df['Strategy_Return'] = result_df['Market_Return'] * result_df['Signal'].shift(1)

    # Calculate Cumulative Returns (Equity Curve)
    result_df['Cumulative_Market'] = (1 + result_df['Market_Return']).cumprod() * INITIAL_CAPITAL
    result_df['Cumulative_Strategy'] = (1 + result_df['Strategy_Return']).cumprod() * INITIAL_CAPITAL

    # 4. Print Summary Stats
    final_market = result_df['Cumulative_Market'].iloc[-1]
    final_strategy = result_df['Cumulative_Strategy'].iloc[-1]
    
    print("-" * 50)
    print(f"Initial Capital      : ${INITIAL_CAPITAL:,.2f}")
    print(f"Market Return (B&H)  : ${final_market:,.2f}")
    print(f"Strategy Return      : ${final_strategy:,.2f}")
    print("-" * 50)

    # 5. Visualization (Plotting the Graph)
    plt.figure(figsize=(12, 6))
    plt.plot(result_df['Cumulative_Market'], label='Market (S&P 500)', color='gray', alpha=0.5)
    plt.plot(result_df['Cumulative_Strategy'], label='My Strategy (Golden Cross)', color='red', linewidth=2)
    
    plt.title(f"Backtest Analysis: {TICKER} (Moving Average Crossover)")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (USD)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    print("[INFO] Displaying performance graph...")
    plt.show()

if __name__ == "__main__":
    run_backtest()