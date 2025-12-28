import pandas as pd
import numpy as np

class MovingAverageStrategy:
    """
    Implements a trend-following momentum strategy based on dual moving average crossovers.
    Captures structural market shifts by filtering short-term noise against long-term trends.
    """
    def __init__(self, short_window=50, long_window=200):
        # Parameterization for sensitivity tuning (Fast vs. Slow lag)
        self.short_window = short_window
        self.long_window = long_window

    def run(self, df):
        # Enforce immutability to prevent side effects on the raw data pipeline
        data = df.copy()

        # --- Indicator Computation ---
        # Extracting trend signals by smoothing price volatility
        data['Short_MA'] = data['Close'].rolling(window=self.short_window).mean()
        data['Long_MA'] = data['Close'].rolling(window=self.long_window).mean()

        # --- Regime Identification ---
        # 1.0 indicates a bullish regime (Momentum > Trend), 0.0 indicates neutral/bearish
        data['Signal'] = 0.0
        # Logic: Bullish confirmation when short-term momentum overtakes the long-term baseline
        data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1.0

        # --- Execution Logic ---
        # Detecting signal state transitions (edges) to generate discrete trade orders
        # +1.0: Bullish Crossover (Entry), -1.0: Bearish Crossover (Exit)
        data['Position'] = data['Signal'].diff()

        return data
