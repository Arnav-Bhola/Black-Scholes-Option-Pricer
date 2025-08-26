from src.black_scholes import BlackScholes
from src.enums import OptionType

option = BlackScholes(stock_price=100, strike_price=105, time_to_exp=0.5, risk_free_rate=0.05, volatility=0.2, option_type=OptionType.CALL_OPTION)
price = option.calculate_price()
print(option.calculate_greeks())
print(price)