"""
Black-Scholes Option Pricing Model

This module provides a class to calculate the price of European call/put options 
and their Greeks (Delta, Gamma, Vega, Theta, Rho) using the Black-Scholes formula.
"""

import math
from scipy.stats import norm
import numpy as np
from .enums import OptionType

class BlackScholes():
    """
    Black-Scholes option pricer.

    Attributes:
        stock_price (float): Current price of the underlying stock.
        strike_price (float): Strike/exercise price of the option.
        time_to_exp (float): Time to expiration (in years).
        risk_free_rate (float): Annual risk-free interest rate (as a decimal).
        volatility (float): Annual volatility of the underlying stock (σ).
        option_type (OptionType): Either CALL_OPTION or PUT_OPTION.
        base_price (float): Reference price for P&L calculations (optional).
        d1 (float | None): Intermediate value used in calculations.
        d2 (float | None): Intermediate value used in calculations.
    """
    def __init__(self, stock_price, strike_price, time_to_exp, risk_free_rate, volatility, option_type=OptionType.CALL_OPTION, base_price=0):
        """Initialize the option parameters."""
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.option_type = option_type
        self.base_price = base_price
        self.d1 = None

    def calculate_d1(self):
        """
        Compute d1, an intermediate term in the Black-Scholes model.

        Returns:
            float: The computed d1 value.
        """
        self.d1 = (math.log(self.stock_price / self.strike_price) + self.time_to_exp * (self.risk_free_rate + ((self.volatility ** 2) / 2))) / (self.volatility * (self.time_to_exp ** 0.5))
        return self.d1
    
    def calculate_d2(self):
        """
        Compute d2, an intermediate term in the Black-Scholes model.

        Returns:
            float: The computed d2 value.
        """
        self.d2 = self.d1 - (self.volatility * (self.time_to_exp ** 0.5))
        return self.d2
    
    def calculate_delta(self):
        """
        Compute Delta, sensitivity of option price to underlying stock price.

        Returns:
            float: Delta value for call/put option.
        """
        if self.option_type == OptionType.CALL_OPTION:
            return norm.cdf(self.d1)
        return norm.cdf(self.d1) - 1
    
    def calculate_gamma(self):
        """
        Compute Gamma, sensitivity of Delta to stock price.

        Returns:
            float: Gamma value.
        """
        return norm.pdf(self.d1) / (self.stock_price * self.volatility * np.sqrt(self.time_to_exp))
    
    def calculate_vega(self):
        """
        Compute Vega, sensitivity of option price to volatility.

        Returns:
            float: Vega value.
        """
        return self.stock_price * norm.pdf(self.d1) * np.sqrt(self.time_to_exp)
    
    def calculate_theta(self):
        """
        Compute Theta, sensitivity of option price to time decay.

        Returns:
            float: Theta value for call/put option.
        """
        if self.option_type == OptionType.CALL_OPTION:
            return -self.stock_price * norm.pdf(self.d1) * self.volatility / (2 * np.sqrt(self.time_to_exp)) - self.risk_free_rate * self.strike_price * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(self.d2)
        else:
            return -self.stock_price * norm.pdf(self.d1) * self.volatility / (2 * np.sqrt(self.time_to_exp)) + self.risk_free_rate * self.strike_price * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(-self.d2)

    def calculate_rho(self):
        """
        Compute Rho, sensitivity of option price to interest rate.

        Returns:
            float: Rho value for call/put option.
        """
        if self.option_type == OptionType.CALL_OPTION:
            return self.stock_price * self.time_to_exp * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(self.d2)
        else:
            return self.stock_price * self.time_to_exp * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(-self.d2)

    def calculate_price(self):
        """
        Compute the Black-Scholes option price.

        Returns:
            float: Option price for call/put.
        """
        self.calculate_d1()
        self.calculate_d2()
        if self.option_type == OptionType.CALL_OPTION:
            self.price = self.stock_price * norm.cdf(self.d1) - self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(self.d2)
        elif self.option_type == OptionType.PUT_OPTION:
            self.price = self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(-1 * self.d2) - self.stock_price * norm.cdf(-1 * self.d1)
        return self.price
    
    def calculate_greeks(self):
        """
        Compute all Greeks (Delta, Gamma, Vega, Theta, Rho).

        Returns:
            list[float]: [Delta, Gamma, Vega, Theta, Rho]
        """
        if (not self.d1):
            self.calculate_price()      # Ensures d1/d2 are computed
        self.delta = self.calculate_delta()
        self.gamma = self.calculate_gamma()
        self.vega = self.calculate_vega()
        self.theta = self.calculate_theta()
        self.rho = self.calculate_rho()
        return [self.delta, self.gamma, self.vega, self.theta, self.rho]

    
