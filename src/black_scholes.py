import math
from scipy.stats import norm
import numpy as np
from .enums import OptionType

class BlackScholes():
    def __init__(self, stock_price, strike_price, time_to_exp, risk_free_rate, volatility, option_type=OptionType.CALL_OPTION):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.option_type = option_type
        self.d1 = None

    def calculate_d1(self):
        self.d1 = (math.log(self.stock_price / self.strike_price) + self.time_to_exp * (self.risk_free_rate + ((self.volatility ** 2) / 2))) / (self.volatility * (self.time_to_exp ** 0.5))
        return self.d1
    
    def calculate_d2(self):
        self.d2 = self.d1 - (self.volatility * (self.time_to_exp ** 0.5))
        return self.d2
    
    def calculate_delta(self):
        if self.option_type == OptionType.CALL_OPTION:
            return norm.cdf(self.d1)
        return norm.cdf(self.d1) - 1
    
    def calculate_gamma(self):
        return norm.pdf(self.d1) / (self.stock_price * self.volatility * np.sqrt(self.time_to_exp))
    
    def calculate_vega(self):
        return self.stock_price * norm.pdf(self.d1) * np.sqrt(self.time_to_exp)
    
    def calculate_theta(self):
        if self.option_type == OptionType.CALL_OPTION:
            return -self.stock_price * norm.pdf(self.d1) * self.volatility / (2 * np.sqrt(self.time_to_exp)) - self.risk_free_rate * self.strike_price * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(self.d2)
        else:
            return -self.stock_price * norm.pdf(self.d1) * self.volatility / (2 * np.sqrt(self.time_to_exp)) + self.risk_free_rate * self.strike_price * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(-self.d2)

    def calculate_rho(self):
        if self.option_type == OptionType.CALL_OPTION:
            return self.stock_price * self.time_to_exp * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(self.d2)
        else:
            return self.stock_price * self.time_to_exp * np.exp(-self.risk_free_rate * self.time_to_exp) * norm.cdf(-self.d2)

    def calculate_price(self):
        self.calculate_d1()
        self.calculate_d2()
        if self.option_type == OptionType.CALL_OPTION:
            self.price = self.stock_price * norm.cdf(self.d1) - self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(self.d2)
        elif self.option_type == OptionType.PUT_OPTION:
            self.price = self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(-1 * self.d2) - self.stock_price * norm.cdf(-1 * self.d1)
        return self.price
    
    def calculate_greeks(self):
        if (not self.d1):
            self.calculate_price()
        self.delta = self.calculate_delta()
        self.gamma = self.calculate_gamma()
        self.vega = self.calculate_vega()
        self.theta = self.calculate_theta()
        self.rho = self.calculate_rho()
        return [self.delta, self.gamma, self.vega, self.theta, self.rho]

    
