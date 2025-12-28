import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start, end):
    """
    Interfaces with the Yahoo Finance API to fetch raw market data.
    Performs initial schema validation and normalization for downstream analysis.
    """
    print(f"[DATA_FEED] Initiating API request for {ticker}...")
    
    # --- External API Request ---
    # Fetching raw OHLCV time-series data without progress bars to maintain log cleanliness
    df = yf.download(ticker, start=start, end=end, progress=False)
    
    # --- Integrity Check ---
    # Validating payload emptiness to prevent propagation of null data errors
    if len(df) == 0:
        print("[SYSTEM_ERROR] Data fetch failed. Verify ticker symbol or connectivity.")
        return None

    # --- Schema Normalization ---
    # Critical Fix: Flattening MultiIndex columns (common in yfinance v0.2+) 
    # to ensure consistent access patterns across different library versions.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # --- Feature Selection ---
    # Retaining only core pricing and volume attributes required for technical analysis
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    print("[DATA_FEED] Ingestion complete. Pipeline ready.")

    return df
