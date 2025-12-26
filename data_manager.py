import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start, end):
    """
    Downloads historical stock data from Yahoo Finance.
    """
    print(f"[INFO] Downloading data for {ticker}...")
    
    # Download data
    df = yf.download(ticker, start=start, end=end, progress=False)
    
    if len(df) == 0:
        print("[ERROR] No data found. Please check the ticker symbol or date range.")
        return None

    # Handle MultiIndex columns (compatibility for newer yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Keep only necessary columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    print("[INFO] Download complete.")
    return df