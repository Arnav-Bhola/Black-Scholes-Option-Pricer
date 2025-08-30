"""
Heatmap Generator for Black-Scholes Option Pricing

This module provides a class to generate a 2D matrix (heatmap) of option 
prices or profit/loss values across a range of stock prices and volatilities.
"""
import numpy as np
from .black_scholes import BlackScholes
from .enums import OptionType

class Heatmap():
    """
    Generates a heatmap of option prices or P&L using the Black-Scholes model.

    Attributes:
        strike_price (float): Strike/exercise price of the option.
        time_to_exp (float): Time to expiration (in years).
        risk_free_rate (float): Annual risk-free interest rate (as a decimal).
        option_type (OptionType): Either CALL_OPTION or PUT_OPTION.
        min_stock_price (float): Minimum stock price for grid.
        max_stock_price (float): Maximum stock price for grid.
        min_volatility (float): Minimum volatility value for grid.
        max_volatility (float): Maximum volatility value for grid.
        heatmap (ndarray): 10x10 numpy array storing computed results.
        isPNL (bool): If True, compute P&L relative to base_price.
        base_price (float): Reference price used for P&L calculations.
    """

    def __init__(self, strike_price, time_to_exp, risk_free_rate, min_stock_price, max_stock_price, min_volatility, max_volatility, option_type=OptionType.CALL_OPTION, pnl=False, base_price=0):
        """Initialize heatmap parameters and create empty result matrix."""
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.option_type = option_type
        self.min_stock_price = min_stock_price
        self.max_stock_price = max_stock_price
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.heatmap = np.zeros((10, 10))
        self.isPNL = pnl
        self.base_price = base_price

    def generate_grid(self):
        """
        Generate evenly spaced stock prices and volatilities.

        Returns:
            tuple (ndarray, ndarray): Arrays of stock prices and volatilities.
        """
        # Round to 2 decimals for cleaner display
        self.stock_prices = np.ceil(np.linspace(self.min_stock_price, self.max_stock_price, 10) * 100) / 100
        self.volatilities = np.ceil(np.linspace(self.min_volatility, self.max_volatility, 10) * 100) / 100
        return self.stock_prices, self.volatilities
    
    def compute_matrix(self):
        """
        Compute heatmap of option prices or P&L values.

        Returns:
            ndarray: 10x10 matrix of computed values.
        """
        for i, vol in enumerate(self.volatilities):
            for j, s in enumerate(self.stock_prices):
                option = BlackScholes(s, self.strike_price, self.time_to_exp, self.risk_free_rate, vol, self.option_type, self.base_price)
                if (self.isPNL):
                    # Profit/Loss relative to base price
                    self.heatmap[i, j] = np.round(option.base_price - option.calculate_price(), 2)
                else:
                    # Standard option price
                    self.heatmap[i, j] = np.round(option.calculate_price(), 2)
        return self.heatmap
