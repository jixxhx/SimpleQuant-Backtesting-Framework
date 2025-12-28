import matplotlib.pyplot as plt
from data_manager import get_stock_data
from strategy import MovingAverageStrategy

# --- SIMULATION PARAMETERS ---
# Defining the backtest scope and initial capital constraints
TICKER = "SPY"          # Benchmark Instrument: S&P 500 ETF
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"
INITIAL_CAPITAL = 10000.0 # Base equity in USD

def run_backtest():
    # --- Data Ingestion Phase ---
    # Fetching historical OHLCV data to construct the simulation environment
    df = get_stock_data(TICKER, START_DATE, END_DATE)
    if df is None: return

    # --- Strategy Instantiation ---
    # Deploying the Moving Average Crossover logic (Trend Following)
    print(f"[SYSTEM] Initializing Backtest Engine for {TICKER} ({START_DATE} to {END_DATE})...")
    strategy = MovingAverageStrategy(short_window=50, long_window=200)
    result_df = strategy.run(df)

    # --- Performance Attribution & Equity Curve Construction ---
    
    # 1. Benchmark Calculation (Passive Buy & Hold)
    result_df['Market_Return'] = result_df['Close'].pct_change()
    
    # 2. Strategy Return Calculation
    # CRITICAL: Applying a 1-period lag (shift(1)) to align signal generation (Close T) 
    # with trade execution (Open T+1). This eliminates 'Look-ahead Bias'.
    result_df['Strategy_Return'] = result_df['Market_Return'] * result_df['Signal'].shift(1)

    # 3. Equity Curve Generation (Compounding Returns)
    result_df['Cumulative_Market'] = (1 + result_df['Market_Return']).cumprod() * INITIAL_CAPITAL
    result_df['Cumulative_Strategy'] = (1 + result_df['Strategy_Return']).cumprod() * INITIAL_CAPITAL

    # --- Statistical Summary ---
    # Extracting terminal values to compare active vs. passive performance
    final_market = result_df['Cumulative_Market'].iloc[-1]
    final_strategy = result_df['Cumulative_Strategy'].iloc[-1]
    
    print("-" * 50)
    print(f"Initial Equity       : ${INITIAL_CAPITAL:,.2f}")
    print(f"Benchmark (B&H)      : ${final_market:,.2f}")
    print(f"Active Strategy      : ${final_strategy:,.2f}")
    print("-" * 50)

    # --- Visual Analytics ---
    # Plotting equity curves to visualize volatility and alpha generation over time
    plt.figure(figsize=(12, 6))
    plt.plot(result_df['Cumulative_Market'], label='Benchmark (S&P 500)', color='gray', alpha=0.5)
    plt.plot(result_df['Cumulative_Strategy'], label='Active Strategy (Golden Cross)', color='red', linewidth=2)
    
    plt.title(f"Backtest Performance: {TICKER} (Trend Following Model)")
    plt.xlabel("Timeline")
    plt.ylabel("Equity Value (USD)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    print("[SYSTEM] Rendering performance visualization...")
    plt.show()

if __name__ == "__main__":
    run_backtest()
