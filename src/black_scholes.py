import math
from scipy.stats import norm
from .enums import OptionType

class BlackScholes():
    def __init__(self, stock_price, strike_price, time_to_exp, risk_free_rate, volatility, option_type=OptionType.CALL_OPTION):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.option_type = option_type

    def calculate_d1(self):
        self.d1 = (math.log(self.stock_price / self.strike_price) + self.time_to_exp * (self.risk_free_rate + ((self.volatility ** 2) / 2))) / (self.volatility * (self.time_to_exp ** 0.5))
        return self.d1
    
    def calculate_d2(self):
        self.d2 = self.d1 - (self.volatility * (self.time_to_exp ** 0.5))
        return self.d2
    
    def calculate_price(self):
        self.calculate_d1()
        self.calculate_d2()
        if self.option_type == OptionType.CALL_OPTION:
            self.price = self.stock_price * norm.cdf(self.d1) - self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(self.d2)
        elif self.option_type == OptionType.PUT_OPTION:
            self.price = self.strike_price * (math.e ** (-1 * self.risk_free_rate * self.time_to_exp)) * norm.cdf(-1 * self.d2) - self.stock_price * norm.cdf(-1 * self.d1)
        return self.price
    
