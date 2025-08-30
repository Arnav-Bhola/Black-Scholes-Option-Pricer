"""
Streamlit App: Black-Scholes Option Pricing Model

This app provides an interactive interface to calculate Option Premiums
and Greeks using the Black-Scholes model. It also visualizes sensitivity
heatmaps for CALL and PUT options with respect to stock price and volatility.

Author: Arnav Bhola
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from src.black_scholes import BlackScholes
from src.enums import OptionType
from src.visualization import HeatmapGenerator

# ---------------------------- #
# Streamlit Page Configuration #
# ---------------------------- #
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------- #
# Utility Functions            #
# ---------------------------- #
def styled_dataframe(df: pd.DataFrame, index_col: str, precision: int = 2):
    """
    Return a styled DataFrame with dark theme for Streamlit display.

    Args:
        df (pd.DataFrame): DataFrame with results to display.
        index_col (str): Column to set as index for display.
        precision (int, optional): Decimal formatting precision. Defaults to 2.

    Returns:
        pd.io.formats.style.Styler: Styled DataFrame ready for st.dataframe.
    """
    df_indexed = df.set_index(index_col)
    return df_indexed.style.set_table_styles([
        {'selector': 'th',
         'props': [('color', 'white'),
                   ('background-color', '#0E1117'),
                   ('text-align', 'left')]},
        {'selector': 'td',
         'props': [('text-align', 'right'),
                   ('color', '#FAFAFA'),
                   ('background-color', '#0E1117')]}
    ]).format(f"{{:.{precision}f}}")


# ---------------------------- #
# Sidebar Controls             #
# ---------------------------- #
with st.sidebar:
    st.title("Black-Scholes Model")

    # LinkedIn profile link
    linkedin_url = "https://www.linkedin.com/in/arnav-bhola/"
    st.markdown(f"""
    <a href="{linkedin_url}" target="_blank" style="text-decoration: none; display: flex; align-items: center; color: inherit;">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
            <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
            <rect width="4" height="12" x="2" y="9"></rect>
            <circle cx="4" cy="4" r="2"></circle>
        </svg>
        <code>Bhola, Arnav</code>
    </a>
    <br><br>
    """, unsafe_allow_html=True)

    # Input fields for model parameters
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_exp = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    risk_free_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    # Heatmap configuration
    st.markdown("---")
    st.write("Heatmap Parameters")
    stock_min = st.number_input(
        "Minimum Stock Price", min_value=0.01, value=current_price * 0.8, step=0.01
    )
    stock_max = st.number_input(
        "Maximum Stock Price", min_value=0.01, value=current_price * 1.2, step=0.01
    )
    vol_min = st.slider(
        "Minimum Volatility", min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01
    )
    vol_max = st.slider(
        "Maximum Volatility", min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01
    )


# ---------------------------- #
# Option Pricing & Greeks       #
# ---------------------------- #
option = BlackScholes(
    stock_price=current_price,
    strike_price=strike,
    time_to_exp=time_to_exp,
    risk_free_rate=risk_free_rate,
    volatility=volatility,
    option_type=OptionType.CALL_OPTION  # Could add a selectbox for CALL/PUT
)

price = option.calculate_price()
greeks = option.calculate_greeks()

# Display Option Pricing Table
price_data = {
    "Parameter": [
        "Current Asset Price", "Strike Price",
        "Time to Maturity (Years)", "Volatility (σ)",
        "Risk-Free Rate", "Option Price"
    ],
    "Value": [current_price, strike, time_to_exp, volatility, risk_free_rate, price]
}
st.markdown("### Black-Scholes Option Pricing Table")
st.dataframe(styled_dataframe(pd.DataFrame(price_data), index_col="Parameter"))
st.markdown("<br>", unsafe_allow_html=True)

# Display Greeks Table
greeks_data = {
    "Greeks": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
    "Value": greeks
}
st.markdown("##### Option Greeks")
st.dataframe(styled_dataframe(pd.DataFrame(greeks_data), index_col="Greeks"))
st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------- #
# Explanatory Text             #
# ---------------------------- #
st.markdown("""
#### Black-Scholes Model Parameters
- **Current Asset Price (S)**: Price of the underlying asset.
- **Strike Price (K)**: Exercise price of the option.
- **Time to Maturity (T)**: Years until expiration.
- **Volatility (σ)**: Annualized standard deviation of returns.
- **Risk-Free Interest Rate (r)**: Theoretical rate of a risk-free asset.

Below you can see the calculated option price along with 
**sensitivity heatmaps** for CALL and PUT options based on stock price and volatility.
<br><br>
""", unsafe_allow_html=True)


# ---------------------------- #
# Heatmap Generation           #
# ---------------------------- #
base_call_price = base_put_price = 0
if not (volatility < vol_min or volatility > vol_max or current_price < stock_min or current_price > stock_max):
    base_call_price = BlackScholes(
        current_price, strike, time_to_exp, risk_free_rate, volatility, OptionType.CALL_OPTION
    ).calculate_price()
    base_put_price = BlackScholes(
        current_price, strike, time_to_exp, risk_free_rate, volatility, OptionType.PUT_OPTION
    ).calculate_price()

heatmap_gen = HeatmapGenerator(
    strike_price=strike,
    time_to_exp=time_to_exp,
    risk_free_rate=risk_free_rate,
    min_stock_price=stock_min,
    max_stock_price=stock_max,
    min_volatility=vol_min,
    max_volatility=vol_max,
    base_call_price=base_call_price,
    base_put_price=base_put_price
)
heatmap_gen.compute_heatmaps()
heatmap_gen.graph_all_heatmaps()

# Display Heatmaps
col1, col2 = st.columns(2)
with col1:
    st.pyplot(heatmap_gen.call_graph)
with col2:
    st.pyplot(heatmap_gen.put_graph)

if base_call_price and base_put_price:
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(heatmap_gen.call_pnl_graph)
    with col2:
        st.pyplot(heatmap_gen.put_pnl_graph)
