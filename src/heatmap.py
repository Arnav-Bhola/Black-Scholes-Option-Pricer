import numpy as np
from .black_scholes import BlackScholes
from .enums import OptionType

class Heatmap():
    def __init__(self, strike_price, time_to_exp, risk_free_rate, min_stock_price, max_stock_price, min_volatility, max_volatility, option_type=OptionType.CALL_OPTION):
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.option_type = option_type
        self.min_stock_price = min_stock_price
        self.max_stock_price = max_stock_price
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.heatmap = np.zeros((10, 10))

    def generate_grid(self):
        # create evenly spaced stock prices and volatilities
        self.stock_prices = np.ceil(np.linspace(self.min_stock_price, self.max_stock_price, 10) * 100) / 100
        self.volatilities = np.ceil(np.linspace(self.min_volatility, self.max_volatility, 10) * 100) / 100
        return self.stock_prices, self.volatilities
    
    def compute_matrix(self):
        for i, vol in enumerate(self.volatilities):
            for j, s in enumerate(self.stock_prices):
                option = BlackScholes(s, self.strike_price, self.time_to_exp, self.risk_free_rate, vol, self.option_type)
                self.heatmap[i, j] = np.round(option.calculate_price(), 2)
        return self.heatmap
