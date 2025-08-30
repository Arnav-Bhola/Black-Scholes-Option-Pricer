# Black-Scholes Option Pricer

An interactive **Python-based Black-Scholes option pricing engine** built with **Streamlit**. This project allows users to explore option sensitivities, risk metrics, and scenario-based payoff analysis using classic derivatives theory.

---

## Features

- **Option Pricing**  
  Calculate **call and put option prices** using the Black-Scholes formula.

- **Greeks Calculation**  
  Compute **Delta, Gamma, Theta, and Vega** to analyze option sensitivities and manage risk.

- **PnL Analysis**  
  Evaluate **profit and loss ratios** across different market scenarios to assess risk-adjusted performance.

- **Heatmaps**  
  Visualize how option prices respond to changes in underlying parameters like stock price, volatility, and time to expiration.

- **Interactive Streamlit Interface**  
  Adjust parameters in real time and explore how different factors impact option pricing and risk metrics.

---

## Motivation

While Black-Scholes is a canonical model in quantitative finance, implementing it from scratch provided me **practical insight into derivative mechanics, hedging intuition, and risk modeling**.

---

## Demo

Explore the interactive web app here:  
[Black-Scholes Option Pricer](https://arnav-bhola-black-scholes-option-pricer-app-q2mvtl.streamlit.app/)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Arnav-Bhola/Black-Scholes-Option-Pricer.git
cd Black-Scholes-Option-Pricer
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run the Streamlit app
```bash
streamlit run app.py
```

## Usage
1. Input the stock price, strike price, time to expiration, volatility, and risk-free rate.
2. Choose option type (call or put).

3. Explore option price, Greeks, PnL ratios, and heatmaps interactively.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests for improvements, additional features, or advanced visualizations.

