import pandas as pd
import numpy as np

class MovingAverageStrategy:
    """
    A simple Golden Cross strategy.
    Buys when Short MA crosses above Long MA.
    """
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def run(self, df):
        # Create a copy to avoid modifying the original data
        data = df.copy()

        # 1. Calculate Moving Averages (MA)
        data['Short_MA'] = data['Close'].rolling(window=self.short_window).mean()
        data['Long_MA'] = data['Close'].rolling(window=self.long_window).mean()

        # 2. Generate Signals (0 = Hold/Neutral, 1 = Buy/Long)
        data['Signal'] = 0.0
        # Condition: If Short MA > Long MA, set signal to 1 (Bullish)
        data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1.0

        # 3. Calculate Positions (Difference in signals indicates trade execution)
        # 1.0 = Buy Order, -1.0 = Sell Order
        data['Position'] = data['Signal'].diff()

        return data